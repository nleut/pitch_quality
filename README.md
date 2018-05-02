# pitch_quality

This repository contains the code and datasets to view the pitch quality dashboard. 

To run the program and view the dashboard, enter the command 'bokeh serve --show pitch_quality.py' in the repository directory. 
# Contents 
pitch_quality.py: Bokeh code for running dashboard program and plotting data 

pitch_confidence.ipynb: Jupyter notebook for creating pitch quality dataset and some early Bokeh graphs

csv files: various data sources for generating pitch_quality.csv and pitcher_stats.csv, which are used for the plots

# Requirements 
Bokeh version 0.12.15 

Pandas version 0.20.1

# Description (below in progress for final submission) 
The pitch quality statistic is meant to display how effective a pitcher is at throwing certain types of pitches. The statistic takes into account the result of every pitch thrown to determine the effect it has on the game and how effective the pitcher is at throwing it. 

# Data Source
The primary data source for this project was the PITCHf/x dataset from 2017 and part of the 2018 season. Data was gathered using a slightly modified version of this web scraper: https://github.com/johnchoiniere/pfx_parser. The main feature used from this dataset was the pitch type field, which is generated from the MLBAM neural network. Because these pitch types are determined using a neural network classifier, not all pitch types can be classified accurately. The classifier also includes a confidence number on how confidently the pitch was classified, so only pitches with higher confidence ratings were used for analysis. 

# Similar Statistics 
- Brooks Baseball has analysis based on pitch type, but does not aggregate a single statistic for each pitch type similar to the pitch quality statistic 
http://www.brooksbaseball.net/outcome.php?player=641771&b_hand=-1&gFilt=&pFilt=FA|SI|FC|CU|SL|CS|KN|CH|FS|SB&time=month&minmax=ci&var=pcount&s_type=2&startDate=03/30/2007&endDate=05/01/2018
