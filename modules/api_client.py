#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# ========================================================
# Function
#   Encapsulated QRadar API Calls
#
# Date/Version/Comment
#   2019-01-10 1.1 First Version
#   2019-01-11 1.2 Adding log source type call
#   2019-02-07 1.3 Adding fetching a GLOBALVIEW
#   2019-02-22 1.4 Verification with v7.3.2
#   2019-03-04 1.5 Code modified for python v3
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

# ========================================================
# Load the required libraries
import os,sys,io
import datetime
import requests
import json
import pandas as pd


def api_Fetch_GlobalView(qr_Console, qr_Token, qr_SavedSearch, rpt_Category, rpt_Period):
      
    # ========================================================
    # Input
    #   1. The QRadar http address for the api. See main script 
    #   for an example
    #
    #   2. The QRadar services token for the API authenticaion
    #   and access. 
    #
    #   3. The name of the saved search to fetch from the
    #      GLOBALVIEW. See ../rpt_EventStats.aql for details
    #
    #   4. The aggregation type to fetch
    #      { NORMAL | DAILY | MONTHLY } 
    #
    #   5. Time window
    #      { last x minutes | last x hours | last x days }
    #
    # Ouput
    #   A data frame with the data requested
    # ========================================================
   
    # ========================================================
    # Prepare the API Call
    headers = {"Accept" : "application/json" } 
    headers["Content-Type"] = 'application/json'
    auth = {"SEC" : qr_Token}
    headers.update(auth)
    
    # ========================================================
    # 1. Launch the "saved search" and grab the cursor id    
    qr_query = "select * from GLOBALVIEW('" + qr_SavedSearch + "','" + rpt_Category + "') " + rpt_Period
    data     = {'query_expression': qr_query}
    api_URL   = qr_Console + '/ariel/searches'
    
    try:
        req_Data = requests.post(api_URL, headers = headers, 
                                 params = data, 
                                 verify = False,
                                 timeout = 2)
        req_Data.raise_for_status()
        
    except requests.exceptions.HTTPError as err:
        print ("\nThe https request failed\n\n" + format(err) + "\n\n")
        sys.exit(1)
    
    # ========================================================
    # 2. Grab the request ID created for the data
    req_ID = req_Data.json()['search_id']
    
    # ========================================================
    # 3. Establish if the search has finised
    api_URL = qr_Console + "/ariel/searches/" + req_ID
    req_Status = requests.get(api_URL, 
                              headers = headers, 
                              verify = False).json()['status']
    #print (req_Status)
    while req_Status != 'COMPLETED' :
        req_Status = requests.get(api_URL, 
                                  headers = headers, 
                                  verify = False).json()['status']    
        #print (req_Status)
    
    # ========================================================
    # 4. Grab the data
    headers = {"Accept" : "application/csv" } 
    headers["Content-Type"] = 'application/csv'
    auth = {"SEC" : qr_Token}
    headers.update(auth)
    api_URL = qr_Console + '/ariel/searches/' + req_ID + '/results'
    req_Data = requests.get(api_URL, headers = headers, verify = False)
    
    # ========================================================
    # Transform the csv results returned to a dataframe
    df_GlobalView=pd.read_csv(io.StringIO(req_Data.content.decode('utf-8')))
    
    # ========================================================
    # Convert EPOC milliseconds to date string and rename
    # the columns in the data frame
    df_GlobalView['Time'] = pd.to_datetime(df_GlobalView['Time'], unit='s')
    df_GlobalView['Time'] = df_GlobalView['Time'].apply(lambda t: t.strftime('%y-%m-%d %H:%M'))  

    df_GlobalView.columns = ['Log Source','Event Name','Log Source Type','Category','Timestamp','Events']    

    
    # ========================================================
    # Return the saved search
    return df_GlobalView
    
   # ========================================================
    # END api_Fetch_GlobalView()