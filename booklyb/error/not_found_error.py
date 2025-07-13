class NotFoundError(Exception):
    pass


class ParamNotFoundError(NotFoundError):
    pass


class PlaceNotFoundError(NotFoundError):
    pass


class ProjectNotFoundError(NotFoundError):
    pass

class ISBNNotFound(NotFoundError):
    pass