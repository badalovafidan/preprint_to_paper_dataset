import pandas as pd
import numpy as np

# file path
input_file  = r"data/standardizedCrossrefData.csv"
output_file = r"data/mergedPublicationDate.csv"

# read file
df = pd.read_csv(input_file, dtype="string", low_memory=False)

publication_online_date = "crossref_online_publication_date"
issue_online_date  = "crossref_issue_online_date"

# clean gaps
for column_name in (publication_online_date, issue_online_date):
    if column_name in df.columns:
        df[column_name] = df[column_name].astype("string").str.strip()

# checking values nan or empty
existed_publication_date = df[publication_online_date].notna() & (df[publication_online_date] != "")
existed_issue_date  = df[issue_online_date].notna()  & (df[issue_online_date]  != "")

# if there is a publication online date, select only it and select the issue date only that time when there is only an issue date 
df["crossref_publication_date"] = np.where(
    existed_publication_date, df[publication_online_date],
    np.where(existed_issue_date, df[issue_online_date], pd.NA)
)

# publication date type column for categorize publish dates
df["crossref_publication_type"] = np.where(
    existed_publication_date, "online published",
    np.where(existed_issue_date, "issue", pd.NA)
)

# write result
df.to_csv(output_file, index=False)
print("done", output_file)