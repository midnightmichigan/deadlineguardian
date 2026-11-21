import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from triage import classify

cases = [
    ("Your electric bill: amount due $90.00, payment due December 18, 2026. Past due notice.", "bill_due", "high"),
    ("You are summoned to court for a hearing on 01/05/2027, case no. 26-123.", "court_legal", "medium"),
    ("SNAP redetermination: return your renewal notice by November 30, 2026.", "benefits", "medium"),
    ("Property tax notice from the treasurer: $1,200 due 02/14/2027.", "tax", "medium"),
    ("Clinic appointment reminder for your prescription refill.", "medical", "low"),
    ("A friendly newsletter with no dates or requests.", "general_notice", "low"),
]
passed = 0
for text, want_cat, want_urg in cases:
    t = classify(text)
    assert t.category == want_cat, (t, want_cat)
    assert t.urgency == want_urg, (t, want_urg)
    assert t.action
    passed += 1
t = classify(cases[0][0])
assert t.amounts and t.due_dates, t
print(f"ALL PASS ({passed} cases + extraction check)")
