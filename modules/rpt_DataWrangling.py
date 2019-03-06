#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ========================================================
# Function
#   Encapsulated Data Frame Transformations
#
# Date/Version/Comment
#   2019-02-15 1.1 First Version
#   2019-02-22 1.2 Testing with v7.3.2
#   2019-03-04 1.3 Code verified for python v3
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
#   Typically a dataframe but depends on the function
# ========================================================

def rpt_TopX(df_Input, str_ColumnLabelY, str_ColumnLabelX, str_ColumnValueY, val_TopX):
              
    # ========================================================
    # Input
    #   1. The Data frame to be processed
    #
    #   2. The column label that should be grouped on and plotted
    #
    #   3. The column for the X-Axis, typically a Timestamp
    #      value
    #
    #   4. The column label having the value that should
    #      be aggregated 
    #
    #   5. The slicer where to cut the Top records.
    #      Everything else will be bucketed in to "other"
    #
    # Ouput
    #   A data frame with the wrangled data
    # ========================================================
    
    df_Wrangle = df_Input.copy(deep = True)
    
    # ========================================================
    # Group the Data Frame on df_Column and find the Top X
    # entries first
    
    #str_ColumnLabelY = 'Category'
    #str_ColumnLabelX = 'Timestamp'
    #str_ColumnValueY = 'Events'
    #val_TopX = 5
    
    df_Tmp = df_Wrangle.groupby([str_ColumnLabelY])[str_ColumnValueY].sum().reset_index().sort_values(str_ColumnValueY, ascending=False)
    #print df_Tmp.tail(len(df_Tmp.index)-val_TopX)
    #print df_Tmp
    
    # ========================================================
    # These are the ones we want to rename to "other" and
    # "bucket" into everything else than val_TopX
    df_Tmp = df_Tmp.tail(len(df_Tmp.index)-val_TopX)
    
    # ========================================================
    # Replace these values with "other"
    for row in df_Tmp[str_ColumnLabelY]:
        #print row
        #print df_Wrangle[df_Wrangle[str_ColumnLabelY] == row].Category
        df_Wrangle.loc[df_Wrangle[str_ColumnLabelY] == row, str_ColumnLabelY] = 'Other'
        #print df_Wrangle[df_Wrangle[str_ColumnLabelY] == 'Other'].Category
    
    #df_Wrangle[df_Wrangle['Category'] == 'Firewall Deny'].Category
    #df_Wrangle.loc[df_Wrangle['Category'] == 'Firewall Deny','Category'] = 'Other'
    #df_Wrangle[df_Wrangle['Category'] == 'Other'].Category

    # ========================================================
    # Group on rpt_ColumnLabelY, rpt_ColumnLabelX 
    df_Tmp = df_Wrangle.groupby([str_ColumnLabelY,str_ColumnLabelX], as_index = False).sum()
    
    # ========================================================
    # Stick the wrangled results in a CSV
    #df_Tmp.to_csv('./rpt_EventStats_wrangled.csv', sep=',', encoding='utf-8')
    
    #return wrangled data
    return df_Tmp

    # ========================================================
    # END rpt_TopX()