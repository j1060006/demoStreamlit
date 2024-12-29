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

left_column, right_column = st.columns(2)
startDate = left_column.date_input('回測起始日')
endDate = right_column.date_input('回測終止日')

btn = st.button('回測開始')


if btn:
    df = yf.Ticker(stockId).history(start = startDate, end = endDate, interval = '1d', auto_adjust=False)
    df.index = [i.date() for i in df.index]
    df.index.name = 'Date' 
    dd = []
    hh = 0
    for i in range(df.shape[0]):
        if df.loc[df.index[i], 'Adj Close'] > hh:
            hh = df.loc[df.index[i], 'Adj Close']
        dd.append(df.loc[df.index[i],'Adj Close']-hh)
    df.insert(6, 'DrowDown', dd)  
    
    df['logReturn'] = np.log(df['Adj Close'] / df['Adj Close'].shift(1))  
    df['logReturn'] = 0
        
    df['logReturn'] = df['logReturn'].fillna(0)
    
    avg = float(df['logReturn'].mean() * 252 * 100)
    std = float(np.sqrt(252) * np.std(df['logReturn']) * 100)
    mdd = float(df['DrowDown'].min())
    res_col_left, res_col_mid,  res_col_right= st.columns(3)
    res_col_left.metric('平均年化報酬率', value="{} %".format(np.round(avg, 2)))    
    res_col_mid.metric('平均年化波動率', value="{} %".format(np.round(std, 2)))    
    res_col_right.metric('持倉期間最大拉回 / 股', value="{} USD".format(np.round(mdd, 2)))

    df = df.round(2)



    options ={
        'title':{'text': str(stockId), }, 
        'tooltip':{}, 
        'xAxis':{'type': 'category', 'data':[str(i) for i in df.index], }, 
        'yAxis':[{'type':'value', }], 
        'series':[
            {'data':[i for i in df['Adj Close']], 'type':'line', }, 
            {'data':[i for i in df['DrowDown']], 'type':'line', 'areaStyle':{}, }
        ]
    }
    
    st_echarts(options=options) 

    st.write(df)





