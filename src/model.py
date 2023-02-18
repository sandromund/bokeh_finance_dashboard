import pandas as pd
pd.options.mode.chained_assignment = None


class Model:

    def __init__(self):
        self.filters = ['Mandatsreferenz', 'Glaeubiger ID', 'Kundenreferenz (End-to-End)',
                        'Sammlerreferenz', 'Lastschrift Ursprungsbetrag', 'Auslagenersatz Ruecklastschrift',
                        'BIC (SWIFT-Code)', 'Waehrung', 'Info', 'Valutadatum']
        self.date = "Buchungstag"
        self.amount = "Betrag"

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
