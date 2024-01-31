import os
import csv
from datetime import datetime
import pandas as pd
from src.google_scholar import search_author_on_google_scholar, get_abstract_from_google_scholar
from src.scopus import search_author_on_scopus

scopus_api_key = "52454aa42e8b5e5c4f5860f62a6d4c5f"


def overwrite_data(file, result, id_column):
    if os.path.exists(file):
        df = pd.read_csv(file)
        df[id_column] = df[id_column].astype('str')
        print(df)
        print(result)
        df = df[df[id_column] != result[id_column].iloc[0]]  # remove the existing rows with the same ID
    else:
        df = pd.DataFrame()

    df = pd.concat([df, result])  # append the new data
    df.to_csv(file, index=False)


def collect_publications_for_PIs(year):
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
            google_scholar_result = search_author_on_google_scholar(google_scholar_id=google_scholar_id, year=str(year))

            google_scholar_result['first_name'] = first_name
            google_scholar_result['last_name'] = last_name
            google_scholar_result['updated'] = str(datetime.now())

            overwrite_data(google_scholar_file, google_scholar_result, 'google_scholar_id')

        if pd.notnull(scopus_au_id):
            print(f'Searching for Scopus AU-ID {scopus_au_id}: {last_name} {first_name}')
            scopus_result = search_author_on_scopus(scopus_au_id=scopus_au_id, year=year)

            column_names = ['@_fa','error','link','prism:url','dc:identifier','eid','dc:title','dc:creator','prism:publicationName','prism:eIssn','prism:volume','prism:issueIdentifier','prism:pageRange','prism:coverDate','prism:coverDisplayDate','prism:doi','citedby-count','affiliation','pubmed-id','prism:aggregationType','subtype','subtypeDescription','source-id','openaccess','openaccessFlag','freetoread','freetoreadLabel','article-number','prism:isbn','scopus_au_id','source']
            scopus_result = scopus_result.reindex(columns=column_names)

            scopus_result['first_name'] = first_name
            scopus_result['last_name'] = last_name
            scopus_result['updated'] = str(datetime.now())

            overwrite_data(scopus_file, scopus_result, 'scopus_au_id')


def fill_abstract_for_google_scholar_results() -> None:
    # Read the CSV file
    df = pd.read_csv('google_scholar_results.csv')

    # Apply the function to each row in the DataFrame
    additional_info_list = []
    for pub_title in df['pub_title']:
        additional_info = get_abstract_from_google_scholar(pub_title=pub_title)
        print(additional_info)
        additional_info_list.append(additional_info)

    # Concatenate all additional info DataFrames
    additional_info_df = pd.concat(additional_info_list, ignore_index=True)

    # Join the additional info to the original DataFrame
    df = df.join(additional_info_df)

    # Write the updated DataFrame to a new CSV file
    df.to_csv('updated_google_scholar_results.csv', index=False)


def fill_abstract_for_scopus_results() -> None:
    pass


def create_empty_csv_if_not_exist(filename):
    if not os.path.exists(filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([])
        print(f"Empty CSV file '{filename}' created successfully.")
    else:
        print(f"CSV file '{filename}' already exists.")


def main():
    # # Check and create empty CSV files if they don't exist
    # create_empty_csv_if_not_exist('scopus_results.csv')
    # create_empty_csv_if_not_exist('google_scholar_results.csv')

    # fill_abstract_for_google_scholar_results()
    collect_publications_for_PIs(year=2023)


if __name__ == '__main__':
    main()
