"""
clean_data.py
--------------
Cleans and standardizes the raw 'India - Exam Paper Leak Cases and Incidents'
dataset and engineers analysis-ready fields.

Input : data/raw/Paper_leaks_India.csv
Output: data/processed/cleaned_paper_leaks.csv

Run:
    python scripts/clean_data.py
"""

import pandas as pd
import re
from pathlib import Path

RAW_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "Paper_leaks_India.csv"
OUT_PATH = Path(__file__).resolve().parent.parent / "data" / "processed" / "cleaned_paper_leaks.csv"

# ---------------------------------------------------------------------------
# 1. Load (source file is not UTF-8 encoded)
# ---------------------------------------------------------------------------
df = pd.read_csv(RAW_PATH, encoding="latin1")
df.columns = [c.strip() for c in df.columns]

# ---------------------------------------------------------------------------
# 2. Parse dates
# ---------------------------------------------------------------------------
df["Date"] = pd.to_datetime(df["Date of Exam/Incident"], format="%d-%m-%Y", errors="coerce")
df["Year"] = df["Date"].dt.year

# ---------------------------------------------------------------------------
# 3. Standardize state / area names (fixes typos found in the raw file)
# ---------------------------------------------------------------------------
STATE_FIXES = {
    "Maharasthra": "Maharashtra",
    "Gujrat": "Gujarat",
    "Tamilnadu": "Tamil Nadu",
    "All India": "All India",
    "Utar Pradesh": "Uttar Pradesh",
}

def clean_area(val: str) -> str:
    if pd.isna(val):
        return "Not Specified"
    val = val.strip()
    return STATE_FIXES.get(val, val)

df["State"] = df["Area(s) of Incident"].apply(clean_area)

# ---------------------------------------------------------------------------
# 4. Standardize Leak Confirmation Status
# ---------------------------------------------------------------------------
df["Leak Confirmation Status"] = (
    df["Leak Confirmation Status"].str.strip().str.lower().map(
        {"confirmed": "Confirmed", "accused": "Alleged"}
    ).fillna("Not Specified")
)

# ---------------------------------------------------------------------------
# 5. Standardize Action Taken into a fixed set of categories
#    (raw column has spelling variants: "Claim dissmissed" / "dismissed claim" / "claim dismissed")
# ---------------------------------------------------------------------------
def categorize_action(val: str) -> str:
    if pd.isna(val):
        return "Not Reported"
    v = val.strip().lower()
    if "cancel" in v:
        return "Exam Cancelled"
    if "chargesheet" in v:
        return "Chargesheet Filed"
    if "legal action" in v:
        return "Legal Action Taken"
    if "dissmiss" in v or "dismiss" in v:
        return "Claim Dismissed"
    if "no rexam" in v or "no re-exam" in v or "no action" in v:
        return "No Corrective Action"
    if "suspension" in v:
        return "Suspension Issued"
    if "alternative question paper" in v:
        return "Alternative Paper Used"
    if "denied" in v:
        return "Reports Denied"
    return "Other"

df["Action Category"] = df["Action taken"].apply(categorize_action)

# Severity tiering of the response, used for the accountability view
ACTION_SEVERITY = {
    "Chargesheet Filed": "Strong Response",
    "Suspension Issued": "Strong Response",
    "Exam Cancelled": "Moderate Response",
    "Legal Action Taken": "Moderate Response",
    "Alternative Paper Used": "Moderate Response",
    "Claim Dismissed": "No Consequence",
    "Reports Denied": "No Consequence",
    "No Corrective Action": "No Consequence",
    "Not Reported": "Unknown",
    "Other": "Unknown",
}
df["Response Severity"] = df["Action Category"].map(ACTION_SEVERITY)

# ---------------------------------------------------------------------------
# 6. Conducting Body Type / Name cleanup
# ---------------------------------------------------------------------------
df["Conducting Body Type"] = df["Conducting Body Type"].fillna("Not Specified").str.strip()

def clean_body_name(val: str) -> str:
    if pd.isna(val):
        return "Not Specified"
    v = val.strip()
    v = re.sub(r"\bComission\b", "Commission", v)
    v = re.sub(r"\bservice\b", "Service", v)
    return v

df["Conducting Body"] = df["Conducting Body"].apply(clean_body_name)

# ---------------------------------------------------------------------------
# 7. Repeat-offender flag: how many prior incidents this conducting body has had
# ---------------------------------------------------------------------------
df = df.sort_values("Date")
df["Prior Incidents (Same Body)"] = df.groupby("Conducting Body").cumcount()
body_totals = df.groupby("Conducting Body")["Conducting Body"].transform("count")
df["Repeat Offender"] = body_totals > 1

# ---------------------------------------------------------------------------
# 8. Data quality flag for Appeared Students (98% missing in source)
# ---------------------------------------------------------------------------
df["Appeared Students Reported"] = df["Appeared Students"].notna()

# ---------------------------------------------------------------------------
# 9. Final column selection / ordering
# ---------------------------------------------------------------------------
final_cols = [
    "Date", "Year", "Exam Name", "Conducting Body", "Conducting Body Type",
    "State", "Leak Confirmation Status", "Action taken", "Action Category",
    "Response Severity", "Repeat Offender", "Prior Incidents (Same Body)",
    "Note about action Taken", "Note about incident",
    "Appeared Students", "Appeared Students Reported", "References",
]
final_cols = [c for c in final_cols if c in df.columns]
df_out = df[final_cols].sort_values("Date", ascending=False)

OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df_out.to_csv(OUT_PATH, index=False)

print(f"Cleaned {len(df_out)} rows -> {OUT_PATH}")
print(df_out["Action Category"].value_counts())
print(df_out["Response Severity"].value_counts())
