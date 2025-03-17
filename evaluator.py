#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: babacardiallo
"""

import numpy as np
import pandas as pd

from pricer.factory import PricerFactory
from mc_diffusion import MCDiffusion
from MarketData.marketdata import Equity, Rate

class VaRMCEvaluator:
    def __init__(self, calculation_date: str, number_sample: int, diffusion_path: int, threshold: float):
        self.calculation_date = calculation_date
        self.number_sample = number_sample
        self.diffusion_path = diffusion_path
        self.threshold = threshold

        self.mc_diffusion = MCDiffusion(calculation_date, number_sample, diffusion_path)
        self.pricer_factory = PricerFactory()

        
    def evaluate(self, deals: dict, market_data: dict, T_days: int):
        """
        Évaluation de la VaR basée sur le PnL à un instant T spécifique.
        1. Calcul du prix théorique aujourd'hui (date_spot)
        2. Simulation Monte Carlo des prix des actifs sous-jacents à T jours
        3. Simulation Monte Carlo des prix des dérivés basés sur ces simulations
        4. Calcul de la VaR basée sur le PnL à T jours

        Paramètres :
        ------------
        - deals : dict -> Ensemble des transactions
        - market_data : dict -> Données de marché actuelles
        - T_days : int -> Nombre de jours futurs pour évaluer le prix (doit être entre aujourd'hui et maturity)
        """

        var_results = {}

        self.calculation_date = pd.to_datetime(self.calculation_date)

        for deal_id, deal in deals.items():
            # **1. Vérification de T_days**
            max_T_days = (deal.maturity - self.calculation_date).days
            if T_days < 0:
                print(f"Erreur : T_days ({T_days}) ne peut pas être négatif. Fixé à 0.")
                T_days = 0
            if T_days > max_T_days:
                print(f"Erreur : T_days ({T_days}) dépasse la maturité. Fixé à {max_T_days}.")
                T_days = max_T_days

            # **2. Calcul du prix théorique du dérivé aujourd'hui**
            pricer = self.pricer_factory.create_pricer(self.calculation_date, deal)
            # print("market_data: ", market_data)
            theoretical_price = pricer.calculate(market_data)  # Prix calculé aujourd'hui

            # **3. Simulation Monte Carlo des prix des actifs sous-jacents à T_days jours**
            simulated_asset_prices = self.mc_diffusion.diffuse(market_data, T_days)[deal.underlying]
            # print("🔍 Monte Carlo Simulated Prices: ", simulated_asset_prices)

            # **4. Simulation Monte Carlo des prix des dérivés à T_days jours**
            simulated_derivative_prices = []

            target_date = (self.calculation_date + pd.Timedelta(days=T_days)).strftime('%m/%d/%Y')

            for simulated_price in simulated_asset_prices:
                simulated_market_data = {}

                for asset, original_data in market_data.items():
                    simulated_market_data[asset] = type(original_data)(
                        name=original_data.name,
                        data=original_data.data.copy()
                    )

                # **确保构造 `Equity` 或 `Rate` 对象**
                if isinstance(market_data[deal.underlying], Equity):
                    simulated_market_data[deal.underlying] = Equity(
                        name=deal.underlying,
                        data=pd.DataFrame({
                            "Date": [target_date],
                            "Price": [simulated_price]
                        })
                    )
                elif isinstance(market_data[deal.underlying], Rate):
                    simulated_market_data[deal.underlying] = Rate(
                        name=deal.underlying,
                        data=pd.DataFrame({
                            "Date": [target_date],
                            "Price": [simulated_price]
                        })
                    )
                else:
                    raise ValueError(f" Type de marché inconnu pour {deal.underlying}")


                simulated_market_data[deal.underlying].data["Date"] = pd.to_datetime(
                    simulated_market_data[deal.underlying].data["Date"], format="%m/%d/%Y"
                )

                future_pricer = self.pricer_factory.create_pricer(target_date, deal)

                simulated_price_derivative = future_pricer.calculate(simulated_market_data)
                simulated_derivative_prices.append(simulated_price_derivative)

            # **5. Calcul du PnL et de la VaR basée sur le PnL à T_days jours**
            pnl = np.array(simulated_derivative_prices) - theoretical_price  # Calcul du PnL
            var_value = np.percentile(pnl, (1 - self.threshold) * 100)  # Calcul de la VaR
            perte_moyenne = np.mean(pnl)  # Moyenne des pertes sur T jours

            var_results[deal_id] = {
                "Prix du Pricer": round(theoretical_price, 4),
                f"Moyenne simulée MC (T={T_days})": round(np.mean(simulated_derivative_prices), 4),  
                f"VaR (PnL, T={T_days})": round(var_value, 4),
                "Perte moyenne": round(perte_moyenne, 4) 
            }

        # **6. Affichage des résultats**
        print("\n=== Résultats du calcul de la VaR (PnL) à T = {} jours ===".format(T_days))
        for deal_id, result in var_results.items():
            print(f"- Transaction {deal_id}")
            print(f"   - Prix calculé par le Pricer : {result['Prix du Pricer']}")
            print(f"   - Moyenne des simulations MC (T={T_days}) : {result[f'Moyenne simulée MC (T={T_days})']}")
            print(f"   - VaR (PnL, T={T_days}, 99%) : {result[f'VaR (PnL, T={T_days})']}")
            print(f"   - Perte moyenne : {result['Perte moyenne']}")
            print("----------------------------")

        return var_results  # Retourne les résultats de la VaR (PnL)









