import numpy as np
import pandas as pd
from arch import arch_model

np.random.seed(1)

class MCDiffusion:
    def __init__(self, date, number_samples, number_paths):
        self.date = date
        self.number_samples = number_samples
        self.number_paths = number_paths

    def volatility_estimation(self, market_data: dict, T_days: int):
        """
        Utilisation du modèle GARCH pour estimer la volatilité future sur T jours.
        Retourne un dictionnaire {actif: [sigma_1, sigma_2, ..., sigma_T]}
        """
        vol_estimation = {}

        for asset, data in market_data.items():
            prices = data.data.sort_values("Date")["Price"]
            returns = np.log(prices / prices.shift(1)).dropna()

            model = arch_model(returns, vol="Garch", p=1, q=1)
            res = model.fit(disp="off")

            # Prédiction de la volatilité sur T jours
            forecast = res.forecast(start=0, horizon=T_days)
            sigma_forecast = np.sqrt(forecast.variance.iloc[-1].values)  # Liste [sigma_1, sigma_2, ..., sigma_T]
            vol_estimation[asset] = sigma_forecast

        return vol_estimation  # {CAC40: [σ_1, σ_2, ..., σ_T], TTEF: [...]}


    def correlation_estimation(self, market_data: dict):
        """
        Estimation de la matrice de corrélation des rendements.
        """
        returns_df = pd.DataFrame()

        for asset, data in market_data.items():
            prices = data.data.sort_values("Date")["Price"]
            returns_df[asset] = np.log(prices / prices.shift(1))

        returns_df.dropna(inplace=True)
        correlation_matrix = returns_df.corr() 

        return correlation_matrix.values 

    def diffuse(self, market_data: dict, T_days: int):
        """
        Simulation Monte Carlo des prix futurs des actifs sous-jacents.
        - Utilise un processus GBM avec volatilité dynamique estimée par GARCH.
        - Génère une trajectoire de prix pour chaque actif.

        Retourne un dictionnaire {actif: liste de prix simulés à T jours}.
        """
        vol_estimation = self.volatility_estimation(market_data, T_days)
        cov_matrix = self.correlation_estimation(market_data)
        L = np.linalg.cholesky(cov_matrix)  

        numb_variable = len(cov_matrix)
        
        normal_random = np.random.normal(size=(self.number_samples, numb_variable, T_days))  # (10000, 3, 10)

        mc_random = np.einsum("ij,njt->nit", L, normal_random)  # (10000, 3, 10)

        rf = {}

        for i, idx in enumerate(vol_estimation):
            S_0 = market_data[idx].get_by_date(self.date)
            sigma_path = vol_estimation[idx]  # Liste de volatilités pour chaque jour

            S_t = np.ones((self.number_samples,)) * S_0  # Initialisation des prix
            for t in range(T_days):
                drift = -0.5 * sigma_path[t] ** 2 * (1 / 365)
                shock = sigma_path[t] * np.sqrt(1 / 365) * mc_random[:, i, t]
                S_t *= np.exp(drift + shock) 

            rf[idx] = S_t 

        return rf  # {CAC40: [prix_1, prix_2, ..., prix_N], ...}


