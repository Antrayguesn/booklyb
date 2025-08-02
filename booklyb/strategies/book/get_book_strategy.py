from booklyb.strategies.strategy import Strategy
from booklyb.error.not_found_error import NotFoundError
from booklyb.error.request_error import MalFormededUUID
from booklyb.data.book import Book

import uuid


class GetBookStrategy(Strategy):
    def load_data(self):
        self.book = None

    def write_data(self):
        pass

    def process(self, id_to_find):
        try:
            uuid_to_find = uuid.UUID(id_to_find)
        except ValueError:
            raise MalFormededUUID(f"{id_to_find} param is not a correct UUID")

        book = Book.find_by_id(uuid_to_find)
        if book is None:
            raise NotFoundError(f"Unable to find the book with id {id_to_find}")
        return book.to_dict()
