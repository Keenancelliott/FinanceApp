import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import glob

def GetData(filepath):
    cc = []
    for filename in glob.glob(filepath+'/*.csv'):
        dat = pd.read_csv(filename, header = None)
        cc.append(dat)
    ccDat = pd.concat(cc, ignore_index=True)
    return ccDat

def CleanTDdata(data):
    data.columns = ["Date", "Transaction", "AmountPos", "AmountNeg", "TotalBal"]
    data['Date'] = pd.to_datetime(data['Date'])
    #data['Date'] = data['Date'].date
    #data.Date = pd.DatetimeIndex(data.Date,errors='coerce').strftime("%m/%d/%Y")
    data['weekday'] = data['Date'].dt.day_name()
    data['year'] = pd.DatetimeIndex(data['Date']).year
    data['month'] = pd.DatetimeIndex(data['Date']).month
    data['day'] = pd.DatetimeIndex(data['Date']).day
    data = data.sort_values(by=['Date'])
    return data

def RecurringTransactions(data):
    dupes = data[data.duplicated(subset = ["Transaction", 'day', "AmountPos"], keep = False)]
    Recurring = dupes.loc[dupes.duplicated(subset = ["Transaction", "month"], keep = False) == False].dropna(subset = ["AmountPos"]).drop_duplicates("Transaction", keep = 'last')
    Recurring = Recurring.rename({'AmountPos':'Monthly Cost', 'Date': 'Recent Charge Date'}, axis='columns').drop(['AmountNeg', 'TotalBal', 'weekday','year', 'month', 'day'], axis=1)
    Recurring = Recurring.reset_index(drop=True)
    Recurring.index = range(1, len(Recurring)+1)
    return Recurring

def process_uploaded_data():
    current_directory = os.getcwd()
    UPLOAD_DIRECTORY = current_directory + "/app_uploaded_files"
    ccDatRaw = GetData(UPLOAD_DIRECTORY)
    ccDat = CleanTDdata(ccDatRaw)
    ReTrans = RecurringTransactions(ccDat)
    DailyCounts = ccDat['weekday'].value_counts()
    TransData = ccDat[["Date", "Transaction","AmountPos", "AmountNeg", "TotalBal"]]
    #TransData['TransactionType'] = np.nan

    return ccDat, ReTrans, DailyCounts, TransData