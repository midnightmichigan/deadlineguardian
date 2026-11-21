"""DeadlineGuardian CLI — demo, interactive, and batch modes.

Usage:
  python3 src/cli.py demo            # scripted end-to-end demo (3 documents)
  python3 src/cli.py repl            # interactive: paste text, blank line ends a document
  python3 src/cli.py batch FILE      # triage a file of documents separated by a line '---'
  python3 src/cli.py once            # read one document from stdin and triage it

Everything runs offline. Dates are evaluated against today unless
DEADLINEGUARDIAN_TODAY=YYYY-MM-DD is set (used by the test suite).
"""
import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from triage import LABELS, classify, summarize_batch, triage_many  # noqa: E402

DEMO_DOCS = [
    ("Electric bill (past due)",
     "Final notice: your electric bill is past due. Amount due $90.00, payment due December 18, 2026. Service may be disconnected after that date."),
    ("Benefits renewal",
     "SNAP redetermination: return your renewal notice with verification by November 30, 2026 to keep your food assistance."),
    ("Clinic reminder",
     "Clinic appointment reminder: your prescription refill appointment is confirmed. Please bring your referral paperwork."),
]


def _today():
    raw = os.environ.get("DEADLINEGUARDIAN_TODAY")
    return date.fromisoformat(raw) if raw else date.today()


def render(t, title=None):
    lines = []
    if title:
        lines.append(f"--- {title} ---")
    lines.append(f"Summary:    {t.summary}")
    lines.append(f"Category:   {LABELS.get(t.category, t.category)} ({t.category})")
    lines.append(f"Urgency:    {t.urgency}  (confidence {t.confidence:.2f})")
    lines.append(f"Due dates:  {', '.join(t.due_dates) if t.due_dates else 'none found'}")
    if t.days_until is not None:
        lines.append(f"Days left:  {t.days_until}")
    lines.append(f"Amounts:    {', '.join('$' + a for a in t.amounts) if t.amounts else 'none found'}")
    lines.append(f"Signals:    {', '.join(t.signals) if t.signals else 'none'}")
    lines.append(f"Window:     {t.recommended_window}")
    lines.append(f"Next action: {t.action}")
    return "\n".join(lines)


def cmd_demo():
    today = _today()
    results = []
    for title, text in DEMO_DOCS:
        t = classify(text, today=today)
        results.append(t)
        print(render(t, title))
        print()
    print("Batch summary:", summarize_batch(results))
    return 0


def cmd_batch(path):
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()
    docs = [d.strip() for d in raw.split("\n---\n") if d.strip()]
    if not docs:
        print("No documents found (separate documents with a line containing only ---).")
        return 1
    results = triage_many(docs, today=_today())
    for i, t in enumerate(results, 1):
        print(render(t, f"Document {i} (sorted by urgency)"))
        print()
    print("Batch summary:", summarize_batch(results))
    return 0


def cmd_repl():
    print("Paste a document, then a blank line to triage it. Ctrl-D to quit.")
    buf = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "" and buf:
            print(render(classify("\n".join(buf), today=_today())))
            print()
            buf = []
        else:
            buf.append(line)
    if buf:
        print(render(classify("\n".join(buf), today=_today())))
    return 0


def cmd_once():
    print(render(classify(sys.stdin.read(), today=_today())))
    return 0


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd = argv[1]
    if cmd == "demo":
        return cmd_demo()
    if cmd == "batch" and len(argv) == 3:
        return cmd_batch(argv[2])
    if cmd == "repl":
        return cmd_repl()
    if cmd == "once":
        return cmd_once()
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
