class RequestError(Exception):
    pass


class MalFormededUUID(RequestError):
    pass


class NoISBNError(RequestError):
    pass
