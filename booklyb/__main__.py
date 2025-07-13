from flask import Flask, jsonify, request

from booklyb.data.database import engine

import numpy as np
import logging

from booklyb.conf.strategy_sequences import SEQUENCES, INIT_STRATEGIES
from booklyb.strategies.strategy_manager import StrategyManager


from booklyb.error.not_found_error import NotFoundError

from booklyb.data.base import Base

app = Flask(__name__)

logging.getLogger("pymongo").setLevel(logging.ERROR)

strategy_manager = StrategyManager()

# Data init when we start the app
strategy_manager.run_sequence(INIT_STRATEGIES)


with engine.connect() as conn:
    # Create database schema
    Base.metadata.create_all(engine)

# Dynamic
for method, routes in SEQUENCES.items():
    for route, config in routes.items():
        strategies = config.get("STRATEGIES", [])

        def endpoint_function(route=route, strategies=strategies):
            def handler(**kwargs):
                args = np.array([list(s.values()) for s in strategies if type(s) is dict]).flatten().tolist()
                try:
                    if "request_data" in args:
                        response = strategy_manager.run_sequence(strategies, request_data=request.json, **kwargs)
                    else:
                        response = strategy_manager.run_sequence(strategies, **kwargs)
                    return jsonify(response)
                except NotFoundError as e:
                    return {"error": str(e)}, 404
            return handler
        endpoint_name = f"{method}_{route.replace('/', '_')}".strip('_')
        app.route(route, methods=[method], endpoint=endpoint_name)(endpoint_function())


if __name__ == "__main__":
    app.run()
