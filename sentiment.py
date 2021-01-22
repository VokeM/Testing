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

#importing the datasets
ds = pd.read_csv("labeledTrainData.tsv", delimiter="\t")
train = ds.drop(['id'], axis=1)

X1 = train['review'].values
y = train['sentiment'].values

token = RegexpTokenizer(r'[a-zA-Z0-9]+')
cv = CountVectorizer(stop_words = 'english', ngram_range = (1,2), tokenizer = token.tokenize).fit(X1)
X = cv.transform(X1)

#splitting gthe dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle= True, random_state=42)

# training our classifier ; train_data.target will be having numbers assigned for each category in train data
clf = MultinomialNB().fit(X_train, y_train)

#pickle.dump(clf,open('NBmodel.pkl','wb'))
#pickle.dump(cv,open('vector.pkl','wb'))

predicted = clf.predict(X_test)
accuracy_score = metrics.accuracy_score(predicted, y_test)
print(str('{:04.2f}'.format(accuracy_score * 100))+'%')

ServerName='SQL5053.site4now.net'
MSQLDatabase='DB_A5DF1B_jobcenta'
username='DB_A5DF1B_jobcenta_admin'
password='admin2019'
#import mysql.connector as connection
import adodbapi
conn = adodbapi.connect("PROVIDER=SQLOLEDB;Data Source={0};Database={1}; \
       trusted_connection=yes;UID={2};PWD={3};".format(ServerName,MSQLDatabase,username,password))
cursor = conn.cursor()

ds = pd.read_sql_query('select * from ArtisanReviews', cursor)
app = Flask(__name__)
CORS(app)
@app.route('/sentiment/', methods=['GET'])

def make_prediction():
    if flask.request.method == 'GET':
        ID='03bf12c6-72ee-4fab-8982-585242da2064'
        Art=user(ID)
        X2 = Art['Comment'].values
        X_new = cv.transform(X2)# building up feature vector of our input
        prediction = clf.predict(X_new) #making predictions
        zeros = int(np.sum(prediction == 0))#counting the number of zeros in the analysis
        ones = int(np.sum(prediction == 1))#counting the number of ones in the analysis
        return flask.jsonify(zeros,ones)#returning the zeros and ones

def user(userid):
    df=ds.sort_values('ArtisanID')
    grouped_df = df.groupby('ArtisanID')
    Art=grouped_df.get_group(userid)
    return Art

if __name__ == '__main__':
    clf = joblib.load("NBmodel.pkl")#loading the already trained model
    cv = joblib.load("vector.pkl")#loading the count vectorizer that will be used to vectorize the new inputs
    app.run(debug=True, use_reloader=False,threaded=False)