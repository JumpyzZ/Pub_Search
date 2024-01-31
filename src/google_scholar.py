import time
import pandas as pd
from scholarly import scholarly
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def search_author_on_google_scholar(google_scholar_id: str, year: str = None) -> pd.DataFrame:
    """
    Retrieve the author's data, fill-in, and print
    :param google_scholar_id: id at Google Scholar's author home url, e.g.https://scholar.google.com/citations?hl=en&user=Q5MZLZQAAAAJ&view_op=list_works
    :param year: which year's publication needed
    :return: a pandas dataframe
    """
    author = scholarly.search_author_id(id=google_scholar_id, filled=True, sortby='year')
    result = [{'name': author['name'],
               'google_scholar_id': author['scholar_id'],
               'pub_title': b['title'],
               'pub_year': b.get('pub_year', None),
               'source': 'Google Scholar'}
              for b in [p['bib'] for p in author['publications']]
              ]
    result_df = pd.DataFrame(result)

    if year:
        result_df = result_df[result_df['pub_year'] == year]

    if len(result_df) == 0:
        result_df = pd.DataFrame({'name': pd.NA,
                                  'google_scholar_id': pd.NA,
                                  'pub_title': 'Result set is empty.',
                                  'pub_year': pd.NA,
                                  'source': 'Google Scholar'}, index=[0])

    return result_df


def get_abstract_from_google_scholar(pub_title: str) -> str:
    pub = scholarly.search_single_pub(pub_title=pub_title)
    bib = pub['bib']
    print(pub_title, bib)
    # result = pd.DataFrame({'title': bib['title'],
    #                        'abstract': bib['abstract'],
    #                        'author': bib['author'],
    #                        'pub_type': bib['pub_type'],
    #                        'pub_url': pub['pub_url']}, index=[0])
    abstract = bib['abstract']
    return abstract


def fill_abstract_for_google_scholar_result():
    # Read Excel file
    file_path = "../google_scholar_results.csv"
    df = pd.read_csv(file_path)

    # Iterate over rows and retrieve abstracts
    abstracts = []
    for index, row in df.iterrows():
        try:
            title = row["pub_title"]
        except AttributeError:
            # this author don't have a single paper.
            abstracts.append('')
            continue

        abstract = get_abstract_from_google_scholar(title)
        abstracts.append(abstract)
        time.sleep(3)

    # Add abstracts to DataFrame
    df["abstract"] = abstracts

    # Write back to Excel file
    df.to_csv(file_path, index=False)


def main():
    # result = search_author_on_google_scholar(google_scholar_id='Q5MZLZQAAAAJ', year='2022')
    # result = get_abstract_from_google_scholar(pub_title='Sticky Floors, Double-Binds, and Double Whammies: Adjusting for Research Performance Reveals Universitiesâ€™ Gender Pay Gap is Not Disappearing')
    fill_abstract_for_google_scholar_result()


if __name__ == '__main__':
    main()
