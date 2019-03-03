import pandas as pd
import matplotlib.pyplot as plt
import plotStockDiagram as plotStock
import numpy  as np
"""
作者：eyeglasses
链接：https://www.jianshu.com/p/69d5ff78a3e0
来源：简书
简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。
data  股票数据
short,long,mid 是macd的三个参数
"""
def get_macd_data (data, short=0, long=0, mid=0):
    result = pd.DataFrame()
    result['date'] = pd.Series(data['date'])
    if short == 0:
        short = 12
    if long == 0:
        long = 26
    if mid == 0:
        mid = 9

    result['sema'] = pd.Series(data['close']).ewm(span=short).mean()  #计算短期的ema，使用pandas的ewm得到指数加权的方法，mean方法指定数据用于平均
    result['lema'] = pd.Series(data['close']).ewm(span=long).mean()  #计算长期的ema，方式同上
    result.fillna(0, inplace=True)  #填充为na的数据data_dif
    result['dif'] = result['sema']-result['lema']   #计算dif，加入新列
    result['dea'] = pd.Series(result['dif']).ewm(span=mid).mean()  #计算deadata
    result['macd'] = 2*(result['dif']-result['dea'])   #计算macddata
    result.fillna(0, inplace=True)   #填充为na的数据
    # #返回data的三个新列
    return result[['date','dif','dea','macd']]

"""
stock_data 传入的数据
ma_list    分别计算5日、20日、60日的移动平均线
"""
def get_ma_data(stock_data,ma_list=[5, 10, 20,30, 60, 120, 250]):
    result = pd.DataFrame()
    result['date'] = pd.Series(stock_data['date'])
    # 将数据按照交易日期从远到近排序
    #stock_data.sort_values('date', inplace=True)

    # 计算简单算术移动平均线MA - 注意：stock_data['close']为股票每天的收盘价
    #for ma in ma_list:
    #     result['MA_' + str(ma)] = pd.Series(data['close']).rolling(ma).mean()

    # 计算指数平滑移动平均线EMA
    for ma in ma_list:
        result['EMA_' + str(ma)] = pd.Series(data['close']).ewm(ma).mean()

    # 将数据按照交易日期从近到远排序
    #result.sort_values('date', ascending=False, inplace=True)
    return result

"""
计算几个关键时间点的涨跌幅度
开盘涨幅比例：###关注开盘低开，并且还在20日线上的股票的买点
openPosPer:
收盘相对早盘比列：
closePosPer
全天涨幅

"""
def get_pos_per(stock_data):
    result = pd.DataFrame()
    result['date'] = pd.Series(stock_data['date'])

    result['openPosPer'] = np.float64(0)
    result['incPer'] = np.float64(0)
    result['closePosPer'] = np.float64(0)
    for n in range(1, len(stock_data.index)):
        result.at[n , 'openPosPer'] = np.float64(100) * (stock_data.at[n, 'open'] - stock_data.at[n-1, 'close']) / stock_data.at[n-1, 'close']
        result.at[n, 'closePosPer'] = np.float64(100) *(stock_data.at[n, 'close'] - stock_data.at[n, 'open']) / stock_data.at[n, 'open']
        result.at[n, 'incPer'] = np.float64(100) * (stock_data.at[n, 'close'] - stock_data.at[n-1, 'close']) / stock_data.at[n-1, 'close']

    return result

"""
stock_data包含open, close, high, low, EMA_5, EMA10, EMA20, EMA30
计算K线和均线的关系，输出字段包括：####关注上穿多均线的情况
cross5
cross10
cross20
cross30
"""
def get_K_MA_Pos(stock_data):
    result = pd.DataFrame()
    result['date'] = pd.Series(stock_data['date'])
    ###使用DataFrame的列进行比较，返回的是一列的判定结果
    result['cross5'] = np.where( (stock_data['open'] < stock_data['EMA_5']) & (stock_data['close'] > stock_data['EMA_5']), 1, 0)
    result['cross10'] = np.where( (stock_data['open'] < stock_data['EMA_10']) & (stock_data['close'] > stock_data['EMA_10']), 1, 0)
    result['cross20'] = np.where( (stock_data['open'] < stock_data['EMA_20']) & (stock_data['close'] > stock_data['EMA_20']), 1, 0)
    result['cross30'] = np.where( (stock_data['open'] < stock_data['EMA_30']) & (stock_data['close'] > stock_data['EMA_30']), 1, 0)
    return result

"""
talib可以用来计算均值
"""



if __name__ == '__main__':
    filename = 'D:/stockdata/000001/000001_D.csv'
    filenameout = 'D:/stockdata/000001/000001_D_res.csv'
    data = pd.read_csv(filename, index_col=0)
    #print(data)
    data = get_ma_data(data).merge(data,on='date')
    #print(data)
    data = get_macd_data(data).merge(data,on='date')
    #print(data)
    #print(data.columns)
    #data = data.iloc[0:100, 0:9]
    #print(data[['date','close','EMA_5','macd']])

    data = get_K_MA_Pos(data).merge(data, on='date')
    data = get_pos_per(data).merge(data, on='date')
    print(data)
    data.to_csv(filenameout, mode='w', float_format='%.2f', index=False)

"""
    fig = plt.figure(facecolor='#07000d', figsize=(15, 10))
    = plt.subplot2grid((5, 4), (0, 0), rowspan=4, colspan=4, facecolor='k')
    ax2 = plt.subplot2grid((5, 4), (4, 0), rowspan=1, colspan=4, facecolor='k')
    ax1 = plotStock.plotStockK(data,ax1, ['5','10','20','30','120','250'])
    ax2 = plotStock.plotStockMACD(data, ax2)
    plt.setp(ax1.get_xticklabels(), visible=False)
    plt.suptitle('000001')
    plt.show()
"""