from booklyb.strategies.strategy import Strategy

from booklyb.data.book import Book
from booklyb.data.log import log, INFO_START_FETCHING_BOOK_DATA


from booklyb.fetchers.google_book_api_fetcher import GoogleBooksAPIFetcher
from booklyb.fetchers.local_database_fetcher import LocalDatabaseFetcher


class FetchBookInformationStrategy(Strategy):
    def load_data(self):
        self.books = Book.find(book_info_id=None)
        print(self.books)
        pass

    def write_data(self):
        pass

    def process(self):
        for book in self.books:
            isbn = book.isbn
            log(INFO_START_FETCHING_BOOK_DATA, f"Fetching data for book id : {book.id} isbn {isbn}", book_id=book.id, isbn=isbn)
            print(isbn)

            book_info = LocalDatabaseFetcher().fetch(isbn)
            if not book_info:
                book_info = GoogleBooksAPIFetcher().fetch(isbn)

            book.book_info = book_info
            book.save()

        return {}
