# -*- coding: utf-8 -*-

# ========================================================
# Function
#   This python script create a cvs file with all
#   the configured regex custom properties on the 
#   QRadar Console
#
# Date/Version/Comment
#   2019-02-07 1.1 First Version
#   2019-03-04 1.2 Code verified for python v3
#   2019-03-06 1.3 Adding MS PPT features
#
# Author
#   bjoern steffens - bjs@ch.ibm.com
#
# Python Version
#   3.7.1
#
# QRadar API Version
#   9.1 | 10.0
#
# Input
#   Please configure the qr_Console and qr_Token
#   variables before running the script and create
#   the saved searches and global views needed
#
# Output
#   rpt_EventStats.csv
# ========================================================

# ========================================================
# Load the required libraries
import os,sys
import requests
import json
import pandas as pd

# ========================================================
# Load code developed by the author
from modules.api_client import *
from modules.rpt_DataWrangling import *
from modules.rpt_InfoGraphics import *
from modules.rpt_BuildSlides import *

# ========================================================
# Global variables
qr_Console      = 'https://192.168.12.100/api'
qr_Token        = '77222e7d-c4d9-4454-a522-fddf328511d7'
#qr_Console      = 'https://YOUR_QR_CONSOLE_IP/api'
#qr_Token        = 'YOUR_AUTHORISED_SERVICE_TOKEN'
qr_SavedSearch  = 'rpt_EventStats'
rpt_Category    = 'NORMAL'          # { NORMAL (Minute data) | HOURY | DAILY }
rpt_Period      = 'last 30 Minutes' # last X { minutes | hours | days }

# ========================================================
# Fetch data from a GLOBALVIEW
df_EventStats = api_Fetch_GlobalView(qr_Console, 
                                     qr_Token, 
                                     qr_SavedSearch, 
                                     rpt_Category, 
                                     rpt_Period)

# ========================================================
# Stick the original result set in a CSV
df_EventStats.to_csv('./data/rpt_EventStats_Raw.csv', sep=',', encoding='utf-8')

# ========================================================
# Wrangle the data dynamically
df_EventStats = rpt_TopX(df_EventStats, "Category", "Timestamp", "Events", 5)

# ========================================================
# Stick the wrangled result set in a CSV
df_EventStats.to_csv('./data/rpt_EventStats_Wrangled.csv', sep=',', encoding='utf-8')

# ========================================================
# Create the infoGraphics
img = rpt_StackedAreaChart(df_EventStats, 
                           'Saved Search ' + qr_SavedSearch + ' ' + rpt_Period, 
                           'Category', 
                           'Timestamp', 
                           'Events')
  
# ========================================================
# Save the infoGraphics if we want to use it elsewhere
img_FileName = './images/rpt_EventStats.png'
img.savefig(img_FileName, dpi = 300, bbox_inches = 'tight')
  
# ========================================================
# Place the image on a slide
buildSlide(img_FileName)
