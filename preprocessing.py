#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Babacar Diallo
"""
import pandas as pd
from datetime import datetime
from Deal.deal import Call, Put, Future
from MarketData.marketdata import Equity, Rate

class DealPreprocessing:
    """
    Classe pour le préprocessing des données financières ou des contrats
    (transactions, options, contrats à terme). Permet d'extraire, transformer et
    structurer les informations en vue de leur utilisation dans des traitements en aval.
    """

    def __init__(self, root):
        self.root = root

    @staticmethod
    def _get_text(root, name: str) -> str:
        """
        Méthode interne pour extraire du contenu textuel depuis une source de données.

        :param path: Chemin ou clé permettant d'accéder à la donnée textuelle.
        :return: Contenu textuel extrait.
        """

        return str(root.find(name).text)

    @staticmethod
    def _get_value(root, name: str) -> float:
        """
        Méthode interne pour extraire une valeur numérique depuis une source donnée.

        :param path: Chemin ou clé permettant d'accéder à la donnée.
        :param default: Valeur par défaut à retourner si aucune donnée n'est trouvée.
        :return: Valeur numérique extraite.
        """

        return float(root.find(name).text)

    @staticmethod
    def _get_date(root, name: str) -> datetime:
        """
        Méthode interne pour extraire une date et la convertir dans un format spécifique.

        :param path: Chemin ou clé permettant d'accéder à la donnée.
        :param date_format: Format dans lequel la date doit être convertie.
        :return: Objet date (ou chaîne formatée) extrait et converti.
        """

        return datetime.strptime(root.find(name).text, '%m/%d/%Y')

    def build_call(self) -> Call:
        # TODO: Implement this method
        pass

    def build_put(self) -> Put:
        # TODO: Implement this method
        pass

    def build_future(self) -> Future:
        # TODO: Implement this method
        pass


    def build(self):
        """
        Construit l'ensemble des objets ou des structures nécessaires
        pour une transaction complète à partir des données brutes.

        :param raw_data: Les données brutes représentant une transaction.
        :return: Structure contenant les informations complètes et traitées.
        """

        type_deal = self.root.find('type').text

        if type_deal.lower() == 'call':
            deal = self.build_call()
        elif type_deal.lower() == 'put':
            deal = self.build_put()
        elif type_deal.lower() =='future':
            deal = self.build_future()
        else:
            NotImplemented

        return deal


class MarketDataPreprocessing:
    """
    Cette classe permet de préparer et construire les données de marché
    nécessaires pour modéliser des objets financiers (par exemple : Equity ou Rate).
    Elle lit les données stockées dans un fichier CSV et utilise ces informations
    pour construire les différents facteurs de risque.

    Attributs:
    ----------
    - market_state : pd.DataFrame
        Contient les données lues depuis un fichier CSV.

    Méthodes:
    ---------
    - build_equity(name: str) -> Equity:
        Construit un objet Equity (action) à partir des données de marché.

    - build_rate(name: str) -> Rate:
        Construit un objet Rate (taux d'intérêt) à partir des données de marché.

    - build(data_name: str):
        Permet de construire un facteur de risque (Equity ou Rate) en fonction
        du type passé en paramètre.
    """

    def __init__(self, filepath):
        """
        Initialisation de la classe avec le fichier contenant les données de marché.

        Paramètres:
        -----------
        - filepath : str
            Chemin vers le fichier CSV contenant les données de marché.
        """
        self.market_state = pd.read_csv(filepath, sep=';')

    def build_equity(self, name: str) -> Equity:
        """
        Construit un objet Equity en utilisant les données de marché pour une action donnée.

        Paramètres:
        -----------
        - name : str
            Le nom de l'action (par exemple, 'CAC40').

        Retourne:
        ---------
        - Equity : objet Equity correspondant aux données.
        """
        # TODO: Implémenter la logique de création de l'Equity
        pass

    def build_rate(self, name: str) -> Rate:
        """
        Construit un objet Rate en utilisant les données de marché pour un taux donné.

        Paramètres:
        -----------
        - name : str
            Le nom du taux (par exemple, 'FR6MBond').

        Retourne:
        ---------
        - Rate : objet Rate correspondant aux données.
        """
        # TODO: Implémenter la logique de création du Rate
        pass

    def build(self, data_name: str):
        """
        Construit un facteur de risque en fonction du type donné en entrée (Equity ou Rate).

        Paramètres:
        -----------
        - data_name : str
            Le nom du facteur de risque (par exemple 'CAC40', 'TTEF', 'FR6MBond').

        Retourne:
        ---------
        - risk_factor : objet (Equity ou Rate)
            Le facteur de risque construit en fonction des données.

        Exceptions:
        -----------
        - NotImplementedError : si le nom du type n'est pas géré.
        """
        if data_name in ['CAC40', 'TTEF']:
            risk_factor = self.build_equity(data_name)
        elif data_name == 'FR6MBond':
            risk_factor = self.build_rate(data_name)
        else:
            raise NotImplementedError(f"Type de données non supporté : {data_name}")

        return risk_factor
