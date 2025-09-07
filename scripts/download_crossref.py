import pandas as pd
import requests
import time  # for sleep function

# file path
input_file  = "data/pivotedBiorxivData.csv"
output_file = "data/downloadedCrossref.csv"

# simple user agent for crossref, recommended for polite requests
user_agent = {
    "User-Agent": "preprint to paper dataset/0.1 (mailto:your.email@example.com)"
}

# function that gets all the necessary fields from the crossref api
def retrieve_crossref_metadata(doi: str):   
    try:
        url = f"https://api.crossref.org/works/{doi}"
        r = requests.get(url, headers=user_agent, timeout=15)
        r.raise_for_status()
        msg = r.json().get("message", {})

        # journal name
        list_journal_name = msg.get("container-title") or []
        crossref_journal_name = list_journal_name[0] if list_journal_name else ""

        # title
        list_all_title = msg.get("title") or []
        crossref_title = list_all_title[0] if list_all_title else ""       

        # author
        list_all_authors = msg.get("author") or []
        list_authors_temporary = []
        for author_name in list_all_authors:
            given = (author_name.get("given") or "").strip()
            family = (author_name.get("family") or "").strip()
            if family and given:
                list_authors_temporary.append(f"{family}, {given}")
            elif family:
                list_authors_temporary.append(family)
            elif given:
                list_authors_temporary.append(given)
        crossref_authors = "; ".join(list_authors_temporary)

        # published date
        def published_dates(obj):
            list_published_date = (obj or {}).get("date-parts", [])
            if not list_published_date or not list_published_date[0]:
                return ""
            converted_date_tostr = [str(x) for x in list_published_date[0]]
            return "-".join(converted_date_tostr)

        crossref_online_publication_date = published_dates(msg.get("published-online"))
        crossref_issue_online_date = published_dates(msg.get("published-print"))

        return {
            "crossref_title": crossref_title,
            "crossref_journal_name": crossref_journal_name,
            "crossref_authors": crossref_authors,
            "crossref_online_publication_date": crossref_online_publication_date,
            "crossref_issue_online_date": crossref_issue_online_date,
        }
    except requests.exceptions.RequestException as e:
        return {
            "crossref_title": "",
            "crossref_journal_name": "",
            "crossref_authors": "",
            "crossref_online_publication_date": "",
            "crossref_issue_online_date": "",
        }
    except Exception as e:
        return {
            "crossref_title": "",
            "crossref_journal_name": "",
            "crossref_authors": "",
            "crossref_online_publication_date": "",
            "crossref_issue_online_date": "",
        }

def main():
    # read file
    df = pd.read_csv(input_file)

    # creat new columns
    for new_column in [
        "crossref_journal_name",
        "crossref_title",        
        "crossref_authors",
        "crossref_online_publication_date",
        "crossref_issue_online_date",
    ]:
        if new_column not in df.columns:
            df[new_column] = ""

    # only rows with published DOI
    filtered_published_doi = df["biorxiv_published_doi"].notna() & (df["biorxiv_published_doi"].astype(str).str.strip() != "")
    rows = df[filtered_published_doi].copy()

    # request crossref line by line
    for row_index in rows.index:
        doi = str(df.at[row_index, "biorxiv_published_doi"]).strip()
        if not doi:
            continue

        crossref_metadata = retrieve_crossref_metadata(doi)

        df.at[row_index, "crossref_journal_name"] = crossref_metadata["crossref_journal_name"]
        df.at[row_index, "crossref_title"] = crossref_metadata["crossref_title"]
        df.at[row_index, "crossref_authors"] = crossref_metadata["crossref_authors"]
        df.at[row_index, "crossref_online_publication_date"] = crossref_metadata["crossref_online_publication_date"]
        df.at[row_index, "crossref_issue_online_date"] = crossref_metadata["crossref_issue_online_date"]

        print(f"{doi} | {crossref_metadata['crossref_title'][:60]}")

        # slow down politely, good practice for crossref
        time.sleep(1.0)

        # save regularly, this is useful if the dataset is large
        if row_index % 100 == 0:
            df.to_csv(output_file, index=False, encoding="utf-8-sig")

    # save data
    df.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"Done: {output_file}")

if __name__ == "__main__":
    main()