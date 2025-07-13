from datetime import datetime

from booklyb.strategies.strategy import Strategy

from booklyb.utils.google_books_api_fetcher import fetch_book_information

from booklyb.data.book import Book
from booklyb.data.book_info import BookInfo
from booklyb.data.author import Author
from booklyb.data.publisher import Publisher

from booklyb.error.not_found_error import ISBNNotFound


class CreateBookStrategy(Strategy):
    def load_data(self):
        pass

    def write_data(self):
        pass

    def process(self, isbn):
        print(isbn)

        #book_raw_info = fetch_book_information(isbn)
        #print(book_raw_info)
        #if not book_raw_info:
        #    raise ISBNNotFound(f"Unable to find {isbn} isbn")

        book = Book(isbn=isbn)


#        book_info = BookInfo(
#            isbn=isbn,
#            title=book_raw_info["title"],
#            authors=[Author(name=n) for n in book_raw_info["authors"]],
#            publishers=[Publisher(name=book_raw_info["publisher"])],
#            published_date=datetime.strptime(book_raw_info["publishedDate"], "%Y-%m-%d").date(),
#            page_count=book_raw_info["printedPageCount"],
#            dimensions=book_raw_info["dimensions"],
#            maturity_rating=book_raw_info["maturityRating"],
#            language=book_raw_info["language"]
#        )
#
#        book.book_info = book_info

        book.save()

        #print(book.book_info.dimensions)
