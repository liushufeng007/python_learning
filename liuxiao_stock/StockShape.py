# 为方便演示, 我们随机生成3列正随机数
import pandas as pd
import numpy as np
#import talib

par = {"up":1,
       "dn":0
        }

class StockShape:
    def __init__(self):
        self.df = 0
        self.uncomfirm_pt = 0
        self.comfirm_pt = 0
        self.current_direction = par["up"]
        self.last_max = 0
        self.last_min = 0
        print("stock Shape 初始化完成")
    def SetFirstKValue(self,max,min):
        self.last_max = max
        self.last_min = min


    def GetReverseVal(self,yestodaymax,yestodaymin,todaymidmax,todaymidmin,tommorrowmax,tommorrowmin):
        todaymid = (todaymidmax+todaymidmin)/2
        if todaymid < yestodaymin:
            yestodayReverse = 1
        elif todaymid > yestodaymax:
            yestodayReverse = 0
        else:
            yestodayReverse = (yestodaymax - todaymid) / (yestodaymax - yestodaymin)

        if todaymid < tommorrowmin:
            tommorrowReverse = 1
        elif todaymid > tommorrowmax:
            tommorrowReverse = 0
        else:
            tommorrowReverse = (tommorrowmax - todaymid) / (tommorrowmax - tommorrowmin)

        yestodayReverse_e2 = yestodayReverse #* yestodayReverse
        tommorrowReverse_e2 = tommorrowReverse #* tommorrowReverse

        return yestodayReverse_e2,tommorrowReverse_e2


    def GetConditionisOk(self,yestodayRelativepower,tommorrowRelativepower,yestodayreverse,todayreverse,tommorrowreverse):
        if yestodayRelativepower > 0.1 and tommorrowRelativepower > 0.1 and yestodayreverse > 0.1 and todayreverse > 0.1 and tommorrowreverse > 0.1:
            condition = 1
        else:
            condition = 0
        return condition

    def GetMaxMinVal(self,open,close):
        #获取当前有效的K线值
        if open >= close:
            max = open
            min = close
        else:
            max = close
            min = open

        return max,min

    def CalShapeCondition(self,df):
        #初始化last值为第一根k线值
        max = float(df.loc[0, '最高'])
        min = float(df.loc[0, '最低'])
        df['close'] = df['收盘'].astype('float')
        #df['Ma20'] = df.close.rolling(window=20).mean()
        #df['Ma30'] = df.close.rolling(window=30).mean()
        #df['Ma5'] = df.close.rolling(window=5).mean()
        df = df.drop(labels=['close'], axis=1)  # axis=1 表示按列删除，删除gender列
        self.SetFirstKValue(max,min)
        #遍历k线
        for index in df.index:
            max = float(df.loc[index, '最高'])
            min = float(df.loc[index, '最低'])
            Mid_max, Mid_min = self.GetMaxMinVal(float(df.loc[index, '开盘']), float(df.loc[index, '开盘']))
            Mid_val = (Mid_max + Mid_min) / 2
            if max > min:
                Percent = (Mid_val - min) / (max - min)
                Percent_E2 = Percent #* Percent
                df.loc[index, '转折力度'] = Percent_E2
            else:
                #print(index,":最大值和最小值相等:",max,min)
                df.loc[index, '转折力度'] = 0
            len = index

        for index in df.index:
           if index > 0 and index < len:
               max = float(df.loc[index, '最高'])
               min = float(df.loc[index, '最低'])
               todayresver = float(df.loc[index, '转折力度'])
               yesterday_max = float(df.loc[index-1, '最高'])
               yesterday_min = float(df.loc[index-1, '最低'])
               yestodayresver = float(df.loc[index-1, '转折力度'])
               tomorrow_max = float(df.loc[index+1, '最高'])
               tomorrow_min = float(df.loc[index+1, '最低'])
               tommorrowresver = float(df.loc[index + 1, '转折力度'])
               Mid_max, Mid_min = self.GetMaxMinVal(float(df.loc[index, '开盘']), float(df.loc[index, '开盘']))

               df.loc[index, '前相对转折力度'] = 0
               df.loc[index, '后相对转折力度'] = 0

               if max < yesterday_max and max < tomorrow_max and min <  yesterday_min and min < tomorrow_min:
                   yestodayRelativepower,tomorrowRelativepower = self.GetReverseVal(yesterday_max,yesterday_min,Mid_max,Mid_min,tomorrow_max,tomorrow_min)
                   condition = self.GetConditionisOk(yestodayRelativepower,tomorrowRelativepower,yestodayresver,todayresver,tommorrowresver)
                   if condition == 1:
                       df.loc[index, '分型'] = "强力度底分型"
                       df.loc[index, '前相对转折力度'] = yestodayRelativepower
                       df.loc[index, '后相对转折力度'] = tomorrowRelativepower
                   else:
                       if todayresver > 0.5 and yestodayresver > 0.5 and tommorrowresver > 0.5:
                           df.loc[index, '分型'] = "有力度底分型"
                       else:
                           df.loc[index, '分型'] = "无力度分型"
               elif max > yesterday_max and max > tomorrow_max and min >  yesterday_min and min > tomorrow_min:
                   df.loc[index, '分型'] = "顶分型"
               else:
                   df.loc[index, '分型'] = "无分型"

        counter = 0
        for index in range(0,2):
            #if df.loc[len - index, 'Ma30'] <  df.loc[len - index, 'Ma5'] or df.loc[len - index, 'Ma20'] <  df.loc[len - index, 'Ma5']:
            if df.loc[len - index, '分型'] == "有力度底分型":
                counter = counter+2
            elif df.loc[len - index, '分型'] == "无力度底分型":
                counter = counter+1

        for index in range(0,2):
            if df.loc[len - index, '分型'] == "强力度底分型":
                #if df.loc[len - index, 'Ma30'] > df.loc[len - index, 'Ma5'] or df.loc[len - index, 'Ma20'] > df.loc[len - index, 'Ma5']:
                counter = counter+3

        if counter >= 3:
            retvalue = True
        else:
            retvalue = False

        return  retvalue,df


    def CalShapeConditionDay(self,df):
        #初始化last值为第一根k线值
        max = float(df.loc[0, '最高'])
        min = float(df.loc[0, '最低'])
        df['close'] = df['收盘'].astype('float')
        #df['Ma20'] = df.close.rolling(window=20).mean()
        #df['Ma30'] = df.close.rolling(window=30).mean()
        #df['Ma5'] = df.close.rolling(window=5).mean()
        df = df.drop(labels=['close'], axis=1)  # axis=1 表示按列删除，删除gender列
        self.SetFirstKValue(max,min)
        #遍历k线
        for index in df.index:
            max = float(df.loc[index, '最高'])
            min = float(df.loc[index, '最低'])
            Mid_max, Mid_min = self.GetMaxMinVal(float(df.loc[index, '开盘']), float(df.loc[index, '开盘']))
            Mid_val = (Mid_max + Mid_min) / 2
            if max > min:
                Percent = (Mid_val - min) / (max - min)
                Percent_E2 = Percent #* Percent
                df.loc[index, '转折力度'] = Percent_E2
            else:
                #print(index,":最大值和最小值相等:",max,min)
                df.loc[index, '转折力度'] = 0
            len = index

        for index in df.index:
           if index > 0 and index < len:
               max = float(df.loc[index, '最高'])
               min = float(df.loc[index, '最低'])
               todayresver = float(df.loc[index, '转折力度'])
               yesterday_max = float(df.loc[index-1, '最高'])
               yesterday_min = float(df.loc[index-1, '最低'])
               yestodayresver = float(df.loc[index-1, '转折力度'])
               tomorrow_max = float(df.loc[index+1, '最高'])
               tomorrow_min = float(df.loc[index+1, '最低'])
               tommorrowresver = float(df.loc[index + 1, '转折力度'])
               Mid_max, Mid_min = self.GetMaxMinVal(float(df.loc[index, '开盘']), float(df.loc[index, '开盘']))

               df.loc[index, '前相对转折力度'] = 0
               df.loc[index, '后相对转折力度'] = 0

               if max < yesterday_max and max < tomorrow_max and min <  yesterday_min and min < tomorrow_min:
                   yestodayRelativepower,tomorrowRelativepower = self.GetReverseVal(yesterday_max,yesterday_min,Mid_max,Mid_min,tomorrow_max,tomorrow_min)
                   condition = self.GetConditionisOk(yestodayRelativepower,tomorrowRelativepower,yestodayresver,todayresver,tommorrowresver)
                   if condition == 1:
                       df.loc[index, '分型'] = "强力度底分型"
                       df.loc[index, '前相对转折力度'] = yestodayRelativepower
                       df.loc[index, '后相对转折力度'] = tomorrowRelativepower
                   else:
                       if todayresver > 0.5 and yestodayresver > 0.5 and tommorrowresver > 0.5:
                           df.loc[index, '分型'] = "有力度底分型"
                       else:
                           df.loc[index, '分型'] = "无力度分型"
               elif max > yesterday_max and max > tomorrow_max and min >  yesterday_min and min > tomorrow_min:
                   df.loc[index, '分型'] = "顶分型"
               else:
                   df.loc[index, '分型'] = "无分型"

        counter = 0
        for index in range(0,4):
            #if df.loc[len - index, 'Ma30'] <  df.loc[len - index, 'Ma5'] or df.loc[len - index, 'Ma20'] <  df.loc[len - index, 'Ma5']:
            if df.loc[len - index, '分型'] == "有力度底分型":
                counter = counter+2
            elif df.loc[len - index, '分型'] == "无力度底分型":
                counter = counter+1

        for index in range(0,4):
            if df.loc[len - index, '分型'] == "强力度底分型":
                #if df.loc[len - index, 'Ma30'] > df.loc[len - index, 'Ma5'] or df.loc[len - index, 'Ma20'] > df.loc[len - index, 'Ma5']:
                counter = counter+3

        if counter >= 3:
            retvalue = True
        else:
            retvalue = False

        return  retvalue,df





'''
if __name__ == "__main__":
    StockPictureObj = StockPicture()
'''






