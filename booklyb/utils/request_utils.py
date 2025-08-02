import requests

from booklyb.data.log import log
from booklyb.data.fetcher_request import FetcherRequest

from booklyb.error.internal_error import InternalServerError


def __record_a_fetch_request(fetcher_name: str, url: str, status_code: int, request_content: str):
    FetcherRequest(fetcher_name=fetcher_name, url=url, status_code=status_code, request_content=request_content).save()


def request_url(url: str, fetcher_name: str = None):
    try:
        resp = requests.get(url)
    except requests.exceptions.ConnectionError:
        log("ERROR_0001", "Unable to retrive book information")
        raise InternalServerError("Unable to retrive book data")

    __record_a_fetch_request(fetcher_name=fetcher_name, url=url, status_code=resp.status_code, request_content=resp.text)

    return resp
