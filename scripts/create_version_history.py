import pandas as pd

# file path
input_file  = r"data/downloadedBiorxiv.csv"
output_file = r"data/multipleVersions.csv"

# read file
df = pd.read_csv(input_file, dtype=str)

# clean and convert
df['doi'] = df['doi'].str.strip()
df['version'] = pd.to_numeric(df['version'], errors='coerce')

# version one and at least one additional version
has_v1 = df.groupby('doi')['version'].transform(lambda v: (v == 1).any())
has_other = df.groupby('doi')['version'].transform(lambda v: (v != 1).any())

subset = df[has_v1 & has_other].copy()

# write result
subset.sort_values(['doi', 'version']).to_csv(output_file, index=False, encoding="utf-8-sig")

# print 
print(f"done:  {output_file}")