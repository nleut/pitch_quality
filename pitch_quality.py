from bokeh.io import output_file, show
from bokeh.layouts import widgetbox, layout, row, column
from bokeh.models.widgets import Select
from bokeh.plotting import figure
from bokeh.io import show, output_notebook
from bokeh.models import ColumnDataSource, NumeralTickFormatter
from bokeh.plotting import figure, curdoc
from bokeh.palettes import Spectral11
from bokeh.transform import factor_cmap
from bokeh.server.server import Server
from bokeh.core.properties import value
import pandas as pd
import numpy as np

def make_dataset(name):
    dfPlot = dfOut.loc[dfOut["mlb_name"] == name].drop_duplicates()
    name = np.array_str(dfPlot["mlb_name"].unique())[2:-2]
    pitches = dfPlot["pitch_type"].unique()
    source = ColumnDataSource(dfPlot)
    return source,pitches 

def make_plot_qual(data, name, pitches,all_pitches): 
    
    p = figure(x_range=pitches, plot_height=250,plot_width = 400, toolbar_location=None, title= name, 
           y_axis_label = "Pitch Quality", x_axis_label = "Pitch Type")

    p.vbar(x='pitch_type', top='quality', width=0.9, source=data,line_color='white',
       fill_color=factor_cmap('pitch_type', palette=Spectral11, factors=all_pitches))
    return p

def make_plot_breakdown(data,pitches):
    pcts = ["ball_pct","foul_pct","strike_pct","in_play_pct"]
    headers = ["Ball %","Foul %","Strike %","In Play %"]
    colors = ["#c9d9d3", "#718dbf", "#e84d60","#99d594"]
    
    p = figure(x_range=pitches,y_range = (-.2,1), plot_height=250,plot_width = 400, title="Breakdown",
            toolbar_location=None, tools="")
    p.vbar_stack(pcts, x='pitch_type', width=0.9, source=data,color = colors, 
            legend = [value(x) for x in headers])

    p.legend.location = 'bottom_right'
    p.legend.orientation = 'horizontal'
    p.legend.padding= 2
    p.yaxis[0].formatter = NumeralTickFormatter(format="0.0%")  
    return p
    
def function(attr,old,new):
    print(select.value)

def update(attr,old,new): 
    name = select.value
    new_src,pitches = make_dataset(name)
    p1_qual.x_range.factors = list(pitches)
    p1_qual.title.text = name
    p1_break.x_range.factors = list(pitches)
    data.data.update(new_src.data)

def update2(attr,old,new): 
    name = select2.value
    new_src,pitches = make_dataset(name)
    p2_qual.x_range.factors = list(pitches)
    p2_break.x_range.factors = list(pitches)
    p2_qual.title.text = name
    data2.data.update(new_src.data)


dfOut = pd.read_csv("pitch_quality.csv")
all_pitches = dfOut["pitch_type"].unique()
   
name = "Zack Wheeler"
name2 = "Zack Greinke"
data, pitches = make_dataset(name)
data2,pitches2 = make_dataset(name2)
p1_qual = make_plot_qual(data,name,pitches,all_pitches)
p2_qual = make_plot_qual(data2,name2,pitches2,all_pitches)
p1_break = make_plot_breakdown(data,pitches)
p2_break = make_plot_breakdown(data2,pitches2)

#output_file("select.html")
#show(row(p1,p2))

pitchers = dfOut["mlb_name"].drop_duplicates().tolist()
pitchers.sort(key=str.lower)

select = Select(title="Pitcher:", value="", options= pitchers)
select.on_change('value',update)

select2 = Select(title="Pitcher:", value="", options= pitchers)
select2.on_change('value',update2)

layout = layout([[column(widgetbox(select), row(p1_qual,p1_break))], 
    [column(widgetbox(select2), row(p2_qual,p2_break))]])

curdoc().add_root(layout)


