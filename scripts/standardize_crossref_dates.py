import pandas as pd
from datetime import datetime

# file path
input_file = r"data/verifiedMissingCrossrefData.csv"
output_file = r"data/standardizedCrossrefData.csv"

# read file
df = pd.read_csv(input_file)

# function for formating the date MM/DD/YYYY
def standardize_crossref_dates(crossref_publish_date):
    try:
        if pd.isna(crossref_publish_date) or str(crossref_publish_date).strip() == "":
            return ""

        converted_date_tostr = str(crossref_publish_date).strip()

        # if date format is correct then dont change
        try:
            datetime.strptime(converted_date_tostr, "%m/%d/%Y")
            return converted_date_tostr
        except:
            pass

        # for YYYY-MM-DD
        if len(converted_date_tostr.split("-")) == 3:
            return datetime.strptime(converted_date_tostr, "%Y-%m-%d").strftime("%m/%d/%Y")
        # for YYYY-MM
        elif len(converted_date_tostr.split("-")) == 2:
            year, month = converted_date_tostr.split("-")
            return f"{int(month):02d}/01/{year}"
        # for YYYY
        elif len(converted_date_tostr.split("-")) == 1 and len(converted_date_tostr) == 4:
            return f"12/31/{converted_date_tostr}"
        else:
            return ""
    except:
        return ""

# renew dates in the same column
df['crossref_online_publication_date'] = df['crossref_online_publication_date'].apply(standardize_crossref_dates)
df['crossref_issue_online_date'] = df['crossref_issue_online_date'].apply(standardize_crossref_dates)

# write result
df.to_csv(output_file, index=False)
print("done")