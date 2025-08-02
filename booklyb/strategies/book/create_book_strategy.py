from booklyb.strategies.strategy import Strategy

from booklyb.data.book import Book

from booklyb.data.image import Image


class CreateBookStrategy(Strategy):
    def load_data(self):
        self.book = None

    def write_data(self):
        self.book.save()

    def process(self, request_data):
        isbn = request_data.get("isbn", None)

        image_b64 = request_data.get("image_b64", None)
        image_mime_type = request_data.get("image_mime_type", None)

        image = None

        if image_b64 and image_mime_type:
            image = Image(image_base64=image_b64, mime_type=image_mime_type)

        self.book = Book(isbn=isbn, image=image)
