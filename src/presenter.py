import pandas as pd
from src.view import View
from src.model import Model


class Presenter:

    def __init__(self, input_csv_path, model: Model, view: View):
        self.path = input_csv_path
        self.data = pd.read_csv(self.path, encoding="ISO-8859-1", sep=";")
        self.model = model
        self.view = view

    def create_report(self):
        self.view.add_table_plot(self.model.filter_columns(self.data))
        self.view.show()
