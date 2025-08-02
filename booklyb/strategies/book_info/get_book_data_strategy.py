from booklyb.strategies.strategy import Strategy

from booklyb.data.log import log, INFO_START_FETCHING_BOOK_DATA
from booklyb.data.book_info import BookInfo

from booklyb.fetchers.google_book_api_fetcher import GoogleBooksAPIFetcher
from booklyb.fetchers.bnf_fetcher import BNFFetcher

from sqlalchemy import select

def merge_dicts(dict1, dict2):
    result = dict1.copy()
    for key, val2 in dict2.items():
        if val2 is not None:
            result[key] = val2
        # si val2 est None, on garde dict1[key] (ou None si absent)
    return result

class GetBookDataStrategy(Strategy):
    FETCHERS = [GoogleBooksAPIFetcher(), BNFFetcher()]

    def load_data(self):
        self.book_data = None

    def write_data(self):
        pass

    def process(self, isbn):
        log(INFO_START_FETCHING_BOOK_DATA, f"Fetching data for isbn {isbn}", isbn=isbn)
        # fetcher_names = [f.__class__.__name__ for f in FETCHERS]
        sorted_fetcher = sorted(self.FETCHERS, key=lambda x: x.TRUST_INDICE, reverse=True)
        print(sorted_fetcher)

        info = {}

        for fetcher in self.FETCHERS:
            query = select(BookInfo).where(
                BookInfo.fetcher_name == fetcher.__class__.__name__,
                BookInfo.isbn == isbn
            )
            database_book_info = BookInfo.execute_query(query=query)
            if database_book_info:
                len_book_info = len(database_book_info)
                if len_book_info > 1:
                    log("WARNING_2333",
                        f"More than one row returned : {len_book_info} results",
                        result_number=len_book_info)
                book_info = database_book_info[0]
            else:
                book_info = fetcher.fetch(isbn)
                book_info = book_info.save()
            print(book_info.to_dict())
            print("*******")
            print(info)
            print("##########")
            info = merge_dicts(info, book_info.to_dict())
            print(info)
            print("*******")

        return info
# https://catalogue.bnf.fr/api/SRU?version=1.2&operation=searchRetrieve&query=bib.fuzzyISBN%20all%20%22978-2-7234-5755-2%22
