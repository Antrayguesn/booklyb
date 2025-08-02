from booklyb.data.fetcher_request import FetcherRequest
from booklyb.data.log import log

from datetime import datetime

from sqlalchemy import func
from sqlalchemy import select


class Fetcher():
    RATE_LIMIT = -1
    RATE_TIME_LIMIT = -1
    HTTP_REQUEST = True

    TRUST_INDICE = 999

    def is_under_rate_limit(self):
        if self.__class__.RATE_LIMIT == -1 or self.__class__.RATE_TIME_LIMIT == -1:
            return True

        query = select(
            func.count()
        ).select_from(FetcherRequest).where(
            FetcherRequest.fetcher_name == self.__class__.FETCHER_NAME,
            FetcherRequest.timestamp > datetime.utcnow() - self.__class__.RATE_TIME_LIMIT
        )

        count = FetcherRequest.execute_query(query)[0]
        print(count)
        return self.RATE_LIMIT < count

    def record_a_fetch_request(self, request_data):
        fetcher_name = self.__class__.FETCHER_NAME
        if fetcher_name or fetcher_name == "":
            log("WARNING_00004", f"No fetcher name definied, fetcher_name will be class name : {self.__class__.__name__}")
            fetcher_name = self.__class__.__name__

        status_code = None
        error_result = None
        if self.__class__.HTTP_REQUEST:
            status_code = request_data.status_code
            if status_code > 299:
                error_result = request_data.text

        return FetcherRequest(fetcher_name=fetcher_name, status_code=status_code, result_error=error_result)

    def fetch(self, data):
        pass

    def get_data(self, **kwargs):
        pass

    def process(self, **kwargs):
        if self.is_under_rate_limit() is False:
            log("WARNING_00222",
                f"Rate limit for {self.__class_FETCHER_NAME} is exceeded",
                fetcher_name=self.__class__.FETCHER_NAME,
                rate_limit=self.__class__.RATE_LIMIT,
                rate_time_limit=self.__class__.RATE_TIME_LIMIT,
                )
            return {}
        data = self.get_data(**kwargs)
        book_info = self.fetch(data)
        fetcher_request = self.record_a_fetch_request(data)

        book_info.fetcher_request = fetcher_request

        book_info.save()
