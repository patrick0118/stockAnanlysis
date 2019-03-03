import tushare as ts
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import threading
import time

# mode='all'全量获取，
# mode='inc'增量获取，获取该目录下已经存在的文件，并且增量获取数据后将两个合并
def getKData(ktypelist=['D', '30'], stock_code_list=None, threadname=None, start='2013-01-01', mode='all'):
    print("%s is starting to run \n" % threadname)  # 线程开始
    # 开始下载，获取对应股票的数据，并保存在本地文件中,
    n = 0
    starttime = time.time()
    for code in stock_code_list:
        # 创建保存的文件根目录
        path = 'D:/stockdata/' + code + '/'
        # 创建文件夹，每个code保存一个子目录
        try:
            os.makedirs(path)
        except:
            # print("path already exist")
            pass

        # 根据不同的ktype获取对应的数据并且保存下来
        for ktype in ktypelist:
            filename = 'D:/stockdata/' + code + '/' + code + '_' + ktype + '.csv'
            df = ts.get_k_data(code, ktype=ktype, start=start)
            # 增量模式的时候需要进行处理
            if mode == 'inc':
                dfold = pd.read_csv(filename, index_col=0)
                # print(dfold)
                df = df.append(dfold)
                # print(df)
                df.drop_duplicates(subset='date', keep='last', inplace=True)
                # print(df)

            # 保存到csv文件中
            df.to_csv(filename, mode='w', float_format='%.3f', index_label='Index')

        # if get 100, print log
        n = n + 1
        if n % 100 == 0:
            print('%s finish total is %d, last 100 cost %d' % (threadname, n, time.time() - starttime))
            starttime = time.time()
    # 打印该线程已经完成
    print('%s is finished' % threadname)


def getAllInitData():
    ###获取股票代码列表
    stock_info = ts.get_stock_basics()
    code_list = stock_info.index.tolist()
    # 制定下载的Ktype  D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟
    ktypelist = ['D', '30', 'W', 'M']

    threadnum = 10
    # 创建多线程下载
    step = 3500 / threadnum
    for i in range(threadnum):
        start = int(i * step)
        end = int((i + 1) * step)
        # 将每个线程处理的code的范围确定下来
        if i == threadnum - 1:
            codelist = code_list[start:]
        else:
            codelist = code_list[start:end]
        # _thread.start_new_thread(getKData, (ktypelist, codelist, "Thread %s" % i))
        # getKData(ktypelist=ktypelist,stock_code_list=codelist,threadname="Thread %s" % i)
        my_thread = threading.Thread(target=getKData, args=(ktypelist, codelist, "Thread %s" % i))
        my_thread.start()


def incGetAllData(startDate='2013-01-01'):
    ###获取股票代码列表
    stock_info = ts.get_stock_basics()
    code_list = stock_info.index.tolist()
    # 制定下载的Ktype  D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟
    ktypelist = ['D', '30', 'W', 'M']

    threadnum = 10
    # 创建多线程下载
    step = 3500 / threadnum
    for i in range(threadnum):
        start = int(i * step)
        end = int((i + 1) * step)
        # 将每个线程处理的code的范围确定下来
        if i == threadnum - 1:
            codelist = code_list[start:]
        else:
            codelist = code_list[start:end]
        # _thread.start_new_thread(getKData, (ktypelist, codelist, "Thread %s" % i,startDate,'inc'))
        getKData(ktypelist=ktypelist, stock_code_list=codelist, threadname="Thread %s" % i, start=startDate, mode='inc')


# incGetAllInitData(startDate='2018-04-02')
getAllInitData()
