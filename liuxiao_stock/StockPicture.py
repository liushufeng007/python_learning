# 为方便演示, 我们随机生成3列正随机数
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import mplfinance as mpf
import matplotlib.gridspec as gridspec  # 分割子图
import mpl_finance as mpf

import talib
import matplotlib.ticker as ticker #日期刻度定制
from matplotlib import colors as mcolors #渲染顶点颜色格式
from matplotlib.collections import LineCollection,PolyCollection


class StockPicture:
    def __init__(self):
        self.df = 0

        print("stock picture 初始化完成")

    def Show(self):
        pass

    def SavePicture(self,data,path,title,strategy):
        data['open'] = data['开盘_'].astype('float')
        data['high'] = data['最高_'].astype('float')
        data['low'] = data['最低_'].astype('float')
        data['close'] = data['收盘_'].astype('float')
        data['volume'] = data['volume'].astype('float')
        data['dif'] = data['dif'].astype('float')
        data['dea'] = data['dea'].astype('float')
        data['bar'] = data['bar'].astype('float')

        fig = plt.figure(figsize=(20, 12), dpi=100, facecolor="white")  # 创建fig对象


        # 设置外观效果
        plt.rc('font', family='Microsoft YaHei')  # 用中文字体，防止中文显示不出来
        plt.rc('figure', fc='c')  # 绘图对象背景图
        plt.rc('text', c='#800000')  # 文本颜色
        plt.rc('axes', axisbelow=True, xmargin=0, fc='w', ec='#800000', lw=1.5, labelcolor='#800000',
               unicode_minus=False)  # 坐标轴属性(置底，左边无空隙，背景色，边框色，线宽，文本颜色，中文负号修正)
        plt.rc('xtick', c='#d43221')  # x轴刻度文字颜色
        plt.rc('ytick', c='#d43221')  # y轴刻度文字颜色
        plt.rc('grid', c='#800000', alpha=0.9, ls=':', lw=0.8)  # 网格属性(颜色，透明值，线条样式，线宽)
        plt.rc('lines', lw=0.8)  # 全局线宽

        gs = gridspec.GridSpec(4, 1, left=0.08, bottom=0.15, right=0.99, top=0.96, wspace=None, hspace=0,
                               height_ratios=[3.5, 1, 1, 1])
        graph_KAV = fig.add_subplot(gs[0, :])
        graph_VOL = fig.add_subplot(gs[1, :])
        graph_MACD = fig.add_subplot(gs[2, :])
        graph_KDJ = fig.add_subplot(gs[3, :])
        fig.patch.set_facecolor('blue')

        df_stockload = data

        # 绘制K线图
        mpf.candlestick2_ochl(graph_KAV, df_stockload.open, df_stockload.close, df_stockload.high, df_stockload.low,
                              width=0.5,
                              colorup='r', colordown='g')  # 绘制K线走势

        # 绘制移动平均线图
        df_stockload['Ma5'] = df_stockload.close.rolling(
            window=5).mean()  # pd.rolling_mean(df_stockload.close,window=20)
        df_stockload['Ma10'] = df_stockload.close.rolling(
            window=10).mean()  # pd.rolling_mean(df_stockload.close,window=30)
        df_stockload['Ma20'] = df_stockload.close.rolling(
            window=20).mean()  # pd.rolling_mean(df_stockload.close,window=60)
        df_stockload['Ma30'] = df_stockload.close.rolling(
            window=30).mean()  # pd.rolling_mean(df_stockload.close,window=60)
        df_stockload['Ma60'] = df_stockload.close.rolling(
            window=60).mean()  # pd.rolling_mean(df_stockload.close,window=60)
        df_stockload['Ma89'] = df_stockload.close.rolling(
            window=89).mean()  # pd.rolling_mean(df_stockload.close,window=60)

        pd.set_option('display.width', 300)  # 设置字符显示宽度
        pd.set_option('display.max_rows', None)  # 设置显示最大行
        pd.set_option('display.max_columns', 300)  # 设置显示最大列，None为显示所有列

        #print(df_stockload)

        if strategy == 1:
            df_stockload = df_stockload.rename(columns={'close': 'close1','折线数据': 'close' })
            df_stockload['折线'] = df_stockload.close.rolling(window=1).mean()


        #print(df_stockload['折线'])

        graph_KAV.plot(np.arange(0, len(df_stockload.index)), df_stockload['Ma5'], 'green', label='M5', lw=0)
        graph_KAV.plot(np.arange(0, len(df_stockload.index)), df_stockload['Ma10'], 'pink', label='M10', lw=0)
        graph_KAV.plot(np.arange(0, len(df_stockload.index)), df_stockload['Ma20'], 'blue', label='M20', lw=0)
        #graph_KAV.plot(np.arange(0, len(df_stockload.index)), df_stockload['Ma30'], 'pink', label='M30', lw=1.0)
        graph_KAV.plot(np.arange(0, len(df_stockload.index)), df_stockload['Ma89'], 'red', label='M89', lw=0)
        if strategy == 1:
            graph_KAV.plot(np.arange(0, len(df_stockload.index)), df_stockload['折线'], 'black', label='笔', lw=1.5)
            graph_KAV.plot(np.arange(0, len(df_stockload.index)), df_stockload['中枢顶'], 'red', label='中枢上', lw=1.5)
            graph_KAV.plot(np.arange(0, len(df_stockload.index)), df_stockload['中枢底'], 'blue', label='中枢下', lw=1.5)

        if strategy == 1:
            df_stockload = df_stockload.rename(columns={'close': '折线', 'close1': 'close'})

        # 添加网格
        graph_KAV.grid()
        name = title
        graph_KAV.legend(loc='best')
        graph_KAV.set_title(name)
        graph_KAV.set_ylabel(u"价格")
        graph_KAV.set_xlim(0, len(df_stockload.index))  # 设置一下x轴的范围

        # 绘制成交量图
        graph_VOL.bar(np.arange(0, len(df_stockload.index)), df_stockload.volume,
                      color=['g' if df_stockload.open[x] > df_stockload.close[x] else 'r' for x in
                             range(0, len(df_stockload.index))])
        graph_VOL.set_ylabel(u"成交量")
        graph_VOL.set_xlim(0, len(df_stockload.index))  # 设置一下x轴的范围
        graph_VOL.set_xticks(range(0, len(df_stockload.index), 15))  # X轴刻度设定 每15天标一个日期


        macd_dif, macd_dea, macd_bar = talib.MACD(df_stockload['close'].values, fastperiod=12, slowperiod=26,
                                                  signalperiod=9)
        graph_MACD.plot(np.arange(0, len(df_stockload.index)), macd_dif, 'red', label='macd dif')  # dif
        graph_MACD.plot(np.arange(0, len(df_stockload.index)), macd_dea, 'blue', label='macd dea')  # dea

        bar_red = np.where(macd_bar > 0, 2 * macd_bar, 0)  # 绘制BAR>0 柱状图
        bar_green = np.where(macd_bar < 0, 2 * macd_bar, 0)  # 绘制BAR<0 柱状图
        graph_MACD.bar(np.arange(0, len(df_stockload.index)), bar_red, facecolor='red')
        graph_MACD.bar(np.arange(0, len(df_stockload.index)), bar_green, facecolor='green')

        graph_MACD.legend(loc='best', shadow=True, fontsize='10')
        graph_MACD.set_ylabel(u"MACD")
        graph_MACD.set_xlim(0, len(df_stockload.index))  # 设置一下x轴的范围
        graph_MACD.set_xticks(range(0, len(df_stockload.index), 15))  # X轴刻度设定 每15天标一个日期

        # 绘制KDJ
        df_stockload['K'], df_stockload['D'] = talib.STOCH(df_stockload.high.values, df_stockload.low.values,
                                                           df_stockload.close.values, \
                                                           fastk_period=9, slowk_period=3, slowk_matype=0,
                                                           slowd_period=3, slowd_matype=0)

        df_stockload['J'] = 3 * df_stockload['K'] - 2 * df_stockload['D']

        graph_KDJ.plot(np.arange(0, len(df_stockload.index)), df_stockload['K'], 'blue', label='K')  # K
        graph_KDJ.plot(np.arange(0, len(df_stockload.index)), df_stockload['D'], 'g--', label='D')  # D
        graph_KDJ.plot(np.arange(0, len(df_stockload.index)), df_stockload['J'], 'r-', label='J')  # J
        graph_KDJ.legend(loc='best', shadow=True, fontsize='10')

        graph_KDJ.set_ylabel(u"KDJ")
        graph_KDJ.set_xlabel("日期")
        graph_KDJ.set_xlim(0, len(df_stockload.index))  # 设置一下x轴的范围
        graph_KDJ.set_xticks(range(0, len(df_stockload.index), 15))  # X轴刻度设定 每15天标一个日期
        graph_KDJ.set_xticklabels(
            [df_stockload.index.strftime('%Y-%m-%d')[index] for index in graph_KDJ.get_xticks()])  # 标签设置为日期

        # X-轴每个ticker标签都向右倾斜45度
        for label in graph_KAV.xaxis.get_ticklabels():
            label.set_visible(False)

        for label in graph_VOL.xaxis.get_ticklabels():
            label.set_visible(False)

        for label in graph_MACD.xaxis.get_ticklabels():
            label.set_visible(False)

        for label in graph_KDJ.xaxis.get_ticklabels():
            label.set_rotation(45)
            label.set_fontsize(10)  # 设置标签字体
        #删除路径中的*，ST*中含哈的有*
        valid_path = path.replace('*', '')
        plt.savefig(valid_path)
        #plt.show()

    def SetPicture(self,df):
        self.df = df


'''
if __name__ == "__main__":
    StockPictureObj = StockPicture()
'''






