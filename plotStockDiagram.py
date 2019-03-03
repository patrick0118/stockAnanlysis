import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from matplotlib import ticker as mticker
from mpl_finance import candlestick_ochl,candlestick2_ochl
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY,YEARLY
from matplotlib.dates import MonthLocator,MONTHLY
import datetime as dt

fillcolor = '#00ffe8'
facecolor = '#00ffe8'

"""
绘制K线蜡烛图和均线K线图
"""
def plotStockK(data, ax, malist = ['5','10','20']):
    data = data.loc[len(data.index)-200:,:]
    data = data.reindex(columns=['date','open','high','low','close','EMA_5','EMA_10','EMA_20','EMA_30','EMA_60','EMA_120','EMA_250','volume'])

    #画蜡烛图
    candlestick2_ochl(ax, data['open'], data['close'], data['high'], data['low'],
                          width=0.5, colorup='r', colordown='green', alpha=0.6)
    #画均线图
    for n in malist:
        columnName = 'EMA_' + n
        labelText = n + '日均线'
        ax.plot(data[columnName].values, label=labelText)
    #ax.plot(data['EMA_10'].values, label='10 日均线')
    #ax.plot(data['EMA_20'].values, label='20 日均线')

    ax.set_xticklabels(data['date'][::10])
    #设置网格的颜色
    ax.grid(True,color='w')
    #设置边框的颜色
    ax.spines['bottom'].set_color("#5998ff")
    ax.spines['top'].set_color("#5998ff")
    ax.spines['left'].set_color("#5998ff")
    ax.spines['right'].set_color("#5998ff")
    #设置XY轴的颜色
    ax.tick_params(axis='y', colors='w')
    ax.tick_params(axis='x', colors='w')
    #设置Ylabel和label的颜色
    ax.set_ylabel("stock price and volume")
    ax.yaxis.label.set_color("r")

    return ax
"""
    #绘制交易量
    volumeMin = 0
    ax1v = ax.twinx()
    ax1v.grid(False)
    #设置为浅蓝色
    ax1v.fill_between(data['date'].values, volumeMin, data['volume'], facecolor='#00ffe8',alpha=.4)
    ax1v.axes.yaxis.set_ticklabels([])

    ###Edit this to 3, so it's a bit larger
    ax1v.set_ylim(0, 3 * data.volume.values.max())
    ax1v.spines['bottom'].set_color("#5998ff")
    ax1v.spines['top'].set_color("#5998ff")
    ax1v.spines['left'].set_color("#5998ff")
    ax1v.spines['right'].set_color("#5998ff")
    ax1v.tick_params(axis='x', colors='w')
    ax1v.tick_params(axis='y', colors='w')
"""

"""
绘制MACD图
"""
def plotStockMACD(data, ax):
    data = data.loc[len(data.index)-200:,:]
    data = data.reindex(columns=['date','open','high','low','close','dif','dea','macd'])

    #画均线图
    ax.plot(data['dif'].values,'w',label='dif',lw=1)
    ax.plot(data['dea'].values, 'y',label='dea',lw=1)
    ax.fill_between(data['date'].values, data['macd'], 0, alpha=0.5, facecolor=fillcolor,edgecolor=fillcolor)

    ax.set_xticks(range(0, len(data['date']), 10))
    ax.set_xticklabels(data['date'][::10])
    #设置网格的颜色
    #ax.grid(True,color='w')
    #设置边框的颜色
    ax.spines['bottom'].set_color("#5998ff")
    ax.spines['top'].set_color("#5998ff")
    ax.spines['left'].set_color("#5998ff")
    ax.spines['right'].set_color("#5998ff")
    #设置XY轴的颜色
    ax.tick_params(axis='y', colors='w')
    ax.tick_params(axis='x', colors='w')
    #设置Ylabel和label的颜色
    ax.set_ylabel("MACD")
    ax.yaxis.label.set_color("r")
    #调整显示角度
    for label in ax.xaxis.get_ticklabels():
        label.set_rotation(45)

def plotStock(data, ax):
    #fig = plt.figure(figsize=(15, 10))
    data.sort_index()
    data.reset_index()
    data.dropna()
    data.index.name = 'date'
    data = data.loc[len(data.index)-200:,:]
    #data['date'] = mdates.date2num(pd.to_datetime(data['date']))

    #data['date'] = mdates.date2num(data['date'].astype(dt.date))
    data = data.reindex(columns=['date','open','high','low','close','EMA_5','EMA_10'])
    #fig = plt.figure()
    #fig = plt.figure(facecolor='#07000d', figsize=(15, 10))
    ax = plt.subplot2grid((6,4), (1,0) ,rowspan=4, colspan=4, facecolor='k')

    candlestick2_ochl(ax, data['open'], data['close'], data['high'], data['low'],
                          width=0.5, colorup='r', colordown='green', alpha=0.6)
    ax.set_xticklabels(data['date'][::10])
    ax.plot(data['EMA_5'].values, label='5 日均线')
    ax.plot(data['EMA_10'].values, label='10 日均线')
    #ax1.set_xticks(range(0,len(data['date']),10))

    #candlestick_ochl(ax1, data.values,width=0.5, colorup='r', colordown='b', alpha=0.6)
    #ax.plot(data['date'].values, data['EMA_5'].values, '#e1edf9', label='5 日均线',lw=1.5)
    #ax.plot(data['date'].values, data['EMA_10'].values, '#4ee6fd', label='10 日均线',lw=1.5)

    ax.grid(True,color='w')
    #ax.xaxis.set_major_locator(mticker.MaxNLocator(10))
    #ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y%m%d'))
    #ax.yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))

    ax.spines['bottom'].set_color("#5998ff")
    ax.spines['top'].set_color("#5998ff")
    ax.spines['left'].set_color("#5998ff")
    ax.spines['right'].set_color("#5998ff")
    ax.tick_params(axis='y', colors='w')
    ax.tick_params(axis='x', colors='w')

    #ax.set_xlabel("Date")
    #ax.xaxis.label.set_color("r")
    ax.set_ylabel("stock price and volume")
    ax.yaxis.label.set_color("r")

    #plt.setp(ax0.get_xticklabels(), visible=False)
    #plt.setp(ax1.get_xticklabels(), visible=False)


    plt.show()