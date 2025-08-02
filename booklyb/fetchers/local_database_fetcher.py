from booklyb.data.log import log, WARNING_MORE_THAN_ONE_RESULT_RETURNED
from booklyb.data.book_info import BookInfo


MSG_WRN_MORE_THAN_ONE_RESULT_RETURNED = "Execpted one result but {} returned, first id take {} for procesing"


class LocalDatabaseFetcher:
    def fetch(self, isbn):
        local_book_infos = BookInfo.find(isbn=isbn)
        len_local_book_infos = len(local_book_infos)

        if len_local_book_infos >= 1:
            return local_book_infos

        return {}
