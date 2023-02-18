import bokeh as bk
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.plotting import figure, show
from bokeh.layouts import row


class View:

    def __init__(self):
        self.plots = []

    def add_table_plot(self, data):
        data_table = DataTable(
            columns=[TableColumn(field=Ci, title=Ci) for Ci in
                     data.columns],
            source=bk.models.ColumnDataSource(data=data),
            sizing_mode='stretch_both')
        self.plots.append(data_table)

    def show(self):
        show(row(self.plots))
