from booklyb.strategies.strategy import Strategy

from booklyb.data.book import Book


class CreateBookStrategy(Strategy):
    def load_data(self):
        self.book = None

    def write_data(self):
        self.book.save()

    def process(self, isbn):
        print(isbn)

        self.book = Book(isbn=isbn)
