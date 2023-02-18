import calendar
from math import pi

import pandas as pd
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.palettes import Category20c
from bokeh.plotting import figure, show
import random
from bokeh.transform import cumsum


class View:

    def __init__(self):
        self.plots = []
        self.months = {index: month for index, month in enumerate(calendar.month_abbr) if month}
        self.table_column = []
        self.pie_column = []
        self.bar_column = []

    def add_table_plot(self, data):
        data_table = DataTable(
            columns=[TableColumn(field=Ci, title=Ci) for Ci in
                     data.columns],
            source=ColumnDataSource(data=data),
            sizing_mode='stretch_both')
        self.table_column.append(data_table)

    def add_pie_chart(self, series: pd.Series, title="Pie Chart", map_months=False):
        data = pd.DataFrame()
        data['angle'] = series / series.sum() * 2 * pi
        data['color'] = Category20c[len(series)]
        if map_months:
            data["country"] = [self.months.get(i) for i in series.index]
        else:
            data["country"] = series.index
        data["value"] = [i[0] for i in series.values]
        p = figure(height=350, title=title, toolbar_location=None,
                   tools="hover", tooltips="@country: @value")

        p.wedge(x=0, y=1, radius=0.4,
                start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                line_color="white", fill_color='color', legend_field='country', source=data)

        p.axis.axis_label = None
        p.axis.visible = False
        p.grid.grid_line_color = None
        self.pie_column.append(p)

    def add_bar_chart(self, data: pd.DataFrame):

        labels = list(data)
        labels.remove("Month")

        colors = []
        # TODO Better generation of more distinct colors
        r = lambda: random.randint(0, 255)
        for _ in range(len(labels)):
            colors.append('#%02X%02X%02X' % (r(), r(), r()))

        # labels.remove("Month")
        # source = ColumnDataSource(data=data)
        p = figure(title="Spending by month", toolbar_location=None, tools="")
        p.vbar_stack(labels, x='Month', width=0.9, source=data, color=colors,
                     legend_label=labels)

        p.y_range.start = 0
        p.x_range.range_padding = 0.1
        p.xgrid.grid_line_color = None
        p.axis.minor_tick_line_color = None
        p.outline_line_color = None
        p.legend.location = "top_left"
        p.legend.orientation = "horizontal"

        self.bar_column.append(p)

    def show(self):
        show(
            column(
                row(self.table_column, sizing_mode="stretch_both"),
                row(self.pie_column, sizing_mode="stretch_both"),
                row(self.bar_column, sizing_mode="stretch_both")))
