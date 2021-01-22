# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 10:40:13 2020

@author: Voilet Pince
"""

import pandas as pd
import flask
from flask import Flask
import joblib
import numpy as np
from flask_cors import CORS
import warnings
import mysql.connector as connection

from collections import defaultdict

try: 
    mydb = connection.connect(host='localhost', database = 'review',user='root', passwd='',use_pure=True)#creating the connection to the database review   
    query = "Select * from review;"#selecting the table review from the database review    
    ds= pd.read_sql(query,mydb)#storing the review table in a Pandas dataframe
    mydb.close() #close the connection
#exception to catch errors and print the errors
except Exception as e:
        mydb.close()
        print(str(e))

warnings.filterwarnings('ignore')

def user(ID):
    df=ds.sort_values('ArtisanID')
    grouped_df = df.groupby('ArtisanID')
    Art=grouped_df.get_group(ID)
    return Art
ID='art02'
Art=user(ID)
print(Art)
