#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Babacar Diallo
"""
import xml.etree.ElementTree as ET
from preprocessing import DealPreprocessing, MarketDataPreprocessing
from evaluator import VaRMCEvaluator

path = './Inputs'
nb_sample = 10000
nb_diffusion_path = 1
date_spot = '03/15/2024'
T_days = 10 # Calcul de la VaR basée sur le PnL à T jours


def main():
    list_deals = ['deal1.xml', 'deal2.xml', 'deal3.xml']
    deals_collection = {}
    for file in list_deals:
        tree = ET.parse(path+'/Deals/'+file)
        deal_pp = DealPreprocessing(tree.getroot())
        deal = deal_pp.build()
        deals_collection[deal.deal_id] = deal

    list_md = ['CAC40', 'FR6MBond', 'TTEF']
    mk_data_collection = {}
    for md in list_md:
        mk_data_pp = MarketDataPreprocessing(path + '/MarketData/' + '{}.csv'.format(md))
        mk_data = mk_data_pp.build(md)
        mk_data_collection[md] = mk_data

    var_evaluator = VaRMCEvaluator(date_spot, nb_sample, nb_diffusion_path, threshold=0.99)
    var_evaluator.evaluate(deals_collection, mk_data_collection, T_days)
    test = 1

if __name__ == "__main__":
    main()

# Resultat: T = 30
"""
=== Résultats du calcul de la VaR (PnL) à T = 30 jours ===
- Transaction Deal 1
   - Prix calculé par le Pricer : 752.9366
   - Moyenne des simulations MC (T=30) : 711.8496
   - VaR (PnL, T=30, 99%) : -65.5857
   - Perte moyenne : -41.087
----------------------------
- Transaction Deal 2
   - Prix calculé par le Pricer : 3.8414
   - Moyenne des simulations MC (T=30) : 3.8314
   - VaR (PnL, T=30, 99%) : -0.0242
   - Perte moyenne : -0.01
----------------------------
- Transaction Deal 3
   - Prix calculé par le Pricer : 1.7534
   - Moyenne des simulations MC (T=30) : 1.631
   - VaR (PnL, T=30, 99%) : -0.2968
   - Perte moyenne : -0.1224
----------------------------
"""

# T = 10
"""
=== Résultats du calcul de la VaR (PnL) à T = 10 jours ===
- Transaction Deal 1
   - Prix calculé par le Pricer : 752.9366
   - Moyenne des simulations MC (T=10) : 739.3579
   - VaR (PnL, T=10, 99%) : -27.6365
   - Perte moyenne : -13.5787
----------------------------
- Transaction Deal 2
   - Prix calculé par le Pricer : 3.8414
   - Moyenne des simulations MC (T=10) : 3.8381
   - VaR (PnL, T=10, 99%) : -0.0106
   - Perte moyenne : -0.0033
----------------------------
- Transaction Deal 3
   - Prix calculé par le Pricer : 1.7534
   - Moyenne des simulations MC (T=10) : 1.7138
   - VaR (PnL, T=10, 99%) : -0.138
   - Perte moyenne : -0.0396
----------------------------
"""

