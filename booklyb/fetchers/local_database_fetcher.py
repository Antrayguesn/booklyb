from booklyb.data.log import log, WARNING_MORE_THAN_ONE_RESULT_RETURNED
from booklyb.data.book_info import BookInfo


MSG_WRN_MORE_THAN_ONE_RESULT_RETURNED = "Execpted one result but {} returned, first id take {} for procesing"


class LocalDatabaseFetcher:
    def fetch(self, isbn):
        local_book_infos = BookInfo.find(isbn=isbn)
        len_local_book_infos = len(local_book_infos)

        if len_local_book_infos >= 1:
            # More than one rows returned, just print warning
            if len_local_book_infos > 1:
                book_infos_id = [str(bi.id) for bi in local_book_infos]
                log(code=WARNING_MORE_THAN_ONE_RESULT_RETURNED,
                    msg=MSG_WRN_MORE_THAN_ONE_RESULT_RETURNED.format(len_local_book_infos, local_book_infos[0].id),
                    book_infos_id=book_infos_id)
            return local_book_infos[0]

        return {}
