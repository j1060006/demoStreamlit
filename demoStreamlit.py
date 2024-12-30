import streamlit as st
import os
import time
import numpy as np
import pandas as pd
import yfinance as yf
import datetime as dt
from matplotlib import pyplot as plt
from streamlit_echarts import st_echarts
import math


st.set_page_config(page_title="Stock Buy & Hold", page_icon="📈")

st.header('繪製個股Buy & Hold策略')
syb = ['SPY', 'QQQ', 'DIA', 'IWM', 'VOO', 'VT', 'VTI', 'TLT', 'SMH', 'BND', 'SOXX', 'VXUS']
stockId = st.selectbox('選擇個股', syb)
initCapital = st.number_input('起始投入資金', min_value=0, step=100)
left_column, right_column = st.columns(2)
startDate = left_column.date_input('回測起始日')
endDate = right_column.date_input('回測終止日')

btn = st.button('回測開始')


if btn:
    df = yf.Ticker(stockId).history(start = startDate, end = endDate, interval = '1d', auto_adjust=False)
    df.index = [i.date() for i in df.index]
    df.index.name = 'Date' 
    
    
    df['logReturn'] = np.log(df['Adj Close'] / df['Adj Close'].shift(1))          
    df['logReturn'] = df['logReturn'].fillna(0)
    df['cumLogReturn'] = df['logReturn'].cumsum(axis=0)
    avg = df['logReturn'].mean() * 252 * 100
    std = np.sqrt(252) * np.std(df['logReturn']) * 100
    

    dd = []
    for i in range(df.shape[0]):
        hh = df.loc[df.index[:i+1], 'logReturn'].max()
        dd.append(df.loc[df.index[i], 'logReturn'] - hh)
    df['DrowDown'] = dd  
    mdd = (df['DrowDown'].min()) * 100    
    df['ProfitLoss'] = initCapital * df['logReturn'].cumsum(axis=0)

    ddc = []
    for i in range(df.shape[0]):
        hhc = df.loc[df.index[:i+1], 'Adj Close'].max()
        ddc.append(df.loc[df.index[i], 'Adj Close'] - hhc)
    df['DrowDownC'] = ddc  


    a1, a2, a3, a4= st.columns(4)
    a1.metric('平均年化報酬率 %', value="{} %".format(np.round(avg, 2)))    
    a2.metric('平均年化波動率 %', value="{} %".format(np.round(std, 2)))    
    a3.metric('持倉期間最大拉回 %', value="{} %".format(np.round(mdd, 2)))
    a4.metric('持倉期間獲利', value="{} %".format(np.round(df.loc[df.index[-1], 'cumLogReturn'] * initCapital, 2)))




    options ={
        'title':{'text': str(stockId), }, 
        'tooltip':{}, 
        'xAxis':{'type': 'category', 'data':[str(i) for i in df.index], }, 
        'yAxis':[{'type':'value', 'position':'left'}, ], 
        'series':[
            {'data':[i for i in df['Adj Close']], 'type':'line', }, 
            {'data':[i for i in df['DrowDownC']], 'type':'line', 'areaStyle':{}, }
        ]
    }
    
    st_echarts(options=options) 

    del df['DrowDownC']
    df = df.round(2)
    st.write(df)





