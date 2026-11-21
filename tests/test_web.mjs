import { createRequire } from "module";
const require = createRequire(import.meta.url);
const { classify, triageMany, summarizeBatch } = require("../web/triage.js");
const TODAY = "2026-11-18"; // fixed reference, mirrors tests/test_v2.py

const cases = [
  ["Your electric bill: amount due $90.00, payment due December 18, 2026. Past due notice.", "bill_due", "high"],
  ["You are summoned to court for a hearing on 01/05/2027, case no. 26-123.", "court_legal", "medium"],
  ["SNAP redetermination: return your renewal notice by November 30, 2026.", "benefits", "medium"],
  ["Property tax notice from the treasurer: $1,200 due 02/14/2027.", "tax", "medium"],
  ["Clinic appointment reminder for your prescription refill.", "medical", "low"],
  ["A friendly newsletter with no dates or requests.", "general_notice", "low"],
];
let passed = 0;
for (const [text, cat, urg] of cases) {
  const t = classify(text, TODAY);
  if (t.category !== cat) throw new Error(`${t.category} != ${cat}`);
  if (t.urgency !== urg) throw new Error(`${t.urgency} != ${urg} for ${cat}`);
  if (!t.action) throw new Error("missing action");
  passed++;
}
const t0 = classify(cases[0][0], TODAY);
if (!t0.amounts.length || !t0.due_dates.length) throw new Error("extraction failed");
passed++;

// v2 parity checks (mirror tests/test_v2.py)
if (t0.days_until !== 30) throw new Error(`days_until ${t0.days_until} != 30`);
if (!t0.signals.includes("amount due")) throw new Error("signals missing 'amount due'");
if (!(t0.confidence > 0 && t0.confidence <= 0.99)) throw new Error("confidence out of range");
passed++;
const near = classify("School enrollment form: return by November 24, 2026.", TODAY);
if (near.category !== "school_childcare" || near.days_until !== 6 || near.urgency !== "high") throw new Error("near-date escalation failed");
passed++;
const over = classify("Water bill: balance due $45.10 on November 10, 2026.", TODAY);
if (over.days_until !== -8 || !over.summary.includes("overdue")) throw new Error("overdue handling failed");
passed++;
const ord = classify("Lease renewal: respond by December 3rd, 2026.", TODAY);
if (ord.category !== "housing" || ord.days_until !== 15) throw new Error("ordinal date parse failed");
passed++;
const aug = classify("Registration expires August 20, 2027.", TODAY);
if (aug.category !== "vehicle" || aug.days_until === null) throw new Error("August parse failed");
passed++;
const res = triageMany([
  "Clinic appointment reminder for your prescription refill.",
  "Final notice: your electric bill is past due. Amount due $90.00, payment due December 18, 2026.",
  "SNAP redetermination: return your renewal notice by November 30, 2026.",
], TODAY);
if (res.map(r => r.urgency).join(",") !== "high,medium,low") throw new Error("batch sort failed");
const s = summarizeBatch(res);
if (s.total !== 3 || s.high !== 1 || s.by_category.benefits !== 1) throw new Error("batch summary failed");
passed++;

console.log(`ALL PASS (web triage: ${passed} checks incl. original ${cases.length} cases + extraction + v2 parity)`);
