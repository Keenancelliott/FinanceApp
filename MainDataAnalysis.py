import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import glob
from Functions import GetData, CleanTDdata, RecurringTransactions

cwd = os.getcwd()

ccDatRaw = GetData(cwd+'/app_uploaded_files')
ccDat = CleanTDdata(ccDatRaw)
ReTrans = RecurringTransactions(ccDat)

DailyCounts = ccDat['weekday'].value_counts()


