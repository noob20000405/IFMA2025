from Deal.deal import Deal
from pricer.pricer import CallPricer, PutPricer, FuturePricer

class PricerFactory:
    def __init__(self):
        pass

    @staticmethod
    def create_pricer(calculation_date, deal: Deal):
        """
        Factory pour créer différents types de pricers.
        :param pricer_type: Type de pricer à créer ('call', 'put', 'future').
        :param underlying_price: Prix de l'actif sous-jacent.
        :param strike: Prix d'exercice.
        :param time_to_maturity: Temps jusqu'à l'échéance (en années).
        :return: Une instance du pricer approprié.
        """
        if deal.get_class_name().lower() == "call":
            return CallPricer(calculation_date, deal)
        elif deal.get_class_name().lower() == "put":
            return PutPricer(calculation_date, deal)
        elif deal.get_class_name().lower() == "future":
            return FuturePricer(calculation_date, deal)
        else:
            raise ValueError(f"Unknown pricer type: {deal.get_class_name()}")
