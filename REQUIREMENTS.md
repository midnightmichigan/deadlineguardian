# REQUIREMENTS — SLAY HACKS 2026

Sources fetched 2026-11-18 (public pages, no sign-in):
- Overview: https://slayy-hacks.devpost.com/
- Rules: https://slayy-hacks.devpost.com/rules
- Dates: https://slayy-hacks.devpost.com/details/dates
- Eligibility / prizes detail sub-pages returned 404 via text fetch on 2026-11-18 — items that would live only there are flagged UNVERIFIED below rather than guessed.

## Event facts (verified from the pages above)
- Name: SLAY HACKS 2026 — "Build Bold. Think Beyond. Create with AI."
- Organizer: SLAY HACKS Student Community and Organization.
- Format: Global, fully online, via Devpost. Ticket/entry cost: $0.
- Window: November 7, 2026 – December 7, 2026.
- Contact: organisers via the Devpost page (rules list an organiser email; not reproduced here).

## Deadline (verified, dates page)
- Submissions open: November 7, 2026, 12:00 AM EST.
- **Submission deadline: December 7, 2026, 5:00 PM EST.**
- Judging: December 8, 2026, 9:00 AM EST – December 15, 2026, 5:00 PM EST (overview text says Dec 8–14; the dates table says Dec 8–15 — the dates table governs).
- Winners announced: December 17, 2026, 6:00 PM EST (overview text says planned Dec 16 — dates table governs).
- Internal submit buffer for this entry: **December 5, 2026**.

## Prizes (verified, overview)
Total pool $5,000 USD (overview header also renders "$4,500+ in prizes + other prizes"; the four cash prizes sum to $4,500 and the rules state a $5,000 announced pool — treat the four cash awards below as verified, the residual as perks/certificates):
- Grand Prize: $2,000 cash — 1 winner (plus sponsor perks, certificates, mentorship, spotlight per overview).
- Runner-Up: $1,200 cash — 1 winner.
- 3rd Place: $800 cash — 1 winner.
- Best Beginner Hack: $500 cash — 1 winner; "top-scoring project built entirely by first-time hackathon participants."
- Participation Perk: official digital certificates — 35 winners / all registered participants (wording varies by section).

## Eligibility (verified from overview + rules; browser-verified 2026-11-18 03:43–03:48 EST)
- ⚠️ **STUDENT-ONLY CONTRADICTION — LIVE RISK, clarification requested.** The Overview ELIGIBILITY BOX says "Students only" (and excludes companies/professional organizations), while the Overview BODY welcomes "eligible students, developers, designers, researchers, independent builders and AI enthusiasts." Both texts are on the organizer's own pages. A clarification reply was posted 2026-11-18 in the existing Discussions thread (forum_topics/45836) asking whether a non-student independent builder is eligible solo; organizer contact per Rules §15: slayyhacks@gmail.com. **Do not treat non-student eligibility as settled until the organizer answers.**
- Age: no fixed number printed; rule is "above legal age of majority in country of residence" — for Michigan that is 18+. Entrant is 24. ✓
- Country: all countries/territories except Brazil, Crimea, Cuba, Iran, North Korea, Quebec, Russia. US/Michigan fully eligible. ✓
- Mode: participate individually or with a team (overview + Rules §4). Solo explicitly allowed. ✓ Maximum team size: NOT published on overview/rules (irrelevant for a solo entry unless a cap of 1 team-member-minimum appears at registration — check at registration).
- One official submission per project (Rules §4). All team members must be identified/credited.
- Participants must provide accurate registration information; organisers may verify eligibility (Rules §3). Disqualification grounds include eligibility violations and misrepresentation (Rules §11).
- Account state at verification: dakotamccall200 is NOT yet registered for this hackathon (registration is part of the submission pass).

## Theme constraints (verified)
- **AI theme is mandatory.** Rules §5: "All submitted projects must address the artificial intelligence theme and demonstrate a meaningful application of AI." Overview: projects should demonstrate "a clear use of artificial intelligence and have a purpose beyond simply showcasing technology."
- Welcome areas (overview, non-exhaustive): education, healthcare, sustainability, business, productivity, generative AI, intelligent agents, responsible AI. Techniques named: generative AI, machine learning, AI agents, automation, natural language processing, computer vision, predictive systems.
- "There are no restrictions on your creativity beyond the official hackathon rules."
- Original work only; plagiarism/copyright infringement/misrepresentation = disqualification (Rules §6, §11). Third-party APIs, open-source libraries, frameworks, AI models and public datasets are allowed if licence-compliant (Rules §5). Project descriptions must accurately represent the technologies used (Rules §5) — **do not claim an LLM/ML model this build does not use.**
- Responsible AI (Rules §7): no facilitation of unlawful activity, malware, unauthorised access, harmful discrimination, or privacy violations; disclose significant limitations and external dependencies.
- Privacy (Rules §13): do not include confidential information, credentials, or sensitive personal data in public submissions.
- Working prototype or functional demonstration required (overview + Rules §5).

## Required submission fields (verified, overview "What Should You Submit?" + Rules §8)
1. **Project name and overview** — clear title + brief explanation of what was built.
2. **Problem and solution** — the problem, who it is for, how it helps.
3. **AI implementation** — which AI models/APIs/frameworks/technologies were used and how they contribute to functionality.
4. **Working demo** — link to the application/prototype with access instructions; a demonstration video may substitute if no live demo is available.
5. **Screenshots** — interface, features, functionality.
6. **Source code** — GitHub or other accessible repository link, with basic documentation and setup instructions.
7. **Project demonstration video** — **recommended, not required**: ~2–4 minutes introducing the project (overview §7; Rules §8 lists "a working demonstration or video"). A live demo link can stand in for it.
Plus (Rules §8): accurate team information; all links accessible and information complete — incomplete/inaccessible submissions may be excluded from judging.

Devpost-standard fields the form will also present (platform-standard, not hackathon-specific): tagline/short description, "Built with" technology list, try-it-out links, image gallery. Exact required/optional status of each platform field at submit time: **UNVERIFIED** until the submission pass opens the form.

## Judging criteria (verified — note the page carries TWO rubrics)
Primary rubric (overview "How Projects Will Be Evaluated" + Rules §9, identical):
- Innovation and Originality: **25%**
- Technical Implementation: **25%**
- Real World Impact: **20%**
- AI Integration and Responsible Use: **15%**
- User Experience and Presentation: **15%**

Second rubric shown on the overview under a judge profile (points, sums to 100):
- Innovation & Creativity: 30 points
- Technical Execution & Complexity: 30 points
- Design & User Experience: 20 points
- Presentation & Impact: 20 points

Both are documented here because the page presents both; the Rules §9 percentage rubric is the one written into the official rules and is treated as governing. Either way, the same four levers matter: originality, technical quality, UX, and clear presentation/impact. AI integration is explicitly scored in the governing rubric (15%).

## What this means for the DeadlineGuardian build
- Frame the AI honestly: a deterministic, rule-based **natural language processing** triage engine (keyword-signal classification, named-entity-style date/amount extraction, urgency inference) that runs 100% offline — NLP and automation are named welcome techniques. Never describe it as an LLM or trained ML model.
- Lead with the responsible-AI angle the rubric rewards: no data leaves the device, no API key, no account, works on low-end hardware and low connectivity — privacy by architecture, and the trade-off (rules vs. learned model) disclosed in the story.
- Ship: working web demo (static, open-and-run) + Python CLI with identical logic, full offline test suites for both, public repo with README/setup, screenshots, and a <3-minute screen-only demo video (recommended field).
