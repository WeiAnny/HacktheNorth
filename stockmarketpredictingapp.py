# -*- coding: utf-8 -*-
"""StockMarketPredictingApp.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zEtMhaMjvEm_pJ6VTAyM_u4df2eaRLsa
"""
import math
from pandas_datareader import data as pdr
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential 
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import base64

import plotly.express as px
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import streamlit as st
from datetime import date

import yfinance as yf
yf.pdr_override()

import pickle
#train fuction --> upload to pickle
#convert juypter to python
#access model from pickle file
#save generated img locally + upload


def getStock(stock, startdate, enddate):
  df = pdr.get_data_yahoo(stock, start=startdate, end=enddate)
  data= df.filter(['Close'])
  dataset = data.values
  #get the number of rows to train the model on
  training_data_len = math.ceil( len(dataset)*0.8)
  #scale the data (preprocessing?)
  scaler = MinMaxScaler(feature_range = (0, 1))
  #holds data set that is scaled between 0 and 1
  scaled_data = scaler.fit_transform(dataset)
  train_data = scaled_data[0:training_data_len , :]
  #split the data into x_train and y_train data sets
  x_train = []
  y_train = []
  for i in range(60, len(train_data)):
    x_train.append(train_data[i-60: i,0]) #past values
    y_train.append(train_data[i, 0]) #prediction
  #convert the x_train and y_train to numpy arrays
  x_train, y_train = np.array(x_train), np.array(y_train)
  #reshape the data
  x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
  #build the lstm model
  model = Sequential()
  model.add(LSTM(50, return_sequences = True, input_shape = (x_train.shape[1], 1)))
  model.add(LSTM(50, return_sequences = False))
  model.add(Dense(25))
  model.add(Dense(1))
  #compile the model
  model.compile(optimizer = 'adam', loss = 'mean_squared_error')
  #train the model
  model.fit(x_train, y_train, batch_size = 1, epochs=1)
  #create the testing data set
  test_data = scaled_data[training_data_len - 60:, :]
  #create the data set x_test and y_test
  x_test = []
  y_test = dataset[training_data_len:, :]
  for i in range(60, len(test_data)):
    x_test.append(test_data[i-60:i, 0])
  #convert the data to a numpy array
  x_test = np.array(x_test)
  #reshape the data
  x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1)) # num of samples, num of time steps, close price
  #get the model predicted price values
  predictions = model.predict(x_test)
  predictions = scaler.inverse_transform(predictions)
  #get the root mean squared error
  #rmse = np.sqrt(np.mean(predictions - y_test)**2)
  #plot the data
  train = data[:training_data_len]
  valid = data[training_data_len:]
  valid['Predictions'] = predictions
  #
  filename = 'finalized_model.sav'
  pickle.dump(model, open(filename, 'wb'))


def getPrediction():
  loaded_model = pickle.load(open(filename, 'rb'))
  result = loaded_model.score(X_test, Y_test)
  return result

def

#visualize the closing price history (aka, graph)
#plt.figure(figsize = (16, 8))
#plt.title('Close Price History')
#plt.plot(df['Close'])
#plt.xlabel('Date', fontsize = 18)
#plt.ylabel('Close Price USD ($)', fontsize = 18)
#plt.show


#visiualize the data
plt.figure(figsize = (16,8))
plt.title('Model')
plt.xlabel('Date', fontsize = 18)
plt.ylabel('Close Price USD ($)', fontsize = 18)
plt.plot(train['Close'])
plt.plot(valid[['Close', 'Predictions']])
plt.legend(['Train', 'Val', 'Predictions'], loc = 'lower right')
plt.show()

#show the valid and predicted prices
valid

#lets predict the prices!
#step 1: get the quote
apple_quote = pdr.get_data_yahoo(stock, start="2012-01-01", end="2021-09-16")
#create a new dataframe
new_df = apple_quote.filter({'Close'})
#get the last 60 day closing price values and convert the datafram to an array
last_60_days = new_df[-60:].values
#scale the data to be values between 0 and 1
last_60_days_scaled = scaler.transform(last_60_days)
#create an empty list
X_test = []
#append the past 60 days
X_test.append(last_60_days_scaled)
#convert the x_test data set to a nump array 
X_test = np.array(X_test)
#reshape the data
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
#get the predicted scale price
pred_price = model.predict(X_test)
#undo the scaling
pred_price = scaler.inverse_transform(pred_price)
print(pred_price)

def get_price_history(ticker, sdate, edate):
    data = []
    data = yf.download(ticker, start=sdate, end=edate)
    return (data)

#apple_quote2 =  pdr.get_data_yahoo("MS", start="2021-09-15", end="2021-09-15")
t_aapl = yf.Ticker(stock)
apple_quote2 = get_price_history(t_aapl, "2021-09-17", "2021-09-17")
print(apple_quote2['Close'])

app = JupyterDash(__name__)
app.layout = html.Div([
        html.H1("Stock Market Predictor App")               
        dcc.Graph(id = 'graph'),
        html.Label([])

])

app.run_server(mode = 'external')