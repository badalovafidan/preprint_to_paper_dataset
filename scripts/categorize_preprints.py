import pandas as pd

# file path
input_file = r"data/downloadedCrossref.csv"
output_file = r"data/categorizedPreprints.csv"

# read file
df = pd.read_csv(input_file)

# create a new column: if biorxiv_published_doi is not empty write "published", otherwise "preprint only"
df["custom_status"] = df["biorxiv_published_doi"].apply(
    lambda x: "published" if pd.notna(x) and str(x).strip() != "" else "preprint only"
)

# save the result
df.to_csv(output_file, index=False, encoding="utf-8-sig")

print(f"done: {output_file}")