from bokeh.models.layouts import Row
from bokeh.layouts import *
from bokeh.models import *
from bokeh.palettes import *
from bokeh.plotting import *
from math import *
from scipy.signal import freqz
import numpy as np
from scipy.signal import zpk2tf
from cmath import *

# prepare the graph figures
system = figure(plot_width=340, plot_height=350,match_aspect=True, x_range=(-1.5,1.5), y_range=(-1.5,1.5),margin=11,
title="Control System", toolbar_location="left")
system.circle(0, 0, radius=1.0, fill_alpha=0,color='green')
system.line((0, 1), (0, 0),color='green')
system.line((0, -1), (0, 0),color='green')
system.line((0, 0), (0, 1),color='green')
system.line((0, 0), (0, -1),color='green')

magnitude= figure( tools=[],title='Magnitude',
plot_width=450, plot_height=250 ,  margin=10, toolbar_location="above")

phase = figure( tools=[],title='Phase',
plot_width=450, plot_height=250, margin=10, toolbar_location="above")

filter = figure(plot_width=340, plot_height=350, match_aspect=True,x_range=(-1.5,1.5), y_range=(-1.5,1.5),margin=15,
title="Custom Filter", toolbar_location="left")
filter.circle(0, 0, radius=1.0, fill_alpha=0,color='green')
filter.line((0, 1), (0, 0),color='green')
filter.line((0, -1), (0, 0),color='green')
filter.line((0, 0), (0, 1),color='green')
filter.line((0, 0), (0, -1),color='green')

phase_filter= figure( tools=['save'],title='Filter Phase',
plot_width=450, plot_height=250, margin=0, toolbar_location="above")



magnitude_source= ColumnDataSource({
    'h':[], 'm':[]
})
magnitude.line(x='h',y='m',source=magnitude_source,color='black',width=1.5)

phase_source= ColumnDataSource({
    'w':[], 'p':[]
})
phase.line(x='w',y='p',source=phase_source, color='black',width=1.5)
conjugate_zeros = ColumnDataSource(data=dict(x_of_zeros_conjugate=[], y_of_zeros_conjugate=[]))

conjugate_zeros_renderer = system.circle(x="x_of_zeros_conjugate", y="y_of_zeros_conjugate",
                                        source=conjugate_zeros,color='red', size=10,legend_label="Zero")
conjugate_zeros_columns = [TableColumn(field="x_of_zeros_conjugate", title="x_of_zeros_conjugate"),
           TableColumn(field="y_of_zeros_conjugate", title="y_of_zeros_conjugate")
           ]
conjugate_zeros_table = DataTable(source=conjugate_zeros, columns=conjugate_zeros_columns, editable=True, height=100)
conjugate_poles = ColumnDataSource(data=dict(x_conj_p=[], y_conj_p=[]))

conjugate_poles_renderer = system.x(x="x_conj_p", y="y_conj_p",
                                    source=conjugate_poles,line_width=3, color='black', size=15,legend_label="Pole")
conjugate_poles_columns = [TableColumn(field="x_conj_p", title="x_conj_p"),
           TableColumn(field="y_conj_p", title="y_conj_p")
           ]
conjugate_poles_table = DataTable(source=conjugate_poles, columns=conjugate_poles_columns, editable=True, height=100)
poles_source = ColumnDataSource(data=dict(x_of_poles=[], y_of_poles=[]))

poles_renderer = system.x(x="x_of_poles", y="y_of_poles", source=poles_source,line_width=3, color='black', size=15)
poles_columns = [TableColumn(field="x_of_poles", title="x_of_poles"),
           TableColumn(field="y_of_poles", title="y_of_poles")
           ]
poles_table = DataTable(source=poles_source, columns=poles_columns, editable=True, height=200)
source_z = ColumnDataSource(data=dict(x_of_zeros=[], y_of_zeros=[]))

zeros_render = system.circle(x='x_of_zeros', y='y_of_zeros', source=source_z, color='red', size=10)
zeros_columns = [TableColumn(field="x_of_zeros", title="x_of_zeros"),
           TableColumn(field="y_of_zeros", title="y_of_zeros")
           ]
zeros_table = DataTable(source=source_z, columns=zeros_columns, editable=True, height=200)

div = Div(text=""" To Delete any point click on it then press backspace""",
width=200, height=100)

poles_filter_source = ColumnDataSource(data=dict(x_of_poles_filter=[], y_of_poles_filter=[]))

poles_filter_renderer = filter.x(x="x_of_poles_filter", y="y_of_poles_filter", source=poles_filter_source,line_width=3, color='black', size=15)
poles_filter_columns = [TableColumn(field="x_of_poles_filter", title="x_of_poles_filter"),
           TableColumn(field="y_of_poles_filter", title="y_of_poles_filter")
           ]
poles_filter_table = DataTable(source=poles_filter_source, columns=poles_filter_columns, editable=True, height=200)

zeros_filter_source = ColumnDataSource(data=dict(x_of_zeros_filter=[], y_of_zeros_filter=[]))

zeros_filter_render = filter.circle(x='x_of_zeros_filter', y='y_of_zeros_filter', source=zeros_filter_source, color='red', size=10)
zeros_filter_columns = [TableColumn(field="x_of_zeros_filter", title="x_of_zeros_filter"),
           TableColumn(field="y_of_zeros_filter", title="y_of_zeros_filter")
           ]
zeros_filter_table = DataTable(source=zeros_filter_source, columns=zeros_filter_columns, editable=True, height=200)

relative_zeros = ColumnDataSource(data=dict(x_of_zeros_relative=[], y_of_zeros_relative=[]))

relative_zeros_renderer = filter.circle(x="x_of_zeros_relative", y="y_of_zeros_relative", source=relative_zeros,color='red', size=10)
relative_zeros_columns = [TableColumn(field="x_of_zeros_relative", title="x_of_zeros_relative"),
           TableColumn(field="y_of_zeros_relative", title="y_of_zeros_relative")
           ]
relative_zeros_table = DataTable(source=relative_zeros, columns=relative_zeros_columns, editable=True, height=200)


relative_poles = ColumnDataSource(data=dict(x_of_poles_relative=[], y_of_poles_relative=[]))

relative_poles_renderer = filter.x(x="x_of_poles_relative", y="y_of_poles_relative", source=relative_poles,line_width=3, color='black', size=15)
relative_poles_columns = [TableColumn(field="x_of_poles_relative", title="x_of_poles_relative"),
           TableColumn(field="y_of_poles_relative", title="y_of_poles_relative")
           ]
relative_poles_table = DataTable(source=relative_poles, columns=relative_poles_columns, editable=True, height=200)

phase_filter_source= ColumnDataSource({
    'x':[], 'y':[]
})

phase_filter.line(x='x',y='y',source=phase_filter_source, color='black',width=3)

LABELS = ["Zero", "Pole"]

radio_group_filter = RadioGroup(labels=LABELS, active=None, width=400)



Zero = []
Pole = []
Zero_filter = []
Pole_filter = []


reset_button_filter = Button(label="Reset The Design", width=300,margin=0)


menu = [("D_filter I", "filter_1"), ("D_filter II", "filter_2"), ("D_filter III", "filter_3"), ("D_filter IV", "filter_4"),("D_filter V", "filter_5")]

dropdown = Dropdown(label="Filters", menu=menu,width=100,margin=0)

LABELS = ["Zero", "Pole"]
radio_group = RadioGroup(labels=LABELS, active=None, width=200)

LABELS = ["Conjugate"]
checkbox_group = CheckboxGroup(labels=LABELS, active=[])

clear_zeros_button = Button(label="Clear Zeros",width=100,margin=0)
clear_poles_button = Button(label="Clear Poles",width=100,margin=0)
reset_button = Button(label="Reset", width=100,margin=0)





