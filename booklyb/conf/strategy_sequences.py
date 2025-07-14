# Request's data are passed by the request_data arg

# Strategies run when the app is started
INIT_STRATEGIES = []


SEQUENCES = {
    "GET": {
        "/batch/fetch_book_information": {
            "STRATEGIES": [
                "FetchBookInformationStrategy"
            ]
        },
        "/book/<string:id_to_find>": {
            "STRATEGIES": [
                {"GetBookStrategy": ["id_to_find"]}
            ]
        },
        "/book_data/<string:isbn>": {
            "STRATEGIES": [
                {"GetBookDataStrategy": ["isbn"]}
            ]
        }
    },
    "POST": {
        "/book/<string:isbn>": {
            "STRATEGIES": [
                {"CreateBookDataStrategy": ["isbn"]}
            ]
        },

    }
}
