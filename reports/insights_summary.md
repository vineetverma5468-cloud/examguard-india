# Key Findings — Exam Paper Leak Incidents in India (2014–2024)

*Analysis basis: 66 logged incidents, "India – Exam Paper Leak Cases and Incidents" dataset (Kaggle), cleaned via `scripts/clean_data.py`.*

## 1. Incidents have accelerated sharply since 2021
Year-on-year counts: 2019–20 averaged 2–3 incidents/year. From 2021 onward, that jumped to 8, 11, 15, and 13 in successive years. **59% of all logged incidents (39 of 66) occurred in just 2022–2024**, the most recent three years in the dataset. This is either a genuine rise in leaks, an increase in social-media-driven detection/reporting, or both — a distinction worth flagging to policy stakeholders rather than assuming.

## 2. Uttar Pradesh is a clear, persistent hotspot
UP accounts for 11 of 66 incidents (17%) — more than any other single state, and involves multiple distinct conducting bodies (UPPSC, UP Police Recruitment Board, UP Subordinate Services Selection Commission, UP Board of High School and Intermediate Education). This points to a state-level systemic issue rather than one rogue body.

## 3. Confirmed leaks rarely receive a strong deterrent response
Of the 48 confirmed leaks, **only 4 (8.3%) resulted in a "strong" response** (chargesheet filed or suspension issued). The overwhelming majority (42, ~88%) received a "moderate" response — typically exam cancellation and/or a generic legal-action statement, without a disclosed chargesheet or suspension. Two confirmed leaks had no corrective action recorded at all. This is the accountability gap the dashboard is built to surface.

## 4. Repeat offenders exist and are identifiable
At least 10 conducting bodies have 2 or more incidents on record, including UPPSC (3), CBSE (3), and the Maharashtra State Board of Secondary and Higher Secondary Education (3). Cross-referencing this list against the state hotspot ranking is the fastest way to identify where a proctoring/logistics audit would have the highest expected payoff.

## 5. State-level bodies carry most of the exposure
50 of 66 incidents (76%) involve State-level conducting bodies, vs. 13 Central and 3 Private. Central-body incidents (NTA, CBSE, RRB, SSC) are fewer in count but tend to involve exams with far larger candidate pools, so their impact-per-incident is likely higher even though frequency is lower — a nuance the dashboard flags but the source data can't quantify (see data quality note below).

## Data quality caveat
`Appeared Students` is populated in only 1 of 66 rows (1.5%). Any dashboard or narrative claiming a specific number of "students affected" from this dataset alone would be fabricating precision the source doesn't support. This should be enriched from official conducting-body records before being used as a KPI in a real ministry deployment.

## Suggested next actions for a ministry analyst
1. Prioritize audit resources for conducting bodies appearing on **both** the repeat-offender list and a state hotspot list.
2. Standardize a minimum disclosed response tier (e.g., mandatory chargesheet filing) for any *confirmed* leak, closing the 88% "moderate-only" response gap.
3. Commission a follow-up data-collection effort to backfill `Appeared Students` from official records, since it's currently unusable as an impact metric.
