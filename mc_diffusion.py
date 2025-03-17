import numpy as np
from arch import arch_model

np.random.seed(1)

class MCDiffusion:
    def __init__(self, date, number_samples, number_paths):
        self.date = date
        self.number_samples = number_samples
        self.number_paths = number_paths

    def volatility_estimation(self, market_data: dict):
        # TODO: Implement this method
        pass

    def correlation_estimation(self, market_data: dict):
        # TODO: Implement this method
        pass

    def diffuse(self, market_data: dict):
        vol_estimation = self.volatility_estimation(market_data=market_data)
        cov_matrix = self.correlation_estimation(market_data=market_data)
        L = np.linalg.cholesky(cov_matrix)
        numb_variable = len(cov_matrix)

        normal_random = np.random.normal(size=(numb_variable, self.number_samples))
        mc_random = np.dot(L, normal_random)
        i = 0
        rf = {}
        for idx in vol_estimation:
            shock = vol_estimation[idx] * mc_random[i]
            rf[idx] = market_data[idx].get_by_date(self.date) + shock

            i = i + 1
        return rf