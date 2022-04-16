import requests
import re
import os
import json
import pandas as pd

class StockStrategy:
    def __init__(self):

        print("StockStrategy 类初始化完成")

    def getrelation(self,yestoday_high,yestoday_low,yestoday_close,today_high,today_low,today_close,today_open):
        relate1 = 0
        relate2 = 0
        relate3 = 0
        if today_high >= yestoday_high and today_low >= yestoday_low:
            relate1 = 0#上升
        elif today_high <= yestoday_high and today_low <= yestoday_low:
            relate1 = 1#下降
        elif today_high <= yestoday_high and today_low >= yestoday_low:
            relate1 = 2#被昨天k线包含
        elif today_high >= yestoday_high and today_low <= yestoday_low:
            relate1 = 3  # 包含昨天的K线
        else:
            print("K线包含出现错误")

        if yestoday_close < today_close:
            relate2 = 0#上升
        else:
            relate2 = 1#下降

        if today_close > today_open:
            relate3 = 0#上升
        else:
            relate3 = 1#下降

        return relate1,relate2,relate3

    def getval(self,df,index):
        max=0
        min=99999999
        decreasepercent=0
        condition = 0

        if(max < float(df.loc[index-3, '最高']) ):
            max = float(df.loc[index - 3, '最高'])
        if(max < float(df.loc[index-2, '最高']) ):
            max = float(df.loc[index - 2, '最高'])
        if(max < float(df.loc[index-1, '最高']) ):
            max = float(df.loc[index - 1, '最高'])
        if(min > float(df.loc[index-3, '最低']) ):
            min = float(df.loc[index - 3, '最低'])
        if(min > float(df.loc[index-2, '最低']) ):
            min = float(df.loc[index - 2, '最低'])
        if(min > float(df.loc[index-1, '最低']) ):
            min = float(df.loc[index - 1, '最低'])

        close_yestoday =float(df.loc[index-1, '收盘'])
        close_today = float(df.loc[index, '收盘'])

        if(close_yestoday <= close_today):
            decreasepercent = 0
        else:
            decreasepercent =(-close_today + close_yestoday)/close_yestoday*100

        #print(decreasepercent)

        if max > float(df.loc[index, '最高']) and float(df.loc[index, '最低'])  > min and decreasepercent >=3 and decreasepercent < 6:
            condition = 1
        return condition

    def filldata1(self, df):

        last_buy = 0
        ewma12 = df['开盘'].ewm(span=12, adjust=False).mean()
        ewma26 = df['收盘'].ewm(span=26, adjust=False).mean()
        df['Ma89'] = df['收盘'].ewm(span=89, adjust=False).mean()
        df['Ma20'] = df['收盘'].ewm(span=20, adjust=False).mean()
        df['Ma10'] = df['收盘'].ewm(span=10, adjust=False).mean()
        df['Ma5'] = df['收盘'].ewm(span=5, adjust=False).mean()
        df['dif'] = ewma12 - ewma26
        df['dea'] = df['dif'].ewm(span=9, adjust=False).mean()
        df['bar'] = (df['dif'] - df['dea']) * 2
        lastindex = 0

        seg1_start_index = 0
        seg1_end_index =0
        seg2_start_index = 0
        seg2_end_index =0
        seg3_start_index = 0
        seg3_end_index =0
        counter = 0
        valid_seg_counter = 0

        df.loc[0, 'flag'] = 'null'

        for index in df.index:
            lastindex = index

        endindex = 0
        endflag = 0
        startcounter = 0
        for index in range(lastindex,0,-1):
            if endflag == 1:
                counter = counter + 1

            if index == lastindex:
                if float(df.loc[index, 'bar']) < 0:
                    df.loc[index, 'flag'] = 'end'
                    endflag = 1
                    endindex = index
                else:
                    df.loc[index, 'flag'] = 'null'
            elif endflag == 1:
                if float(df.loc[index, 'bar']) > 0:
                    if counter > 5:
                        df.loc[index, 'flag'] = 'valid_start'
                        startcounter = startcounter +1
                        if startcounter >= 3:
                            break
                    else:
                        df.loc[index, 'flag'] = 'null'
                        df.loc[endindex, 'flag'] = 'null'
                    counter = 0
                    endflag= 0
                else:
                    df.loc[index, 'flag'] = 'null'
            elif float(df.loc[index, 'bar']) <= 0:
                if float(df.loc[index+1, 'bar']) >= 0:
                    df.loc[index, 'flag'] = 'end'
                    endflag = 1
                    endindex = index
                    counter = 0
                else:
                    df.loc[index, 'flag'] = 'null'
            elif float(df.loc[index, 'bar']) >= 0:
                    df.loc[index, 'flag'] = 'null'
            else:
                df.loc[index, 'flag'] = 'null'
                counter = 0
                print("---------------- error state ----------------")


        flag = 0
        flag1 =0
        seg1_area  = 0
        seg2_area = 0
        seg3_area =0


        for index in df.index:
            if df.loc[1, 'flag'] != 'null':
                break;
            if index >= 1:
                if flag == 0:
                    if df.loc[index, 'flag'] == 'valid_start':
                        seg1_start_index = index
                        flag1 =1
                    elif df.loc[index, 'flag'] == 'end':
                        seg1_end_index = index
                        flag = 1
                        flag1 = 0

                    if flag1 == 1:
                        seg1_area = seg1_area + float(df.loc[index,'bar'])

                elif flag == 1:
                    if df.loc[index, 'flag'] == 'valid_start':
                        seg2_start_index = index
                        flag1 = 1
                    elif df.loc[index, 'flag'] == 'end':
                        seg2_end_index = index
                        flag = 2
                        flag1 = 0

                    if flag1 == 1:
                        seg2_area = seg2_area + float(df.loc[index, 'bar'])

                elif flag == 2:
                    if df.loc[index, 'flag'] == 'valid_start':
                        seg3_start_index = index
                        flag1 = 1
                    elif df.loc[index, 'flag'] == 'end':
                        seg3_end_index = index
                        flag = 0
                        flag1 = 0
                        break

                    if flag1 == 1:
                        seg3_area = seg3_area + float(df.loc[index, 'bar'])
                else:
                    print("error:请确任算法是否有问题\n")

        condition =0
        if seg1_area < seg2_area*1.2 and seg1_area < seg3_area and seg2_area < seg3_area*1.2:
            if float(df.loc[lastindex,'bar']) < 0:
                if float(df.loc[seg1_start_index,'最低']) > float(df.loc[seg2_start_index,'最低']) and float(df.loc[seg1_start_index,'最低']) > float(df.loc[seg3_start_index,'最低']):
                    if float(df.loc[seg2_start_index, '最低']) > float(df.loc[seg3_start_index, '最低']):
                        if float(df.loc[seg1_end_index, '最低']) > float(df.loc[seg2_end_index, '最低']) and float(
                                df.loc[seg1_end_index, '最低']) > float(df.loc[seg3_end_index, '最低']):
                            if float(df.loc[seg2_end_index, '最低']) > float(df.loc[seg3_end_index, '最低']):
                                pd.set_option('display.max_colwidth', 500)
                                pd.set_option('display.max_rows', None)
                                print(df)
                                condition = 1
        if df.loc[1, 'flag'] != 'null':
            condition =0

        return df,condition





    def filldata(self, df):
        last_upflag = 0
        last_downflag = 1
        upcounter = 0
        df['Ma20'] = df['收盘'].ewm(span=20, adjust=False).mean()
        #df['Transfer20'] = df['换手率'].ewm(span=20, adjust=False).mean()
        #df['Transfer3'] = df['换手率'].ewm(span=3, adjust=False).mean()
        lastindex= 0

        up_diff = 10
        dn_diff = 1
        up_rate = 0.2
        dn_rate = 0.05

        for index in df.index:
            lastindex = index
            if index > 1:
                if last_upflag == 0:

                    if float(df.loc[index, '最高']) > float(df.loc[index-1, '最高'])*1.01 and \
                       float(df.loc[index, '最低']) > float(df.loc[index-1, '最低'])*1.01:

                        upcounter = upcounter + 1

                        if upcounter >= 2 :
                            if last_upflag == 0 and  \
                               float(df.loc[index, '换手率']) < float(df.loc[index-1 , '换手率'])*(up_diff + 1) and \
                               float(df.loc[index, '换手率']) > float(df.loc[index - 1, '换手率'])*(1- dn_diff ) and \
                               float(df.loc[index-1, '换手率']) < float(df.loc[index-2 , '换手率'])*(up_diff + 1) and \
                               float(df.loc[index-1, '换手率']) > float(df.loc[index-2,  '换手率'])*(1- dn_diff ) and \
                               float(df.loc[index , '换手率']) < 100 and \
                               float(df.loc[index, '收盘']) < float(df.loc[index, '开盘']) * (1+up_rate) and \
                               float(df.loc[index, '收盘']) > float(df.loc[index, '开盘']) * (1-dn_rate) and \
                               float(df.loc[index, '最低']) < float(df.loc[index, 'Ma20'])*1 :

                                df.loc[index, 'buy'] = '买'
                                last_upflag = 1
                                last_downflag = 0
                            else:
                                last_upflag = 0
                                last_downflag = 1
                                upcounter = 0
                                df.loc[index, 'buy'] = "null"
                        else:
                            df.loc[index, 'buy'] = 'null'
                    else:
                        last_upflag = 0
                        last_downflag = 1
                        upcounter = 0
                        df.loc[index, 'buy'] = "null"
                else:
                    if 0:
                        df.loc[index, 'buy'] = '卖'
                        last_upflag = 0
                        last_downflag = 1
                        upcounter = 0
                    elif float(df.loc[index, '最低']) <= float(df.loc[index-1, '最低']) or float(df.loc[index, '最高']) <= float(df.loc[index-1, '最高']):
                        if last_upflag == 1 and last_downflag == 0:
                            df.loc[index, 'buy'] = '卖'
                        else:
                           df.loc[index, 'buy'] = 'null'
                        last_upflag = 0
                        last_downflag = 1
                        upcounter = 0
                    else:
                        df.loc[index, 'buy'] = 'null'




        if df.loc[lastindex, 'buy'] == '买':
            condition = 1
        else:
            condition = 0
        return df,condition


    def filldata2(self, df):

        buy = 0
        lastindex = 0
        for index in df.index:
            if index > 2:
                lastindex = index
                if buy == 0:
                    if float(df.loc[index-1, '收盘']) >= float(df.loc[index-2, '收盘'])*1.096 and \
                       float(df.loc[index, '收盘']) <= float(df.loc[index - 1, '收盘']) * 0.989 and \
                       float(df.loc[index, '收盘']) >= float(df.loc[index - 1, '收盘']) * 0.995 and \
                       float(df.loc[index, '收盘']) >= float(df.loc[index, '开盘']) * 1 and \
                       float(df.loc[index, '换手率']) <= float(df.loc[index - 1, '换手率']):

                        df.loc[index, 'buy'] = '买'
                        buy = 1
                    else:
                        buy = 0
                        df.loc[index, 'buy'] = "null"
                else:
                    df.loc[index, 'buy'] = '卖'
                    buy = 0


        if df.loc[lastindex, 'buy'] == '买':
            condition = 1
        else:
            condition = 0
        return df,condition

    def getcondition(self,df):
        df1,condition = self.filldata(df)
        return condition,df1



if __name__ == "__main__":
    StockCodeObj = StockTEST()
    print(StockCodeObj.data.win_lost_ratio)

