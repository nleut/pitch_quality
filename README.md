# pitch_quality

This repository contains the code and datasets to view the pitch quality dashboard. 

To run the program and view the dashboard, enter the command 'bokeh serve --show pitch_quality.py' in the repository directory. 
# Contents 
pitch_quality.py: Bokeh code for running dashboard program and plotting data 

pitch_confidence.ipynb: Jupyter notebook for creating pitch quality dataset and some early Bokeh graphs

data: various data sources for generating pitch_quality.csv and pitcher_stats.csv, which are used for the plots. The full PITCHf/x dataset used for creating the plotting data is not included in the repository due to size. 

# Requirements 
Bokeh version 0.12.15 

Pandas version 0.20.1

NumPy version 1.12.1

# Description
The pitch quality statistic is meant to display how effective a pitcher is at throwing certain types of pitches. The statistic takes into account the result of every pitch thrown to determine the effect it has on the game and how effective the pitcher is at throwing it. Currently, there is no statistic available to holistically evaluate how good a pitcher is at throwing different types of pitches. I think a statistic like pitch quality will make it easier to compare a pitchers effectiveness with different types of pitches, or compare between pitchers to see who has better results when throwing certain pitches.

Pitch quality is assigned by giving a score based on the result of the pitch every time a pitcher throws a certain pitch type. The score begins with the basic result of the pitch, assigning values like 0.1 for a called strike or -0.05 for a ball. If the pitch was the final pitch in a plate appearance, a greater weight is assigned to the pitch for the result of the at-bat. For example, a double brings the score down by -2.54, and a strikeout increases the score by 2.2. If runners are in scoring position, the weight is modified by a factor of 1.2 to emphasize how pitch results are more important with runners in scoring position. The pitch quality for a pitch type is calculated as the mean for all individual pitch weights with that type. 

Modifications could be made to the pitch quality statistic for different purposes. For example, a pitcher may want to know which pitch type he can most reliably throw to get a strike with a full count. Seeing quality results based on different situations may be an interesting addition to the statistic. Additionally, it would be interesting to further break the pitch quality results up by the type of batter the pitcher is matching up with. 

# Application 
To visualize how the statistic works and the results for different pitches, I created a Bokeh application that can be run from the command line with Bokeh and Pandas installed and updated. The pitch quality plot in the application shows the the quality of each pitch for the selected pitcher. Hovering over the bar for a certain pitch type will display information about the exact quality score, the MLB average for that pitch type, the number of times the pitcher was recorded throwing that pitch, and the full pitch name. The breakdown plot displays the percentages of each pitch type that were a strike, ball, foul, or in play, to get a sense of how the quality was calculated. For comparison with existing stats, there is also a table that shows selected stats from 2017 for the pitcher. Two pitchers can be compared side by side, and pitchers can be selected from the dropdown menus. 

When the application runs, the terminal will output a DeserializationError whenever a new pitcher is selected from the menu. This is currently a known issue with using DataTables in Bokeh, documented here: https://github.com/bokeh/bokeh/issues/7417. The presence of these errors does not effect the accuracy of results or cause the application to crash. 

# Data Source
The primary data source for this project was the PITCHf/x dataset from 2017 and part of the 2018 season. Data was gathered using a slightly modified version of this web scraper: https://github.com/johnchoiniere/pfx_parser. The main feature used from this dataset was the pitch type field, which is generated from the MLBAM neural network. Because these pitch types are determined using a neural network classifier, not all pitch types can be classified accurately. The classifier also includes a confidence number on how confidently the pitch was classified, so only pitches with higher confidence ratings were used for analysis. Only pitchers with more than 100 pitches thrown were considered for analysis. 

# Similar Statistics 
I was unable to find a comparable statistic available that has the same goals as pitch quality. There are some uses of the PITCHf/x data and pitch type classifications, but they do not focus on evaluating pitch types for each pitcher. 

Brooks Baseball has analysis based on pitch type, but does not aggregate a single statistic for each pitch type similar to the pitch quality statistic. Brooks Baseball has specific statistics available broken down into pitch classifications, including whiff percentages, swing percentages, and batting average against pitches. The data used is slightly different, as they classify each pitch manually rather than using the MLBAM classifier. 
http://www.brooksbaseball.net/outcome.php?player=641771&b_hand=-1&gFilt=&pFilt=FA|SI|FC|CU|SL|CS|KN|CH|FS|SB&time=month&minmax=ci&var=pcount&s_type=2&startDate=03/30/2007&endDate=05/01/2018

Baseball Savant has some advanced graphical analysis divided by pitch types. For each pitcher and batter matchup, they display where hits go, where pitches land over the plate, a breakdown of pitch types thrown against the batter, and a breakdown of hit types.
https://baseballsavant.mlb.com/player_matchup?type=batter&teamPitching=cle&teamBatting=nyy&player_id=545333


