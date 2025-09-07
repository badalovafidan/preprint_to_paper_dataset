import requests # request to api
import pandas as pd   # read/write csv files

# parameters
server = "biorxiv" # server name: biorxiv or medrxiv
start_date = "2016-01-01" # start date of the period you want to download metadata for
end_date = "2018-12-31" # end date of the period you want to download metadata for
api_url = f"https://api.biorxiv.org/details/{server}/{start_date}/{end_date}/" # api for retrieve metadata
start_point_cursor = 0    # start point of request
max_limit_cursor = 51149  # limit for the request
step_count = 100          # each query returns 100 results.
output_file = "data/downloadedBiorxiv.csv"

# sends a GET request to the given URL and returns a JSON response.
def retrieve_biorxiv_metadata(url: str):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"error: {e}")
        return None


def main():
    # initial request
    initial_response = retrieve_biorxiv_metadata(api_url + "0/json")
    if not initial_response:
        print("initial call failed.")
        return

    print("successfully loaded.")

    try:
        initial_data = initial_response['messages'][0]
        count_preprints = initial_data.get("count_new_papers")

        if count_preprints is None:
            raise KeyError("count_preprints not found")

        print(f"Total preprints: {count_preprints}")

        # list that keeps all the info
        list_all_data = []

        # navigate all pages with the cursor
        for cursor in range(start_point_cursor, max_limit_cursor, step_count):
            url = f"{api_url}{cursor}/json"
            biorxiv_metadata = retrieve_biorxiv_metadata(url)
            if biorxiv_metadata and 'collection' in biorxiv_metadata:
                list_all_data.extend(biorxiv_metadata['collection'])

        # convert to dataframe
        df = pd.DataFrame(list_all_data)

        # write in csv
        df.to_csv(output_file, index=False, encoding="utf-8-sig")

    except KeyError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()