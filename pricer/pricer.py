#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 11:35:36 2024

@author: babacardiallo
"""
import abc
import numpy as np
import pandas as pd
from scipy.stats import norm

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
        S = risk_factor[self.instrument.underlying].get_by_date(self.calculation_date.strftime('%m/%d/%Y'))
        K = self.instrument.strike 
        r = self.instrument.rate_const 
        sigma = self.instrument.vol_const 
        T = (self.instrument.maturity - self.calculation_date).days / CONVENTION_YEAR_FRACTION 

        if T <= 0:
            return max(S - K, 0) 

        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)

        call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        return call_price


class PutPricer(Pricer):
    def __init__(self, calculation_date, instrument: Put):
        self.calculation_date = pd.to_datetime(calculation_date)
        self.instrument = instrument

    def calculate(self, risk_factor):
        S = risk_factor[self.instrument.underlying].get_by_date(self.calculation_date.strftime('%m/%d/%Y'))
        K = self.instrument.strike
        r = self.instrument.rate_const 
        sigma = self.instrument.vol_const 
        T = (self.instrument.maturity - self.calculation_date).days / CONVENTION_YEAR_FRACTION

        if T <= 0:
            return max(K - S, 0) 

        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)

        put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        return put_price


class FuturePricer(Pricer):
    def __init__(self, calculation_date: str, instrument: Future):
        self.calculation_date = pd.to_datetime(calculation_date)
        self.instrument = instrument

    def calculate(self, risk_factor):
        S = risk_factor[self.instrument.underlying].get_by_date(self.calculation_date.strftime('%m/%d/%Y'))
        r = self.instrument.rate_const
        T = (self.instrument.maturity - self.calculation_date).days / CONVENTION_YEAR_FRACTION 

        if T <= 0:
            return S 

        future_price = S * np.exp(r * T)
        return future_price

    
