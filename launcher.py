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
    var_evaluator.evaluate(deals_collection, mk_data_collection)
    test = 1

if __name__ == "__main__":
    main()


