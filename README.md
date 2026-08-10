# ExamGuard India — National Examination Integrity Dashboard

**An end-to-end data analytics project examining exam paper leak incidents in India (2014–2024), built to surface where leaks recur and whether institutional responses actually escalate with severity.**

[View the live dashboard](https://vineetverma5468-cloud.github.io/examguard-india/) · Dataset: [India – Exam Paper Leak Cases and Incidents (Kaggle)](https://www.kaggle.com/)

---

## Problem Statement

Every reported paper leak in India tends to be covered as an isolated news event — a cancelled exam, a viral WhatsApp screenshot, a state minister's statement. What's missing is a systems view: **which states and conducting bodies are repeat offenders, and does a confirmed leak actually trigger a stronger institutional response than a mere allegation — or does everything default to "cancel and re-conduct" with no lasting consequence?**

This project treats the dataset as a policy analyst at the Ministry of Education would: not as a list of scandals, but as an accountability signal. The goal is a dashboard that helps a real analyst decide **where to prioritize audit and security-hardening resources**, using recurrence and response-severity as the ranking criteria — not just raw incident counts.

## Key Findings

- **Incidents have nearly quadrupled since 2020** — 59% of all 66 logged incidents occurred in just the last 3 years of the dataset (2022–2024).
- **Uttar Pradesh is the single largest hotspot** (11 of 66 incidents, ~17%), spread across four different conducting bodies — a state-level pattern, not a one-off failure.
- **Only 8.3% of confirmed leaks resulted in a strong response** (chargesheet or suspension). The other ~92% got a moderate response (exam cancellation / unspecified legal action) or no recorded consequence at all.
- **At least 10 conducting bodies are repeat offenders**, including UPPSC, CBSE, and the Maharashtra State Board — identifiable and rankable, not anecdotal.
- **A critical data gap**: "Appeared Students" is populated in only 1 of 66 records, so "students affected" is deliberately excluded as a dashboard metric rather than estimated.

Full write-up: [`reports/insights_summary.md`](./reports/insights_summary.md)

## Dashboard

Built as a single self-contained HTML file (Chart.js + vanilla JS) — no server or build step required, works directly on GitHub Pages.

- **KPI strip** — total incidents, confirmed-leak rate, states affected, 3-year trend, strong-response rate
- **Trend view** — incidents by year, 2014–2024
- **Hotspot view** — top 10 states, confirmed vs. alleged split
- **Accountability view** — response severity for confirmed leaks only, repeat-offender leaderboard
- **Filterable case log** — filter by year, state, conducting-body type, and confirmation status

> Open `dashboard/index.html` directly in a browser, or enable GitHub Pages on this repo (Settings → Pages → serve from `/dashboard`) to get a shareable link for LinkedIn.

## Project Structure

```
examguard-india/
├── README.md
├── requirements.txt
├── data/
│   ├── raw/
│   │   └── Paper_leaks_India.csv          # original Kaggle export
│   └── processed/
│       └── cleaned_paper_leaks.csv        # cleaned + feature-engineered
├── scripts/
│   └── clean_data.py                      # cleaning & feature engineering pipeline
├── dashboard/
│   ├── index.html                         # standalone interactive dashboard
│   └── data.json                          # aggregated data consumed by the dashboard
└── reports/
    └── insights_summary.md                # written findings & recommendations
```

## Methodology

1. **Ingest** — load the raw CSV (source file uses Latin-1 encoding, not UTF-8).
2. **Clean** —
   - Parse `Date of Exam/Incident` into a proper date + year field.
   - Standardize state names (source has typos like "Maharasthra", "Gujrat").
   - Standardize `Leak Confirmation Status` into `Confirmed` / `Alleged`.
   - Collapse `Action taken` free text into a fixed set of categories, correcting spelling variants (`"Claim dissmissed"` / `"dismissed claim"` / `"claim dismissed"` → `Claim Dismissed`).
   - Fix conducting-body name typos (e.g. "Comission" → "Commission").
3. **Engineer features** —
   - `Response Severity` — maps each action category into `Strong Response` / `Moderate Response` / `No Consequence` / `Unknown`, so severity can be compared against confirmation status.
   - `Repeat Offender` + `Prior Incidents (Same Body)` — identifies conducting bodies with more than one logged incident.
   - `Appeared Students Reported` — explicit boolean flag for the 98%-missing field, so the gap is visible rather than silently dropped.
4. **Analyze** — aggregate by year, state, body type, action category, and severity; cross-tabulate confirmation status against response severity.
5. **Visualize** — a single-file HTML/JS dashboard styled as a policy-briefing document, with a filterable case log for drill-down.

## Tech Stack

| Layer | Tool | Why |
|---|---|---|
| Data cleaning & feature engineering | Python (pandas) | Standard, transparent, reproducible — the whole pipeline is one readable script |
| Dashboard | HTML/CSS/JS + Chart.js | Zero build step, deploys free on GitHub Pages, no backend needed |
| Version control / hosting | Git + GitHub | Portfolio-standard, free static hosting via GitHub Pages |

**Alternative path (if you prefer BI tooling over hand-rolled HTML):** the same `data/processed/cleaned_paper_leaks.csv` loads directly into Power BI or Tableau Public — both are strong, recruiter-recognized choices for an MBA analytics portfolio piece, and the cleaning script gives you a head start either way.

## How to Reproduce

```bash
git clone https://github.com/<your-username>/examguard-india.git
cd examguard-india
pip install -r requirements.txt
python scripts/clean_data.py     # regenerates data/processed/cleaned_paper_leaks.csv
open dashboard/index.html        # or just double-click it
```

## Data Source & Disclaimer

Source data: *"India – Exam Paper Leak Cases and Incidents"*, publicly available on Kaggle, community-compiled from news reporting. This project is an independent portfolio analysis and is **not** affiliated with, endorsed by, or sourced from the Ministry of Education, Government of India. Given the dataset's size (66 incidents) and its reliance on media-reported status, findings should be read as indicative patterns rather than an authoritative national record.

## Author

Built as a portfolio project demonstrating end-to-end data analysis: problem framing → data cleaning → feature engineering → insight generation → dashboard delivery.
