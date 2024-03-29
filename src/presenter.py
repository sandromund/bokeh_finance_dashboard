import pandas as pd

from src.model import Model
from src.view import View


class Presenter:

    def __init__(self, input_csv_path, model: Model, view: View):
        self.path = input_csv_path
        self.data = pd.read_csv(self.path, encoding="ISO-8859-1", sep=";")
        self.model = model
        self.view = view

    def create_report(self):
        data = self.model.filter_columns(self.data)
        data = self.model.preprocess_data(data)
        data = self.model.add_spending_label(data)

        self.view.add_table_plot(data)
        # self.view.add_table_plot(self.model.get_income_by_month(data))
        self.view.add_pie_chart(self.model.get_income_by_month(data=data), map_months=True, title="Income per month")
        self.view.add_pie_chart(self.model.get_spending_by_month(data), map_months=True, title="Spending per month")
        self.view.add_pie_chart(self.model.get_spending_by_label(data), title="Spending by group")

        self.view.add_bar_chart(self.model.get_spending_by_month_and_label(data))

        self.view.show()
