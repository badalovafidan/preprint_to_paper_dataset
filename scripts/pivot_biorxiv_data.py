import pandas as pd

# file path
input_file = r"data/filteredBiorxivData.csv"
output_file = r"data/pivotedBiorxivData.csv"

# read file
df = pd.read_csv(input_file)

# version is converted to a number so that it can be sorted correctly
df["version"] = pd.to_numeric(df["version"], errors="coerce")
df = df.dropna(subset=["version"])  # delete nan
df["version"] = df["version"].astype(int)

# extract function for the 1st and last version
def extract_1st_and_last_version(group: pd.DataFrame) -> pd.Series:
    sorted_group = group.sort_values(by="version")
    first = sorted_group.iloc[0]
    last  = sorted_group.iloc[-1]

    pivoted = {
        "biorxiv_doi": first["doi"],
        "biorxiv_title_1st": first["title"],
        "biorxiv_title_last": last["title"],
        "biorxiv_authors_1st": first["authors"],
        "biorxiv_authors_last": last["authors"],
        "biorxiv_author_corresponding_1st": first["author_corresponding"],
        "biorxiv_author_corresponding_last": last["author_corresponding"],
        "biorxiv_author_corresponding_institution": last["author_corresponding_institution"],
        "biorxiv_submission_date_1st": first["date"],
        "biorxiv_submission_date_last": last["date"],        
        "biorxiv_version_last": last["version"],
        "biorxiv_type": last["type"],
        "biorxiv_license": last["license"],
        "biorxiv_category": last["category"],
        "biorxiv_jatsxml": last["jatsxml"],
        "biorxiv_abstract_1st": first["abstract"],
        "biorxiv_abstract_last": last["abstract"],
        "biorxiv_published_doi": last["published"],
    }

    return pd.Series(pivoted)

# call function and pivot dataset
pivoted_df = (
    df.groupby("doi", group_keys=False)
      .apply(extract_1st_and_last_version)
      .reset_index(drop=True)
)

# write result
pivoted_df.to_csv(output_file, index=False, encoding="utf-8-sig")

print("done:", output_file)