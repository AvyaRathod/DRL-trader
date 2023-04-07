# -*- coding: utf-8 -*-
"""angel one api connect

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qmGuy5UhgUFNZx79TqCDoMuVVGsEMe73

### task:
* create watchlist
* add totp verfication
* historic data frame
* filter for NSE equity
* add TA for the stocks

importing lib
"""

!pip install smartapi-python
!pip install websocket-client 
!pip install pyotp

from smartapi import SmartConnect
import requests
import datetime
from datetime import date
import os
import json
import csv
import pandas as pd
import numpy as np
import time
import math
import pyotp

"""Login"""

class login:
  def __init__(self):
      self.__client_id = "A50876433"
      self.__pwd = "1406"
      self.__api = "BubCvEuz"
      self.__token = "Z2D573OIJ2PDHCKD66NMIRVGWY"
      self.obj = None

  def Login(self):
    '''logs into angel one'''
    try:

      self.obj=SmartConnect(api_key=self.__api)
      data = self.obj.generateSession(self.__client_id,self.__pwd,pyotp.TOTP(self.__token).now())
      self.refreshToken= data['data']['refreshToken']
      self.feedToken=self.obj.getfeedToken()
      self.userProfile= self.obj.getProfile(self.refreshToken)
      print(self.userProfile)
    except Exception as e:
      print("Login failed: {}".format(e))

class DataHandling(login):
  def __init__(self):
    super().__init__()

  def initializeTokenMap(self):
    '''gets the token map for all tradeables'''

    url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
    d = requests.get(url).json()
    token_df = pd.DataFrame.from_dict(d)
    token_df['expiry'] = pd.to_datetime(token_df['expiry'])
    token_df = token_df.astype({'strike':float})
    self.token_map = token_df
    print(token_df)

  def getTokenInfo(self,symbol,exch_seg = 'NSE'):
    '''eq_df contains all the details about tradeable eq'''
    df = self.token_map
    if exch_seg == "NSE":
      eq_df = df[(df['exch_seg'] == "NSE") & (df['symbol'].str.contains('EQ')) ]
      return eq_df[eq_df['name'] == symbol]

  def OHLCHistory(self,symbol,token,interval,fdate,todate,exchange="NSE"):
    '''
    gets the candle data for one symbol by doing a single api call
  
    task: 
    -make this function such that we can get data more than the limit of the 
    api(ie 30 days for 1 min data)
    -need to get data for n tickers
    '''
    #try:
    historicParam={
    "exchange": exchange,
    "tradingsymbol": symbol,
    "symboltoken": token,
    "interval": interval,
    "fromdate": fdate, 
    "todate": todate
    }

    #the obj in the line below has to be accessed which aint happening
    self.history = self.obj.getCandleData(historicParam)['data']
    self.history = pd.DataFrame(self.history)

    self.history = self.history.rename(
        columns = {0:"Datetime",1:"open",2:"high",3:"low",4:"close",5:"volume",}
    )
    self.history['Datetime']=pd.to_datetime(self.history['Datetime'])
    print(self.history)
    #except Exception as e:
      #print("Historic Api failed: {}".format(e))

dh = DataHandling()

dh.Login()

dh.initializeTokenMap()

stocks = ['SBIN','SRF','KTKBANK']
Dailydata={}

for ticker in stocks:
   tokendetails = dh.getTokenInfo(ticker).iloc[0]
   symbol = tokendetails['symbol']
   token = tokendetails['token']
   Dailydata[ticker] = dh.OHLCHistory(str(symbol),str(token),"ONE_MINUTE","2021-02-28 00:00","2021-3-31 00:00")









