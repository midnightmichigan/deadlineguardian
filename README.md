# DeadlineGuardian — offline paperwork triage

Paste a bill, notice, or letter. DeadlineGuardian tells you what it is, how
urgent it is, what date and amount matter, how many days you have left, why
it decided that — and the one next action to take. It runs **100% offline**:
no account, no API key, no network. Your paperwork never leaves the device.

Built for **SLAY HACKS 2026** (Devpost) — see `REQUIREMENTS.md` for the
official rules this build targets and `SUBMIT-PACKET.md` for the submission.

## What it does

- **Classifies** a document into 8 household-critical categories (bill due,
  court/legal, benefits, school/childcare, medical, housing, vehicle, tax)
  plus a general-notice fallback, using weighted keyword signals from a
  deterministic, rule-based NLP engine.
- **Extracts** due dates (written-out and numeric, including ordinals like
  "December 3rd") and dollar amounts with regex entity extraction.
- **Infers urgency** from escalation language ("final notice", "past due",
  "disconnect") and from deadline proximity (due within 7 days = high).
- **Explains itself**: every result shows the matched signals and a
  confidence score — no black box.
- **Counts down**: days left until the earliest due date (or days overdue).
- **Batch mode**: paste several documents separated by a line containing
  only `---` and get them back sorted most-urgent first, with a summary.

## Run it

### Web demo (no install)
Open `web/index.html` in any browser. It is a single static page; the engine
(`web/triage.js`) is a line-for-line port of the Python engine and behaves
identically. Six sample documents are built in.

### Python CLI (Python 3.10+, no dependencies)
```bash
python3 src/cli.py demo            # scripted end-to-end demo (3 documents)
python3 src/cli.py repl            # interactive: paste text, blank line triages it
python3 src/cli.py batch FILE      # triage a '---'-separated file, urgency-sorted
python3 src/cli.py once < doc.txt  # triage one document from stdin
```

## Tests
```bash
python3 tests/test_flow.py   # original classification cases
python3 tests/test_v2.py     # countdowns, confidence, signals, batch
python3 tests/test_cli.py    # CLI demo / once / batch end-to-end (subprocess)
node    tests/test_web.mjs   # web engine, incl. Python-parity checks
```
All suites pass fully offline.

## How it works / honest limitations

The engine is **symbolic NLP by design** — weighted keyword-signal
classification plus regex date/amount extraction — not a large language
model and not a trained ML model. That is the point: it is deterministic,
explainable, testable, private, and works on low-end hardware with no
connectivity. The trade-off is real and disclosed: unusual wording can be
misclassified, and `classify()` is the single seam where a learned model
could later be swapped in behind the same interface.

## Layout
- `src/triage.py` — the engine (Python)
- `src/cli.py` — demo / repl / batch / once CLI
- `web/index.html`, `web/triage.js` — the browser demo (same engine, ported)
- `tests/` — four offline test suites
- `REQUIREMENTS.md`, `SUBMIT-PACKET.md`, `BUILD-LOG.md` — hackathon records

## Lane facts (SLAY HACKS 2026)
- URL: https://slayy-hacks.devpost.com/ — organized by the SLAY HACKS Student Community
- Prizes: $5,000 pool — Grand $2,000 / Runner-Up $1,200 / 3rd $800 / Best Beginner $500
- Deadline: **December 7, 2026, 5:00 PM EST** (internal buffer: December 5)
- Eligibility: students, developers, designers, researchers, independent builders and AI enthusiasts; solo allowed; $0 entry; fully online; demo video recommended (2–4 min), not required.
