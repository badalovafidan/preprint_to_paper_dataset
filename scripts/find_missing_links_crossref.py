import pandas as pd        
import requests              
import time                 
import unicodedata  # normalization text
from difflib import SequenceMatcher  # calculation similarity

# file path
input_file  = "data/categorizedPreprints.csv"
output_file = "data/foundMissingCrossrefData.csv"

# threshold for similarity percentage 
threshold_similarity_score = 0.75

user_agent = {
    "User-Agent": "preprint to paper dataset/0.1 (mailto:your.email@example.com)"
}

# function normalization author name
def normalization_author_name(author_name: str) -> str:
    if author_name is None:
        return ""
    author_name = str(author_name)
    normalized_author_name = unicodedata.normalize("NFKD", author_name)
    standart_ascii_author_name = "".join(character for character in normalized_author_name if not unicodedata.combining(character))
    return " ".join(standart_ascii_author_name.split()).strip()

# calculation function of similarity between two titles
def calculation_title_match_score(first_title: str, second_title: str) -> float:
    return SequenceMatcher(None, first_title.lower(), second_title.lower()).ratio()

# convert date to string
def published_dates(obj) -> str:
    list_published_date = (obj or {}).get("date-parts", [])
    if not list_published_date or not list_published_date[0]:
        return ""
    converted_date_tostr = [str(x) for x in list_published_date[0]]
    return "-".join(converted_date_tostr)

# author list
def convert_authorName_toReadableStr(author_list) -> str:
    if not author_list:
        return ""
    list_authors_temporary = []
    for author in author_list:
        given  = normalization_author_name(author.get("given", "")).strip()
        family = normalization_author_name(author.get("family", "")).strip()
        if family and given:
            list_authors_temporary.append(f"{family}, {given}")
        elif family:
            list_authors_temporary.append(family)
        elif given:
            list_authors_temporary.append(given)
    return "; ".join(list_authors_temporary)

# paper types
required_paper_types = {"journal-article", "proceedings-article"}

# search for title and get the best similar paper
def find_most_similar_title(title: str):
    url = "https://api.crossref.org/works"
    parameters = {
        "query.title": title,
        "rows": 10,
    }
    try:
        crossref_request = requests.get(url, params=parameters, headers=user_agent, timeout=15)
        crossref_request.raise_for_status()
        crossref_papers = crossref_request.json().get("message", {}).get("items", [])
    except Exception:
        return None

    most_similar = None
    most_similar_score = -1.0
    for crossref_paper in crossref_papers:
        crossref_type = (crossref_paper.get("type") or "").lower()
        if crossref_type not in required_paper_types:
            continue  # only required_paper_types

        list_crossref_title = crossref_paper.get("title") or [""]
        crossref_title = list_crossref_title[0] if list_crossref_title else ""
        title_similarity_score = calculation_title_match_score(title, crossref_title)

        if title_similarity_score >= threshold_similarity_score and title_similarity_score > most_similar_score:
            most_similar = crossref_paper
            most_similar_score = title_similarity_score

    if most_similar is None:
        return None

    crossref_title = (most_similar.get("title") or [""])[0]
    crosreff_journal_name = (most_similar.get("container-title") or [""])[0]
    crosreff_authors = convert_authorName_toReadableStr(most_similar.get("author"))
    crossref_online_publication_date = published_dates(most_similar.get("published-online"))
    crossref_issue_online_date = published_dates(most_similar.get("published-print"))
    crossref_doi = most_similar.get("DOI", "")

    return {
        "crossref_title": crossref_title,
        "crossref_journal_name": crosreff_journal_name,
        "crossref_authors": crosreff_authors,
        "crossref_online_publication_date": crossref_online_publication_date,
        "crossref_issue_online_date": crossref_issue_online_date,
        "biorxiv_published_doi": crossref_doi,
        "title_match_score": round(most_similar_score, 2),
    }

# read file
df = pd.read_csv(input_file)

# check the output columns exist (if not, create them)
for column in [
    "biorxiv_published_doi",    
    "crossref_journal_name",
    "crossref_title",
    "crossref_authors",
    "crossref_online_publication_date",
    "crossref_issue_online_date",
    "title_match_score",
]:
    if column not in df.columns:
        df[column] = ""

# filter "preprint only" rows
filter_status = df["custom_status"].astype(str).str.lower().eq("preprint only")
filtered_row_index = df.index[filter_status]

# search on each selected row in crossref
for row_number, row_index in enumerate(filtered_row_index, 1):
    # if biorxiv_title_last is available, use it, if not, use biorxiv_title_1st.
    biorxiv_title = str(
        df.at[row_index, "biorxiv_title_last"] if "biorxiv_title_last" in df.columns and pd.notna(df.at[row_index, "biorxiv_title_last"])
        else df.at[row_index, "biorxiv_title_1st"]
    ).strip()

    if not biorxiv_title:
        continue

    print(f"[{row_number}/{len(filtered_row_index)}] searching: {biorxiv_title[:80]}…")
    match = find_most_similar_title(biorxiv_title)

    if match:
        for crossref_key, crossref_value in match.items():
            df.at[row_index, crossref_key] = crossref_value
            
    # avoid making requests to api too quickly
    time.sleep(1) 

    # update custom_status to "gray zone"
    filtered_rows = filter_status & df["title_match_score"].astype(str).str.strip().ne("")
    df.loc[filtered_rows, "custom_status"] = "gray zone"

# write result
df.to_csv(output_file, index=False, encoding="utf-8-sig")
print(f"done: {output_file}")