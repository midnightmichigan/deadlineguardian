import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from datetime import date
from triage import classify, triage_many, summarize_batch

TODAY = date(2026, 11, 18)  # fixed reference for deterministic day math
passed = 0

# days_until: Dec 18, 2026 is exactly 30 days after Nov 18, 2026
t = classify("Your electric bill: amount due $90.00, payment due December 18, 2026. Past due notice.", today=TODAY)
assert t.days_until == 30, t
assert t.signals and "amount due" in t.signals, t
assert 0 < t.confidence <= 0.99, t
assert "Bill due" in t.summary and "urgency high" in t.summary, t
passed += 1

# due within 7 days escalates to high even without urgent words
t = classify("School enrollment form: return by November 24, 2026.", today=TODAY)
assert t.category == "school_childcare", t
assert t.days_until == 6 and t.urgency == "high", t
passed += 1

# far-future date stays medium
t = classify("Property tax notice from the treasurer: $1,200 due 02/14/2027.", today=TODAY)
assert t.urgency == "medium" and t.days_until == 88, t
passed += 1

# overdue date reports negative days and high urgency via window wording
t = classify("Water bill: balance due $45.10 on November 10, 2026.", today=TODAY)
assert t.days_until == -8, t
assert "overdue" in t.summary, t
passed += 1

# ordinal dates parse ("December 3rd, 2026")
t = classify("Lease renewal: respond by December 3rd, 2026.", today=TODAY)
assert t.category == "housing" and t.days_until == 15, t
passed += 1

# month names containing ordinal letters are not corrupted ("August")
t = classify("Registration expires August 20, 2027.", today=TODAY)
assert t.category == "vehicle" and t.days_until is not None, t
passed += 1

# general notice: low confidence fallback, no signals
t = classify("A friendly newsletter with no dates or requests.", today=TODAY)
assert t.category == "general_notice" and t.signals == [] and t.days_until is None, t
passed += 1

# batch: sorted most-urgent first + summary counts
docs = [
    "Clinic appointment reminder for your prescription refill.",
    "Final notice: your electric bill is past due. Amount due $90.00, payment due December 18, 2026.",
    "SNAP redetermination: return your renewal notice by November 30, 2026.",
]
res = triage_many(docs, today=TODAY)
assert [r.urgency for r in res] == ["high", "medium", "low"], res
s = summarize_batch(res)
assert s["total"] == 3 and s["high"] == 1 and s["by_category"]["benefits"] == 1, s
passed += 1

print(f"ALL PASS (python v2: {passed} checks)")
