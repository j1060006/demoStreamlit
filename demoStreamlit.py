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
syb = ['SPY', 'QQQ', 'DIA', 'IWM']
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
    df['logReturn'] = df['logReturn'].fillna(0)
    
    avg = df['logReturn'].mean() * 252 * 100
    std = np.sqrt(252) * np.std(df['logReturn']) * 100
    mdd = df['DrowDown'].min()
    res_col_left, res_col_mid,  res_col_right= st.columns(3)
    res_col_left.metric('平均年化報酬率', value="{} %".format(avg.round(2)))    
    res_col_mid.metric('平均年化波動率', value="{} %".format(std.round(2)))    
    res_col_right.metric('持倉期間最大拉回 / 股', value="{} USD".format(mdd.round(2)))    

    df = df.round(2)

    st.write(df)

    # df.reset_index(drop=False, inplace=True)
    # df['Date'] = [dt.datetime.combine(i, dt.datetime.min.time()) for i in df['Date']]    
    # st.line_chart(df, x='Date', y=['Close', 'Adj Close'])

    options ={
        'title':{'text': str(stockId), }, 
        'tooltip':{}, 
        'xAxis':{'type': 'category', 'data':[str(i) for i in df.index], }, 
        # 'yAxis':[{'type':'value', 'position':'left'}, {'type':'value', 'position':'right'}], 
        'yAxis':[{'type':'value', }], 
        'series':[
            # {'data':[i for i in df['Close']], 'type':'line', 'yAxisIndex':0},
            # {'data':[i for i in df['DrowDown']], 'type':'line', 'areaStyle':{}, 'yAxisIndex':1}    
            {'data':[i for i in df['Adj Close']], 'type':'line', }, 
            {'data':[i for i in df['DrowDown']], 'type':'line', 'areaStyle':{}, }
        ]
    }
    
    # options = {
    # "xAxis": {
    #     "type": "category",
    #     "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    # },
    # "yAxis": {"type": "value"},
    # "series": [
    #     {"data": [820, 932, 901, 934, 1290, 1330, 1320], "type": "line"}
    # ],
    # }
    st_echarts(options=options)


    # chart = st.line_chart(np.array([[df.loc[df.index[0], 'Close']]]))
    # for i in range(1, df.shape[0]):
    #     chart.add_rows(np.array([[df.loc[df.index[i], 'Close']]]))
    #     time.sleep(0.05)





# You can use a column just like st.sidebar:
# bar = st.progress(0, "{}".format("0" + "%"))
# for i in range(100):
#     time.sleep(0.1)
#     i = i + 1
#     bar.progress(i, '{}'.format(str(i) + "%"))    
    

