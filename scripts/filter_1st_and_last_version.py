import pandas as pd

# file path
input_file  = r"data/downloadedBiorxiv.csv"
output_file = r"data/filteredBiorxivData.csv"

# read file
df = pd.read_csv(input_file)

# necessary fields: doi and version
if not {"doi", "version"}.issubset(df.columns):
    raise ValueError(f"columns: {list(df.columns)}")

# convert version to numeric
df["version"] = pd.to_numeric(df["version"], errors="coerce")

# filtering function
def filter_1st_and_last_version(sorted_version: pd.DataFrame) -> pd.DataFrame:
    sorted_version = sorted_version.sort_values("version")
    earliest_version = sorted_version["version"].min()

    # if version 1st does not exist, it is deleted.
    if pd.isna(earliest_version) or int(earliest_version) != 1:
        return sorted_version.iloc[0:0] 

    #  keep only version 1 and the last one
    latest_version = sorted_version["version"].max()
    keep = sorted_version[sorted_version["version"].isin([1, latest_version])].drop_duplicates(subset=["doi", "version"])
    return keep

# call function and filter metadata
filtered_metadata = (
    df.groupby("doi", group_keys=False)
      .apply(filter_1st_and_last_version)
      .reset_index(drop=True)
)

# write result
filtered_metadata.to_csv(output_file, index=False, encoding="utf-8-sig")

# print 
print(f"done:  {output_file}")