# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 10:34:17 2020

@author: Voilet Pince
"""

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from nltk.tokenize import RegexpTokenizer
from sklearn import metrics
#import pickle
import flask
from flask import Flask
import joblib
import numpy as np
from flask_cors import CORS
import warnings
import pyodbc 

warnings.filterwarnings('ignore')

print('I am a girl')

cnxn = pyodbc.connect("Driver={SQL Server};"
                        "Server=SQL5053.site4now.net;"
                        "Database=DB_A5DF1B_jobcenta;"
                        "uid=DB_A5DF1B_jobcenta_admin;pwd=admin2019")
ds = pd.read_sql_query('select * from ArtisanReviews', cnxn)

app = Flask(__name__)
CORS(app)
@app.route('/sentiment/', methods=['GET'])

def make_prediction():
    if flask.request.method == 'GET':
        ID='03bf12c6-72ee-4fab-8982-585242da2064'
        Art=user(ID)
        X2 = Art['Comment'].values        
        return flask.jsonify(X2)#returning the zeros and ones

def user(userid):
    df=ds.sort_values('ArtisanID')
    grouped_df = df.groupby('ArtisanID')
    Art=grouped_df.get_group(userid)
    return Art

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False,threaded=False)
