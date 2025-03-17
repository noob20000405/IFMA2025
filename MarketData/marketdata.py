# -*- coding: utf-8 -*-
import pandas as pd
from dataclasses import dataclass
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: babacardiallo
"""
@dataclass
class Rate:
    name: str
    data: pd.DataFrame

    def get_by_date(self, date: str) -> pd.Series:
        if "Date" not in self.data.columns:
            raise KeyError("La colonne 'Date' est absente du DataFrame.")
        return self.data[self.data["Date"] == date].Price[0]
       
@dataclass    
class Equity:
    name: str
    data: pd.DataFrame

    def get_by_date(self, date: str) -> pd.Series:
        if "Date" not in self.data.columns:
            raise KeyError("La colonne 'Date' est absente du DataFrame.")
        return self.data[self.data["Date"] == date].Price[0]

@dataclass
class Commodity:
    name: str
    data: pd.DataFrame

    def get_by_date(self, date: str) -> pd.Series:
        if "Date" not in self.data.columns:
            raise KeyError("La colonne 'Date' est absente du DataFrame.")
        return self.data[self.data["Date"] == date].Price[0]
        