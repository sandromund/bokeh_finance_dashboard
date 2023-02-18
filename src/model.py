import pandas as pd


class Model:

    def __init__(self):
        self.filters = ['Mandatsreferenz', 'Glaeubiger ID', 'Kundenreferenz (End-to-End)',
                        'Sammlerreferenz', 'Lastschrift Ursprungsbetrag', 'Auslagenersatz Ruecklastschrift',
                        'BIC (SWIFT-Code)', 'Waehrung', 'Info', 'Valutadatum']

    def filter_columns(self, data: pd.DataFrame) -> pd.DataFrame:
        return data.drop(columns=self.filters)
