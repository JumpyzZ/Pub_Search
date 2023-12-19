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
               'scholar_id': author['scholar_id'],
               'pub_title': b['title'],
               'pub_year': b.get('pub_year', None),
               'source': 'Google Scholar'}
              for b in [p['bib'] for p in author['publications']]
              ]
    result_df = pd.DataFrame(result)

    if year:
        result_df = result_df[result_df['pub_year'] == year]

    return result_df


def main():
    result = search_author_on_google_scholar(google_scholar_id='Q5MZLZQAAAAJ', year='2022')


if __name__ == '__main__':
    main()
