import numpy as np

import pandas as pd
import json

pd.options.mode.chained_assignment = None


class Model:

    def __init__(self, spending_dict_path):
        self.filters = ['Mandatsreferenz', 'Glaeubiger ID', 'Kundenreferenz (End-to-End)',
                        'Sammlerreferenz', 'Lastschrift Ursprungsbetrag', 'Auslagenersatz Ruecklastschrift',
                        'BIC (SWIFT-Code)', 'Waehrung', 'Info', 'Valutadatum']
        self.date = "Buchungstag"
        self.amount = "Betrag"
        self.recipient = "Beguenstigter/Zahlungspflichtiger"
        self.purpose = "Verwendungszweck"

        self.spending_dict_path = spending_dict_path
        with open(self.spending_dict_path, 'r') as f:
            self.spending = json.load(f)

    def __classify_by_recipient_and_purpose(self, row):
        for label in self.spending.keys():
            for keyword in self.spending[label]:
                if type(row[self.recipient]) == np.float:
                    continue
                if keyword in row[self.recipient] or keyword in row[self.purpose]:
                    return label
        return np.nan

    def add_spending_label(self, data: pd.DataFrame) -> pd.DataFrame:
        label_list = []
        for index, row in data.iterrows():
            if row[self.amount] >= 0:
                label_list.append("Income")
            else:
                label_list.append(self.__classify_by_recipient_and_purpose(row))
        data["label"] = label_list
        return data

    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        data[self.amount] = data[self.amount].str.replace(",", ".")
        data[self.amount] = pd.to_numeric(data[self.amount])
        data[self.amount] = data[self.amount]
        return data

    def filter_columns(self, data: pd.DataFrame) -> pd.DataFrame:
        return data.drop(columns=self.filters)

    def get_income_by_month(self, data: pd.DataFrame) -> pd.Series:
        data = data[data[self.amount] >= 0]
        data.loc[:, self.date] = pd.to_datetime(data[self.date])
        group = data.groupby(data[self.date].dt.month).sum().round(4)
        return group

    def get_spending_by_month(self, data: pd.DataFrame) -> pd.Series:
        data = data[data[self.amount] < 0]
        data.loc[:, self.date] = pd.to_datetime(data[self.date])
        group = data.groupby(data[self.date].dt.month).sum().round(4)
        return group
