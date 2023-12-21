import os
from datetime import datetime
import pandas as pd
from src.google_scholar import search_author_on_google_scholar
from src.scopus import search_author_on_scopus

scopus_api_key = "52454aa42e8b5e5c4f5860f62a6d4c5f"


def overwrite_data(file, result, id_column):
    if os.path.exists(file):
        df = pd.read_csv(file)
        df[id_column] = df[id_column].astype('str')
        df = df[df[id_column] != result[id_column][0]]  # remove the existing rows with the same ID
    else:
        df = pd.DataFrame()

    df = pd.concat([df, result])  # append the new data
    df.to_csv(file, index=False)


def collect_publications_for_PIs():
    # Load the data from the Excel file
    df = pd.read_excel('TPM 2023 Principal Investigators.xlsx')

    google_scholar_file = 'google_scholar_results.csv'
    scopus_file = 'scopus_results.csv'

    # Print total number of rows to be processed
    print(f'Total PIs to be processed: {len(df)}')

    # Iterate over each row in the dataframe
    for index, row in df.iterrows():
        # Get the necessary data
        first_name = row['First Name']
        last_name = row['Last Name']
        google_scholar_id = row['google_scholar_id']
        if pd.notnull(row['scopus_au_id']):
            scopus_au_id = str(int(row['scopus_au_id']))
        else:
            scopus_au_id = pd.NA
        skip = row['skip']

        # Print current index
        print(f'Processing PI {index + 1} of {len(df)}')

        # Skip this iteration if the 'skip' field is 1
        if skip == 1:
            print(f'Skipping PI {index + 1} as skip field is set to 1')
            continue

        # Search on Google Scholar and Scopus, and write the results to the CSV files
        if pd.notnull(google_scholar_id):
            print(f'Searching for Google Scholar ID {google_scholar_id}: {last_name} {first_name}')
            google_scholar_result = search_author_on_google_scholar(google_scholar_id=google_scholar_id, year='2023')

            google_scholar_result['first_name'] = first_name
            google_scholar_result['last_name'] = last_name
            google_scholar_result['updated'] = str(datetime.now())

            overwrite_data(google_scholar_file, google_scholar_result, 'google_scholar_id')

        if pd.notnull(scopus_au_id):
            print(f'Searching for Scopus AU-ID {scopus_au_id}: {last_name} {first_name}')
            scopus_result = search_author_on_scopus(scopus_au_id=scopus_au_id, year=2023)

            column_names = ['@_fa','error','link','prism:url','dc:identifier','eid','dc:title','dc:creator','prism:publicationName','prism:eIssn','prism:volume','prism:issueIdentifier','prism:pageRange','prism:coverDate','prism:coverDisplayDate','prism:doi','citedby-count','affiliation','pubmed-id','prism:aggregationType','subtype','subtypeDescription','source-id','openaccess','openaccessFlag','freetoread','freetoreadLabel','article-number','prism:isbn','scopus_au_id','source']
            scopus_result = scopus_result.reindex(columns=column_names)

            scopus_result['first_name'] = first_name
            scopus_result['last_name'] = last_name
            scopus_result['updated'] = str(datetime.now())

            overwrite_data(scopus_file, scopus_result, 'scopus_au_id')


def fill_abstract_for_google_scholar_results() -> None:
    pass


def fill_abstract_for_scopus_results() -> None:
    pass


def main():
    collect_publications_for_PIs()


if __name__ == '__main__':
    main()
