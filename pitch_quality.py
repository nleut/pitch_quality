from bokeh.io import output_file, show
from bokeh.layouts import widgetbox, layout, row, column
from bokeh.models.widgets import Select, DataTable, TableColumn, Div
from bokeh.plotting import figure
from bokeh.io import show, output_notebook
from bokeh.models import ColumnDataSource, NumeralTickFormatter, HoverTool
from bokeh.plotting import figure, curdoc
from bokeh.palettes import Spectral11
from bokeh.transform import factor_cmap
from bokeh.server.server import Server
from bokeh.core.properties import value
import pandas as pd
import numpy as np

#slice datasets for names and generate list of pitches for that pitcher
def make_dataset(name):
    dfPlot = dfOut.loc[dfOut["mlb_name"] == name].drop_duplicates()
    dfTable = dfStats.loc[dfStats["mlb_name"]== name]
    name = np.array_str(dfPlot["mlb_name"].unique())[2:-2]
    #todo: replace pitch type code with full pitch name 
    pitches = dfPlot["pitch_type"].unique()
    source = ColumnDataSource(dfPlot)
    stats_source = ColumnDataSource(dfTable)
    return source,pitches, stats_source 

#create plot of pitch quality for each pitch type
def make_plot_qual(data, name, pitches,all_pitches): 
    
    p = figure(x_range=pitches, plot_height=250,plot_width = 400, toolbar_location=None, title= name, 
           y_axis_label = "Pitch Quality", x_axis_label = "Pitch Type")

    p.vbar(x='pitch_type', top='quality', width=0.9, source=data,line_color='white',
       fill_color=factor_cmap('pitch_type', palette=Spectral11, factors=all_pitches))

    hover = HoverTool(tooltips=[("Num pitches", "@pitch_count")])
    p.add_tools(hover)
    return p

#create stacked plot of pitch result breakdown 
def make_plot_breakdown(data,pitches):
    pcts = ["ball_pct","foul_pct","strike_pct","in_play_pct"]
    headers = ["Ball %","Foul %","Strike %","In Play %"]
    colors = ["#c9d9d3", "#718dbf", "#e84d60","#99d594"]
    
    hover = HoverTool(tooltips=[("Num pitches", "@pitch_count")])

    p = figure(x_range=pitches,y_range = (-.2,1), plot_height=250,plot_width = 400, title="Breakdown",
            toolbar_location=None, tools="")
    p.vbar_stack(pcts, x='pitch_type', width=0.9, source=data,color = colors, 
            legend = [value(x) for x in headers])

    p.legend.location = 'bottom_right'
    p.legend.orientation = 'horizontal'
    p.legend.padding= 2
    p.yaxis[0].formatter = NumeralTickFormatter(format="0.0%")  
    p.add_tools(hover)
    return p

#create data table to display pitcher stats from 2017  
def make_table(data, name):
    columns = [
        TableColumn(field="ERA", title="ERA"),
        TableColumn(field="IP", title="IP"),
        TableColumn(field = "SO", title = "SO"),
        TableColumn(field = "HR", title = "HR"),
        TableColumn(field = "WHIP", title = "WHIP")
    ]
    data_table = DataTable(source=data, columns=columns, width=300, height=200, index_position = None)
    return data_table

#update callback for first pitcher section 
def update(attr,old,new): 
    name = select.value
    new_src,pitches, stats_src = make_dataset(name)
    p1_qual.x_range.factors = list(pitches)
    p1_qual.title.text = name
    p1_break.x_range.factors = list(pitches)
    data.data.update(new_src.data)
    #data_table1.update()
    stats.data.update(stats_src.data)

#update callback for second pitcher section 
def update2(attr,old,new): 
    name = select2.value
    new_src,pitches, stats_src = make_dataset(name)
    p2_qual.x_range.factors = list(pitches)
    p2_break.x_range.factors = list(pitches)
    p2_qual.title.text = name
    data2.data.update(new_src.data)
    stats2.data.update(stats_src.data)

#read datasets and create list of all pitch types
dfOut = pd.read_csv("pitch_quality.csv")
dfStats = pd.read_csv("pitcher_stats.csv")
all_pitches = dfOut["pitch_type"].unique()

#initialize names for first view
name = "Chris Sale"
name2 = "Zack Greinke"

#generate initial datasets
data, pitches, stats = make_dataset(name)
data2,pitches2, stats2 = make_dataset(name2)

#make plots and tables 
p1_qual = make_plot_qual(data,name,pitches,all_pitches)
p2_qual = make_plot_qual(data2,name2,pitches2,all_pitches)
p1_break = make_plot_breakdown(data,pitches)
p2_break = make_plot_breakdown(data2,pitches2)
data_table1 = make_table(stats,name)
data_table2 = make_table(stats2,name2)

#create list of pitchers 
pitchers = dfOut["mlb_name"].drop_duplicates().tolist()
pitchers.sort(key=str.lower)

#dropdown menu initialization 
select = Select(title="Pitcher:", value="", options= pitchers)
select.on_change('value',update)

select2 = Select(title="Pitcher:", value="", options= pitchers)
select2.on_change('value',update2)

#title divs for tables
div = Div(text = "2017 Stats",height = 10, width = 300)
div2 = Div(text = "2017 Stats",height = 10, width = 300)

#format layout and output
layout = layout([[column(widgetbox(select), row(p1_qual,p1_break,column(div,data_table1)))], 
    [column(widgetbox(select2), row(p2_qual,p2_break,column(div2,data_table2)))]])

curdoc().add_root(layout)


