from src.google_scholar import search_author_on_google_scholar
from src.scopus import search_author_on_scopus

scopus_api_key = "52454aa42e8b5e5c4f5860f62a6d4c5f"


def main():
    google_scholar_result = search_author_on_google_scholar(google_scholar_id='Q5MZLZQAAAAJ', year='2022')
    scopus_result = search_author_on_scopus(scopus_au_id='57209018448', year=2022)


if __name__ == '__main__':
    main()

