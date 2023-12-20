import requests
import json
import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
scopus_api_key = "52454aa42e8b5e5c4f5860f62a6d4c5f"


def search_author_on_scopus(scopus_au_id: str, year: int = None, result_count: int = 100) -> pd.DataFrame:
    """
    This function is used to search for a scholar's publications on Scopus using their Scholar ID.
    The function can also filter the publications based on a specific year.

    :param scopus_au_id: str - The Scholar ID of the author.
    :param year: str - The year of publication. If not provided, publications from all years are returned.
    :return: pd.DataFrame - A DataFrame containing the retrieved publications.
    """
    # Construct URL and header information
    url = f"https://api.elsevier.com/content/search/scopus?query=AU-ID({scopus_au_id})&date={year}&count={result_count}"
    headers = {
        "X-ELS-APIKey": scopus_api_key,
        "Accept": "application/json"
    }

    # Send the request
    response = requests.get(url, headers=headers)

    # Parse the response
    data = json.loads(response.text)

    # Retrieve all publications
    publications = data['search-results']['entry']

    result_df = pd.DataFrame(publications)

    # Tag what AU-ID is used in this query
    result_df['scopus_au_id'] = scopus_au_id
    result_df['source'] = 'Scopus'

    return result_df


def retrieve_abstract_from_scopus(scopus_id: str) -> pd.DataFrame:
    url = f"https://api.elsevier.com/content/abstract/scopus_id/{scopus_id}"
    headers = {
        "X-ELS-APIKey": scopus_api_key,
        "Accept": "application/json"
    }
    params = {
        "field": 'dc:title,authors,dc:description'
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = json.loads(response.text)
        entry = data['abstracts-retrieval-response']
        abstract = entry['coredata']['dc:description']
        authors = entry['authors']['author']
        author_ids = ','.join([a['@auid'] for a in authors])
        author_names = ','.join([a['ce:given-name'] + ' ' + a['ce:surname'] for a in authors])

        result_df = pd.DataFrame({'scopus_id': scopus_id,
                                  'abstract': abstract,
                                  'author_ids': author_ids,
                                  'author_names': author_names}, index=[0])
        return result_df
    else:
        print(f"Error: {response.status_code}")
        return None


if __name__ == '__main__':
    # result = search_author_on_scopus(scopus_au_id='57209398695',
    #                                  year=2023)
    result = retrieve_abstract_from_scopus(scopus_id='85141466366')
    print(result)

