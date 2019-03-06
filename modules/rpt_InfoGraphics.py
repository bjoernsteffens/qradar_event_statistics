#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ========================================================
# Function
#   Create InfoGraphics based on data frames
#
# Date/Version/Comment
#   2019-02-22 1.1 First Version
#   2019-03-04 1.2 Code verified for python v3
#
# Author
#   bjoern steffens - bjs@ch.ibm.com
#
# Python Version
#   3.7.1
#
# QRadar API Version
#   9.1 | 10.0 (v7.3.2)
#
# Input
#   See each function for required input
#
# Output
#   An image object
# ========================================================

import matplotlib.pyplot as plt
import numpy as np
from pylab import figure


def rpt_StackedAreaChart(df_Input, rpt_Title, str_ColumnLabelY, str_ColumnLabelX, str_ColumnValueY):
              
    # ========================================================
    # Input
    #   1. The Data frame to be processed
    #
    #   2. The title for the InfoGraphics
    #
    #   3. The column for the Y-Axis data series
    #
    #   4. The column for the X-Axis data points
    #
    #   5. The colimn with the values to plot
    #
    # Ouput
    #   A data frame with the wrangled data
    # ========================================================

    # wrangle the dataframe
    df_Tmp = df_Input.pivot(index=str_ColumnLabelX, columns=str_ColumnLabelY, values=str_ColumnValueY)
    
    # ========================================================
    # Fix data problem with nan for observations leading
    # to dips in the chart
    df_Tmp.fillna(0, inplace = True)

    fig = figure()
    
    _ = plt.style.use('seaborn-darkgrid') 
    _ = plt.title(rpt_Title, loc='left', fontsize=14, fontweight=0, color='blue')
    _ = plt.xticks(np.arange(0, len(df_Tmp.index), 5.0))
    _ = plt.tick_params(axis='both', labelsize=8)
    _ = plt.ylabel(str_ColumnValueY, fontsize=5, color = 'grey') 
    _ = plt.stackplot(df_Tmp.index.values, df_Tmp.values.T)
    _ = plt.legend(df_Tmp.columns,loc=9, bbox_to_anchor=(0.5, -0.07), ncol=2, fontsize=6)

    fig.tight_layout()
    return fig
    
    # ========================================================
    # END rpt_StackedAreaChart()