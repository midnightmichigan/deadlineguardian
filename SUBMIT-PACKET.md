# SUBMIT-PACKET — SLAY HACKS 2026 / DeadlineGuardian

**Deadline: December 7, 2026, 5:00 PM EST — internal buffer: December 5, 2026.**
Hackathon: https://slayy-hacks.devpost.com/ — all requirements verified from the
official overview/rules/dates pages on 2026-11-18; see `REQUIREMENTS.md`.
Status: **BUILD COMPLETE, tests green, NOT submitted, no account created.**

---

## A. Ordered checklist for the submission pass (parent / browser steps only)

1. **Verify eligibility tab live** — the public pages fetched for this build do
   not list an age minimum, country exclusions, or team-size limit (flagged
   UNVERIFIED in `REQUIREMENTS.md`). Open the Devpost eligibility tab and
   confirm a solo independent builder in Michigan, USA is eligible before
   submitting. Do not guess it.
2. **Register** on https://slayy-hacks.devpost.com/ (Google sign-in first per
   browser account order; create an account if none — never surface a Vault card).
3. **Publish the repo** — DONE 2026-11-21: https://github.com/midnightmichigan/deadlineguardian
   (PUBLIC, pushed from this directory; no secrets — the classifier is
   offline, no keys exist to leak).
4. **Host the demo** — DONE 2026-11-21: https://midnightmichigan.github.io/deadlineguardian/
   (live, HTTP 200 verified, zero-login; served from the midnightmichigan.github.io repo).
5. **Record the demo video** — screen-only, under 3 minutes, using the script
   in §D. Nobody on camera. Upload to YouTube (unlisted) and paste the link.
6. **Take the screenshots** — shot list in §E (take them from the live demo).
7. **Submit on Devpost** — paste the field-by-field text in §F verbatim.
8. **Verify** the submission shows as submitted before the December 5 buffer;
   log the confirmation in `~/workspace/bounty-hunts/HUNT-LOG.md`.

---

## B. Project identity (paste-ready)

- **Project name:** DeadlineGuardian
- **Tagline:** Paste a bill, notice, or letter — get what it is, how urgent it is, and the one thing to do next. 100% offline.
- **Built with:** Python 3 · JavaScript (vanilla, no frameworks) · HTML/CSS · regex NLP · pytest-style assert suites · Node.js (web-engine tests)
- **Demo link:** https://midnightmichigan.github.io/deadlineguardian/
- **Video link:** [PASTE unlisted YouTube link, screen-only, under 3 minutes]
- **Code link:** https://github.com/midnightmichigan/deadlineguardian

---

## C. Devpost story (paste-ready; claims only what is built and verified)

### Inspiration
Paperwork is where families lose money and benefits — not because people are
careless, but because a deadline hides in paragraph three of a letter that
arrived with four other letters. A missed renewal can stop food assistance;
a missed bill can cut off power; a missed court date can cost far more.
People who most need help triaging paperwork are also the least likely to
have a paid app, a fast connection, or a spare hour to read every page.
DeadlineGuardian was built for that exact situation: one paste, one answer,
no account, no cost, no waiting.

### What it does
DeadlineGuardian takes the text of a bill, notice, or letter and returns a
complete triage card: the category (bill due, court/legal, benefits,
school/childcare, medical, housing, vehicle, tax, or general notice), an
urgency level, every due date and dollar amount found, a day-countdown to
the earliest deadline (including days overdue), the matched signals and a
confidence score explaining why it decided that, a recommended action window,
and one concrete next action. Paste several documents at once — separated by
a line of `---` — and it returns them sorted most-urgent first with a batch
summary. It runs entirely offline, in the browser or from the command line,
with no account and no API key; the text never leaves the device.

### How we built it
The core is a deterministic, rule-based NLP engine written in Python
(`src/triage.py`) and ported line-for-line to JavaScript (`web/triage.js`)
so both surfaces behave identically. Classification uses weighted keyword
signals per category; date and amount extraction uses regular expressions
that handle written-out dates, numeric dates, and ordinals ("December 3rd");
urgency inference combines escalation language ("final notice", "past due",
"disconnect") with deadline proximity (due within 7 days escalates to
high). The web demo is a single static page with six built-in sample
documents, single and batch modes, and a print/save action. The CLI
(`src/cli.py`) adds demo, interactive, batch-file, and single-document
modes. Everything is covered by four offline test suites: the original
classification cases, v2 checks for countdowns, confidence, signals and
batch sorting, CLI end-to-end subprocess tests, and a web-engine suite that
re-runs the same cases against the JavaScript port to prove parity.

### Challenges we ran into
The honest challenge was a trade-off, not a bug: a rule-based engine can be
misled by unusual wording, where a large language model would be more
flexible — but an LLM would need a network connection, an API key, and would
send a family's paperwork to a third party. We chose privacy and
determinism, and made the trade-off visible instead of hiding it: every
result shows its signals and confidence, so a wrong answer is inspectable
and correctable. A second, smaller challenge was date parsing — ordinals
and month names that contain ordinal letters ("August") needed careful
handling, and it is covered by a regression test.

### Accomplishments that we're proud of
- A tool that genuinely works end to end: paste real paperwork text and get
  a correct, explainable triage in under a second, offline, on any device.
- Identical behaviour in two languages: the Python engine and the JavaScript
  port pass the same test cases, including countdowns and batch sorting.
- Explainability as a feature: matched signals and a confidence score on
  every result, instead of a black-box verdict.
- Zero-cost, zero-friction design: no account, no API key, no network, no
  tracking — built for the people who need it most.

### What we learned
- Explainable, deterministic AI can be the right answer when privacy and
  offline access matter more than flexibility — and disclosing the limits
  builds trust rather than losing it.
- Porting an engine between languages is the fastest way to find its
  assumptions: the date parser's ordinal bug only showed up when the same
  cases ran in both runtimes.
- For household paperwork, the highest-value output is not more information
  — it is one decision (what is this, how urgent is it, what do I do
  next) presented in one place.

### What's next for DeadlineGuardian
- A model-swap seam: `classify()` is the single interface where a learned
  model could later be added behind the same output shape, keeping the
  offline rule engine as the always-available fallback.
- More document types (appointment letters with time-of-day, multi-page
  notices) and a "save my deadlines" local calendar export.
- Accessibility pass: larger touch targets and full screen-reader labels on
  the demo page.

### AI implementation (paste into the AI Implementation field)
DeadlineGuardian uses natural language processing — one of the AI techniques
named in the hackathon's welcome areas. Its engine is a deterministic,
rule-based NLP system: weighted keyword-signal classification over eight
household-critical categories, regular-expression entity extraction for due
dates and dollar amounts, and urgency inference from escalation language and
deadline proximity. There is no large language model and no trained machine
learning model in this build — that is a deliberate, disclosed design
choice: the engine is fully explainable (every result lists the signals
that triggered it), fully private (text never leaves the device), and fully
offline (no API key, no network, no cost). The Python engine and the
JavaScript browser port share identical logic and pass the same test cases.
`classify()` is the single seam where a learned model could later be added
behind the same interface.

---

## D. Demo video script — screen-only, target 2:45 (under 3 minutes)

Record the live demo only. Nobody on camera. Narration text below; show the
named screen for each block.

| Time | Show | Say |
|---|---|---|
| 0:00–0:20 | Demo landing page, title and badges | "Paperwork is where families lose money and benefits — a deadline hides in paragraph three of a letter that arrived with four others. DeadlineGuardian turns one paste into one answer: what it is, how urgent it is, and what to do next. It runs completely offline." |
| 0:20–0:55 | Click "Sample: past-due electric bill", triage, scroll the card | "Here is a past-due electric bill. It finds the $90 amount, the December 18th due date, counts down 30 days, and flags it high urgency because of the final-notice language — and it shows exactly which words triggered that decision." |
| 0:55–1:20 | Click "Sample: benefits renewal", triage | "A benefits renewal gets a medium urgency, a 12-day countdown, and a concrete next action — complete the verification before the deadline, because missing it can stop benefits." |
| 1:20–1:55 | Paste two documents separated by `---`, triage the batch | "Paste several documents at once and they come back sorted most urgent first, with a batch summary — the bill that can cut off your power before the appointment reminder." |
| 1:55–2:25 | Terminal: `python3 src/cli.py demo` | "The same engine runs from the command line — same answers, same tests. Four offline test suites cover both the Python engine and the JavaScript port, so both surfaces stay in lockstep." |
| 2:25–2:45 | Back on the demo, footer note | "DeadlineGuardian is rule-based NLP by design: no account, no API key, no network, and your paperwork never leaves the device. That is the whole point — built for the people who need it most." |

---

## E. Screenshot shot list (take from the live demo)

1. **Landing + samples** — full page with the title, offline badges, and the six sample buttons visible.
2. **Single triage card** — past-due electric bill result: category, high urgency, countdown, confidence bar, matched-signal chips, next action.
3. **Batch result** — two documents triaged, sorted most-urgent first, with the batch summary line.
4. **Benefits card** — SNAP renewal result showing the medium urgency and 12-day countdown.
5. **CLI demo** — terminal running `python3 src/cli.py demo`, showing all three documents plus the batch summary.

---

## F. Field-by-field form text

- **Project name:** DeadlineGuardian
- **Tagline:** Paste a bill, notice, or letter — get what it is, how urgent it is, and the one thing to do next. 100% offline.
- **Problem and solution:** Families lose money and benefits when a deadline hides in a letter that arrived with four others — a missed renewal can stop food assistance, a missed bill can cut power, a missed court date costs far more. DeadlineGuardian takes pasted paperwork text and returns one triage card: category, urgency, due dates and amounts, a day-countdown to the deadline, the signals behind the decision, and one concrete next action. It is built for people with no paid app, no fast connection, and no spare hour — it works offline, with no account and no cost.
- **AI implementation:** See §C "AI implementation" above — rule-based NLP (weighted keyword-signal classification, regex date/amount extraction, urgency inference). No LLM and no trained ML model; disclosed by design for privacy and explainability.
- **Working demo:** https://midnightmichigan.github.io/deadlineguardian/ — open-and-run, no login; six sample documents built in; single and batch modes.
- **Screenshots:** §E shots 1–5.
- **Source code:** https://github.com/midnightmichigan/deadlineguardian — README with setup and test instructions; no secrets (offline classifier, no keys).
- **Video:** [PASTE unlisted YouTube link] — screen-only, under 3 minutes; script in §D.
- **Built with:** Python 3 · JavaScript (vanilla, no frameworks) · HTML/CSS · regex NLP · Node.js (web-engine tests)
- **Team:** solo independent builder.
