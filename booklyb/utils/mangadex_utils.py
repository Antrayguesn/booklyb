import requests

from unimarc_parser.unimarc_parser import fetch_and_parse_unimarc_bnf

BNF_URL_SEARCH_ISBN = ""


def fetch_book_information(isbn):
    resp = requests.get(BNF_URL_SEARCH_ISBN.format(isbn=isbn))
    content = resp.content
    book_data = fetch_and_parse_unimarc_bnf(content)
    return book_data
