"""DeadlineGuardian — offline paperwork triage.

A deterministic, rule-based natural-language-processing engine (no network,
no API key, no trained model) that turns a pasted letter / notice / bill
into: a category, an urgency level, extracted due dates and amounts, the
matched signals that explain the decision, a confidence score, a plain-
language summary, and one concrete next action.

Design notes
------------
* Symbolic NLP by design: keyword-signal classification + regex entity
  extraction. It runs identically offline in Python and in the browser
  (web/triage.js is a line-for-line port) and is fully unit-testable.
* Privacy by architecture: text never leaves the device. There is nothing
  to leak, bill, or rate-limit.
* classify() keeps its original public fields (category, urgency,
  due_dates, amounts, action, score) so existing callers and tests keep
  working; v2 adds confidence, signals, summary, days_until and
  recommended_window.
"""
import re
from dataclasses import dataclass, field
from datetime import date, datetime

# category -> (weighted keyword signals, next action)
# Weight 2 = strong, category-specific phrase; weight 1 = supporting word.
CATEGORIES = {
    "bill_due": ({"amount due": 2, "payment due": 2, "balance due": 2, "water bill": 2,
                  "bill": 1, "utility": 1, "electric": 1},
                 "Pay or schedule payment before the due date; if you cannot, call the biller before the due date to ask about a payment plan."),
    "court_legal": ({"summons": 2, "hearing": 2, "case no": 2, "court": 1, "probation": 1, "judge": 1},
                    "Calendar the date immediately and keep the original; do not miss a court date — call the clerk if anything is unclear."),
    "benefits": ({"redetermination": 2, "renewal notice": 2, "food assistance": 2,
                  "snap": 1, "wic": 1, "medicaid": 1, "benefits": 1},
                 "Complete any requested verification before the deadline in the notice; missing it can stop benefits."),
    "school_childcare": ({"immunization": 2, "daycare": 1, "childcare": 1, "school": 1, "enrollment": 1},
                         "Return the form / complete enrollment by the stated date and keep a copy."),
    "medical": ({"prescription": 2, "lab results": 2, "appointment": 1, "clinic": 1, "referral": 1},
                "Confirm the appointment; add it to the calendar with travel time."),
    "housing": ({"land contract": 2, "eviction": 2, "lease": 1, "rent": 1, "mortgage": 1, "landlord": 1},
                "Note the due date; keep proof of every payment; respond in writing to any notice."),
    "vehicle": ({"license plate": 2, "auto insurance": 2, "secretary of state": 2,
                 "registration": 1, "insurance policy": 1, "dmv": 1},
                "Renew / respond before the expiration date to avoid late fees."),
    "tax": ({"property tax": 2, "tax notice": 2, "treasurer": 2, "irs": 1, "assessment": 1},
            "Calendar the tax due date; taxes are not covered by most assistance — plan the payment early."),
}

GENERAL_ACTION = "File it, note any date in it, and check whether a reply is requested."

LABELS = {
    "bill_due": "Bill due",
    "court_legal": "Court / legal",
    "benefits": "Benefits",
    "school_childcare": "School / childcare",
    "medical": "Medical",
    "housing": "Housing",
    "vehicle": "Vehicle",
    "tax": "Tax",
    "general_notice": "General notice",
}

DATE_RE = re.compile(
    r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4}\b"
    r"|\b\d{1,2}/\d{1,2}/\d{2,4}\b", re.I)
AMOUNT_RE = re.compile(r"\$\s?([\d,]+\.\d{2}|[\d,]+)")

URGENT_WORDS = ["final notice", "past due", "overdue", "shutoff", "disconnect",
                "eviction", "deadline", "immediately", "urgent"]


def _parse_date(s: str):
    """Parse one DATE_RE match into a date, or None if it does not parse."""
    s = s.strip()
    for fmt in ("%B %d %Y", "%b %d %Y", "%m/%d/%Y", "%m/%d/%y"):
        try:
            cleaned = re.sub(r"(?<=\d)(st|nd|rd|th)\b", "", s.replace(",", " ")).strip()
            cleaned = re.sub(r"\s+", " ", cleaned)
            return datetime.strptime(cleaned.title(), fmt).date()
        except ValueError:
            continue
    return None


@dataclass
class Triage:
    category: str
    urgency: str
    due_dates: list = field(default_factory=list)
    amounts: list = field(default_factory=list)
    action: str = ""
    score: int = 0
    confidence: float = 0.0
    signals: list = field(default_factory=list)
    summary: str = ""
    days_until: object = None  # int days to the earliest due date, or None
    recommended_window: str = ""


def classify(text: str, today: date = None) -> Triage:
    """Classify one document. `today` is injectable for deterministic tests."""
    if today is None:
        today = date.today()
    low = text.lower()

    best, best_score, best_action, best_signals = "general_notice", 0, GENERAL_ACTION, []
    total_weight = 0
    for cat, (signals, action) in CATEGORIES.items():
        hits = [k for k in signals if k in low]
        score = sum(signals[k] for k in hits)
        total_weight += score
        if score > best_score:
            best, best_score, best_action, best_signals = cat, score, action, hits

    dates = DATE_RE.findall(text)
    amounts = AMOUNT_RE.findall(text)

    parsed = [d for d in (_parse_date(s) for s in dates) if d is not None]
    days_until = min((d - today).days for d in parsed) if parsed else None

    urgent_hit = any(w in low for w in URGENT_WORDS)
    if urgent_hit or (days_until is not None and days_until <= 7):
        urgency = "high"
    elif dates:
        urgency = "medium"
    else:
        urgency = "low"

    if best == "general_notice":
        confidence = 0.35 if not dates and not amounts else 0.5
    else:
        share = best_score / total_weight if total_weight else 0.0
        confidence = round(min(0.99, 0.45 + 0.3 * share + 0.05 * len(best_signals)), 2)

    if urgency == "high":
        window = "Act today — this is time-critical."
    elif days_until is not None and days_until <= 30:
        window = f"Act within the next {max(days_until, 0)} days, before the due date."
    elif dates:
        window = "Calendar it now and act well before the due date."
    else:
        window = "No date pressure found — file it and move on."

    label = LABELS[best]
    bits = [f"{label}"]
    if amounts:
        bits.append("amount " + ", ".join("$" + a for a in amounts))
    if dates:
        bits.append("due " + dates[0])
    if days_until is not None:
        bits.append("overdue" if days_until < 0 else
                    "due today" if days_until == 0 else f"{days_until} day(s) left")
    summary = " · ".join(bits) + f" · urgency {urgency}."

    return Triage(best, urgency, dates, amounts, best_action, best_score,
                  confidence, best_signals, summary, days_until, window)


def triage_many(texts, today: date = None):
    """Triage a batch and return results sorted most-urgent first."""
    rank = {"high": 0, "medium": 1, "low": 2}
    results = [classify(t, today=today) for t in texts]
    return sorted(results, key=lambda r: (rank[r.urgency],
                                          r.days_until if r.days_until is not None else 10 ** 9))


def summarize_batch(results) -> dict:
    """Aggregate counts for a batch of Triage results."""
    out = {"total": len(results), "high": 0, "medium": 0, "low": 0, "by_category": {}}
    for r in results:
        out[r.urgency] += 1
        out["by_category"][r.category] = out["by_category"].get(r.category, 0) + 1
    return out


if __name__ == "__main__":
    import sys
    print(classify(sys.stdin.read()))
