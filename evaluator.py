#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: babacardiallo
"""

import numpy as np

from pricer.factory import PricerFactory
from mc_diffusion import MCDiffusion

class VaRMCEvaluator:
    def __init__(self, calculation_date: str, number_sample: int, diffusion_path: int, threshold: float):
        self.calculation_date = calculation_date
        self.number_sample = number_sample
        self.diffusion_path = diffusion_path
        self.threshold = threshold

        self.mc_diffusion = MCDiffusion(calculation_date, number_sample, diffusion_path)
        self.pricer_factory = PricerFactory()


    def evaluate(self, deals: dict, market_data: dict):
        pass





