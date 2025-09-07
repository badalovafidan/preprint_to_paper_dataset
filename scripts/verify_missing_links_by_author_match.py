import pandas as pd
import re

# file path
input_file = r"data/foundMissingCrossrefData.csv"
output_file = r"data/verifiedMissingCrossrefData.csv"

# read file
df = pd.read_csv(input_file)

# nested tokenization [['family1','given1'], ['family2','given2']]
def nested_tokenization_author_list(list_authors):
    if pd.isna(list_authors) or str(list_authors).strip() == "":
        return []
    author_list = [author.strip() for author in str(list_authors).split(";") if author.strip()]
    list_nested_tokens = []
    for author in author_list:
        author_tokens = re.findall(r"\w+", author.lower(), flags=re.UNICODE)
        if author_tokens:
            list_nested_tokens.append(author_tokens)
    return list_nested_tokens

# calculation author match score
def calculation_author_match_score(biorxiv_authors, crossref_authors):
    biorxiv_nested_tokens  = nested_tokenization_author_list(biorxiv_authors)
    crossref_nested_tokens = nested_tokenization_author_list(crossref_authors)
    if not biorxiv_nested_tokens or not crossref_nested_tokens:
        return 0.0
    list_matched_authors = 0
    counted_as_matched = set() 
    for crossref_author in crossref_nested_tokens:
        crossref_tokens = set(crossref_author)
        for biorxiv_author_index, biorxiv_author in enumerate(biorxiv_nested_tokens):
            if biorxiv_author_index in counted_as_matched:
                continue
            if crossref_tokens.intersection(biorxiv_author):
                list_matched_authors += 1
                counted_as_matched.add(biorxiv_author_index)
                break
    length_longest_author_list = max(len(crossref_nested_tokens), len(biorxiv_nested_tokens))
    match_score = list_matched_authors / length_longest_author_list if length_longest_author_list else 0.0
    return round(match_score, 3)

# author match score
df["author_match_score"] = df.apply(
    lambda row: calculation_author_match_score(row.get("biorxiv_authors_last", ""),row.get("crossref_authors", "")),
    axis=1
)

# author count diff
df["author_count_diff"] = df.apply(
    lambda row: abs(len(nested_tokenization_author_list(row.get("biorxiv_authors_last", ""))) -
                    len(nested_tokenization_author_list(row.get("crossref_authors", "")))),
    axis=1
)

# write result
df.to_csv(output_file, index=False, encoding="utf-8-sig")
print(f"done: {output_file}")