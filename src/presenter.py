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
        data = self.model.filter_columns(self.data)
        data = self.model.preprocess_data(data)

        self.view.add_table_plot(data)
        # self.view.add_table_plot(self.model.get_income_by_month(data))
        self.view.add_pie_chart(self.model.get_income_by_month(data=data), title="Income per month")
        self.view.add_pie_chart(self.model.get_spending_by_month(data), title="Spending per month")

        self.view.show()
