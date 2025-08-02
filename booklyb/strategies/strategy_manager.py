from booklyb.strategies.book_info.fetch_book_information_strategy import FetchBookInformationStrategy
from booklyb.strategies.book_info.get_book_data_strategy import GetBookDataStrategy

from booklyb.strategies.book.create_book_strategy import CreateBookStrategy
from booklyb.strategies.book.get_book_strategy import GetBookStrategy

from booklyb.utils.singleton import Singleton
from booklyb.data.log import log, INFO_END_PROCESS, INFO_LOADING_DATA, INFO_RUN_STRATEGIES


class StrategyManager(metaclass=Singleton):
    def __init__(self):
        self.SERVICE_CODE = "100"
        self.STRATEGIES = {CreateBookStrategy.__name__: CreateBookStrategy,
                           FetchBookInformationStrategy.__name__: FetchBookInformationStrategy,
                           GetBookStrategy.__name__: GetBookStrategy,
                           GetBookDataStrategy.__name__: GetBookDataStrategy
                           }

    def run_sequence(self, sequence, **kwargs):
        log(INFO_RUN_STRATEGIES, f"Run strategies {sequence}", self.SERVICE_CODE)

        log(INFO_LOADING_DATA, "Loading data ...", "000")

        return_strategy = None
        strategy_running = None

        for strategy in sequence:
            if type(strategy) is dict:
                for strat, args in strategy.items():
                    strategy_running = self.STRATEGIES[strat]
                    try:
                        params = {arg: kwargs[arg] for arg in args}
                        return_strategy = strategy_running().run(**params)
                    except KeyError as e:
                        log("ERROR_0002", f"Can found arg {e}", "000")
                        raise KeyError

            elif type(strategy) is str:
                strategy_running = self.STRATEGIES[strategy]
                return_strategy = strategy_running().run()
            else:
                log("ERROR_0001", "Paramater not reconized {strategy}", self.SERVICE_CODE)

        log(INFO_END_PROCESS, "End of process", "000")
        return return_strategy
