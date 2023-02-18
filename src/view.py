import bokeh as bk
import pandas as pd
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.plotting import figure, show
from bokeh.layouts import row, column

from bokeh.palettes import Category20c
from bokeh.plotting import figure, show
from bokeh.transform import cumsum
from math import pi
import calendar


class View:

    def __init__(self):
        self.plots = []
        self.months = {index: month for index, month in enumerate(calendar.month_abbr) if month}
        self.table_column = []
        self.pie_column = []

    def add_table_plot(self, data):
        data_table = DataTable(
            columns=[TableColumn(field=Ci, title=Ci) for Ci in
                     data.columns],
            source=bk.models.ColumnDataSource(data=data),
            sizing_mode='stretch_both')
        self.table_column.append(data_table)

    def add_pie_chart(self, series: pd.Series, title="Pie Chart"):
        print(series)
        data = pd.DataFrame()
        data['angle'] = series / series.sum() * 2 * pi
        data['color'] = Category20c[len(series)]
        data["country"] = [self.months.get(i) for i in  series.index]
        data["value"] = [i[0] for i in series.values]

        print(data["value"])

        p = figure(height=350, title=title, toolbar_location=None,
                   tools="hover", tooltips="@country: @value")

        p.wedge(x=0, y=1, radius=0.4,
                start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                line_color="white", fill_color='color', legend_field='country', source=data)

        p.axis.axis_label = None
        p.axis.visible = False
        p.grid.grid_line_color = None
        self.pie_column.append(p)

    def show(self):
        show(column(row(self.table_column),
                    row(self.pie_column), sizing_mode="stretch_both"),)
