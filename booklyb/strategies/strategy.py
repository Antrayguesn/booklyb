from booklyb.data.log import INFO_RUN_STRATEGY, INFO_PROCESSING_DATA, INFO_END_PROCESS, log


class Strategy():
    """
    Classe mère représentant une stratégie de traitement par lots.
    """

    def __init__(self):
        """
        Initialise un objet Stragegy avec les répertoires d'entrée et de sortie.
        """
        self.STRATEGY_CODE = "00"

    def log(self, code, msg, **kwargs):
        log(code=code, msg=msg, service_code=self.STRATEGY_CODE, **kwargs)

    def process(self):
        """
        Traite les données chargées.

        Raises:
            NotImplementedError: Cette méthode doit être implémentée par les sous-classes.
        """
        raise NotImplementedError("La méthode 'process' doit être implémentée par les sous-classes.")

    def load_data(self):
        """
        Traite les données chargées.

        Raises:
            NotImplementedError: Cette méthode doit être implémentée par les sous-classes.
        """
        raise NotImplementedError("La méthode 'load_data' doit être implémentée par les sous-classes.")

    def write_data(self):
        """
        Traite les données chargées.

        Raises:
            NotImplementedError: Cette méthode doit être implémentée par les sous-classes.
        """
        raise NotImplementedError("La méthode 'write_data' doit être implémentée par les sous-classes.")

    def run(self, **kwargs):
        """
        Exécute la stratégie complète de traitement par lots.
        """
        self.log(INFO_RUN_STRATEGY, f"Run strategy {self.__class__.__name__}")
        self.load_data()

        self.log(INFO_PROCESSING_DATA, "Processing data ...")
        return_value = self.process(**kwargs)

        self.write_data()

        self.log(INFO_END_PROCESS, "End of strategy")
        return return_value
