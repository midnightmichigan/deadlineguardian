# BUILD-LOG — SLAY HACKS 2026 / DeadlineGuardian

## 2026-11-18 — scaffold (discovery run)
- Lane screened and scaffolded: `src/triage.py` (rule-based classifier, 8 categories + general), `tests/test_flow.py` (6 cases), `web/index.html` + `web/triage.js` (minimal JS port), `tests/test_web.mjs`, stub `SUBMIT-PACKET.md`, `README.md`.

## 2026-11-18 — build-out to submittable (this run)
### Requirements
- Fetched the official public pages (no sign-in): overview https://slayy-hacks.devpost.com/, /rules, /details/dates. Eligibility and prizes detail sub-pages returned 404 via text fetch.
- Wrote `REQUIREMENTS.md`: deadline **Dec 7, 2026, 5:00 PM EST** (dates page governs over overview's Dec 16/17 announcement wording), $5,000 pool ($2,000/$1,200/$800/$500), eligibility (independent builders welcome, solo allowed; age/country/team-size **UNVERIFIED** — flagged, not guessed), mandatory AI theme, 7 required submission components (video recommended 2–4 min, not required), and **both** judging rubrics the page carries (Rules §9 percentages govern: Innovation 25 / Technical 25 / Impact 20 / AI Integration 15 / UX+Presentation 15).

### Build (v2 engine, Python + JS parity)
- `src/triage.py` rewritten: weighted keyword signals; explainability fields (`signals`, `confidence`, `summary`); real date parsing (written-out, numeric, ordinal — incl. an ordinal-stripping bug found and fixed: naive stripping corrupted "August"); `days_until` countdown (negative = overdue); urgency escalation when a deadline is ≤7 days away; `triage_many()` urgency-sorted batch + `summarize_batch()`. Original public fields and all original test expectations preserved.
- `src/cli.py` (new): `demo` (3 scripted documents + batch summary), `repl`, `batch FILE` (`---`-separated, urgency-sorted), `once` (stdin). `DEADLINEGUARDIAN_TODAY` env override for deterministic tests.
- `web/triage.js` rewritten as a line-for-line v2 port (same weights, urgency, confidence, countdown, batch logic).
- `web/index.html` rebuilt: 6 one-click sample documents, single + batch modes, triage card with category/urgency/countdown/confidence bar/matched-signal chips/action window/next action, print/save, HTML-escaped rendering, offline/no-account badges, honest footer (rule-based NLP, not an LLM).

### Tests — exact commands and results (2026-11-18, all offline)
Run from `~/workspace/bounty-hunts/slay-hacks-2026/`:
- `python3 tests/test_flow.py` → **ALL PASS (6 cases + extraction check)**, rc=0
- `python3 tests/test_v2.py` → **ALL PASS (python v2: 8 checks)**, rc=0
- `python3 tests/test_cli.py` → **ALL PASS (python cli: 3 checks)**, rc=0
- `node tests/test_web.mjs` → **ALL PASS (web triage: 13 checks incl. original 6 cases + extraction + v2 parity)**, rc=0
- `node --check web/triage.js` → OK; inline UI script extracted and `node --check` → OK
- Smoke: `DEADLINEGUARDIAN_TODAY=2026-11-18 python3 src/cli.py demo` → 3 documents triaged correctly (bill high/30 days, benefits medium/12 days, medical low) + batch summary.

### Submission packet
- `SUBMIT-PACKET.md` rewritten completely: ordered submission-pass checklist (incl. live eligibility-tab verification), project identity, full Devpost story (inspiration / what it does / how built / challenges / accomplishments / learned / next), a dedicated AI-implementation paragraph that honestly describes rule-based NLP with **no LLM/ML claim**, a timed **2:45** screen-only demo script, a 5-shot screenshot list, and field-by-field form text with [PASTE] slots only for URLs that do not exist yet.
- `README.md` rewritten with repo-grade setup, run, and test instructions (Rules §8 documentation requirement).

## Final state
- **Submittable.** Nothing submitted; no account created or signed into; $0 spent.
- Remaining for the submission pass (parent/browser steps, ordered in SUBMIT-PACKET §A): (1) verify the live Devpost eligibility tab (age/country/team-size UNVERIFIED), (2) register, (3) publish the public repo, (4) host `web/` statically, (5) record the <3-min screen-only video, (6) take the 5 screenshots, (7) submit with the packet text before the **Dec 5 buffer** (hard deadline Dec 7, 2026, 5:00 PM EST).
