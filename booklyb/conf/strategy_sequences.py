# Request's data are passed by the request_data arg

# Strategies run when the app is started
INIT_STRATEGIES = []


SEQUENCES = {
    "GET": {
        "/add_book/<string:isbn>": {
            "STRATEGIES": [
                {"CreateBookStrategy": ["isbn"]}

            ]
        },

    },
}
