import pandas as pd

# file path
input_file  = r"data/mergedPublicationDate.csv"
output_file = r"data/calculatedDateDifference.csv"

# read file
df = pd.read_csv(input_file)

# convert date time
required_date_columns = [
    "biorxiv_submission_date_1st",
    "biorxiv_submission_date_last",
    "crossref_publication_date",
]
for column in required_date_columns:
    if column in df.columns:
        df[column] = pd.to_datetime(df[column], errors="coerce", infer_datetime_format=True)

# difference between last and 1st submission date for all preprints in biorxiv
df["custom_biorxivVersion_dateDifference"] = (
    (df["biorxiv_submission_date_last"] - df["biorxiv_submission_date_1st"])
    .dt.days
)

#  difference between publish and submission date for only published and gray zone preprints
selected_column = df.get("custom_status", pd.Series(index=df.index, dtype="object")).astype(str).str.lower()
filtered_status = selected_column.isin(["gray zone", "published"])

df["custom_submission&publication_dateDiff"] = pd.NA
df.loc[filtered_status, "custom_submission&publication_dateDiff"] = (
    (df.loc[filtered_status, "crossref_publication_date"] - df.loc[filtered_status, "biorxiv_submission_date_last"])
    .dt.days
)

# write result
df.to_csv(output_file, index=False, encoding="utf-8-sig")
print(f"done: {output_file}")