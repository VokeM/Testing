"""
Created on Mon Dec 14 10:34:17 2020
@author: Voilet Pince
"""


from flask import Flask
app= Flask(__name__)
@app.route('/')
def index():
  return "<h1>Welcome to CodingX</h1>"