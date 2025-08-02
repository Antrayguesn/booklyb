from booklyb.utils.request_utils import request_url

from unimarc_parser.unimarc_parser import fetch_and_parse_unimarc_bnf

BNF_URL_SEARCH_ISBN = 'https://catalogue.bnf.fr/api/SRU?version=1.2&operation=searchRetrieve&query=bib.fuzzyISBN all "{isbn}"'


def fetch_book_information(isbn, fetcher_name: str = None):
    url = BNF_URL_SEARCH_ISBN.format(isbn=isbn)
    resp = request_url(url, fetcher_name=fetcher_name)
    book_data = fetch_and_parse_unimarc_bnf(resp.text)
    return book_data
