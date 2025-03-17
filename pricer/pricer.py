#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 11:35:36 2024

@author: babacardiallo
"""
import abc
import pandas as pd

from Deal.deal import Call, Put, Future

CONVENTION_YEAR_FRACTION = 365

class Pricer(abc.ABC):
    @abc.abstractmethod
    def calculate(self, risk_factor):
        pass

    
class CallPricer(Pricer):
    def __init__(self, calculation_date, instrument: Call):
        self.calculation_date = pd.to_datetime(calculation_date)
        self.instrument = instrument
    
    def calculate(self, risk_factor):
        # TODO: Implement this method
        pass

    
class PutPricer(Pricer):
    def __init__(self, calculation_date, instrument: Put):
        self.calculation_date = pd.to_datetime(calculation_date)
        self.instrument = instrument

    def calculate(self, risk_factor):
        # TODO: Implement this method
        pass


class FuturePricer(Pricer):
    def __init__(self, calculation_date: str, instrument: Future):
        self.calculation_date = pd.to_datetime(calculation_date)
        self.instrument = instrument
    
    def calculate(self, risk_factor):
        # TODO: Implement this method
        pass

    