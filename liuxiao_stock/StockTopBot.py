# 为方便演示, 我们随机生成3列正随机数
import pandas as pd
import numpy as np

class StockTopK:
    def __init__(self):
        self.df = 0
        self.par = {"up": 1,
               "dn": 0
               }
        self.type = {"top": 1,
               "bot": 0
               }
        self.unconfirm_index = 0
        self.unconfirm_type = ''
        #self.counterUpK = 0
        #self.counterDnK = 0
        self.validKcounter = 0
        #self.lastdirect = 'up'

        print("stock Top kline 初始化完成")

    def GetDfLastIndex(self,df):
        for index in df.index:
            pass
        return index

    def preupdateTopShape(self,df,last_index):
        df.loc[0, 'k预分型'] = '无'
        #last_index = self.GetDfLastIndex(df)
        for index in df.index:
            if index > 0 and index < last_index:
                if df.loc[index, 'k有效位'] == "有效k":
                    if df.loc[index, 'k方向'] == 'up' and df.loc[index + 1, 'k方向'] == 'up':
                        df.loc[index, 'k预分型'] = '无'
                    elif df.loc[index, 'k方向'] == 'up' and df.loc[index + 1, 'k方向'] == 'dn':
                        df.loc[index, 'k预分型'] = '顶'
                    elif df.loc[index, 'k方向'] == 'dn' and df.loc[index + 1, 'k方向'] == 'dn':
                        df.loc[index, 'k预分型'] = '无'
                    elif df.loc[index, 'k方向'] == 'dn' and df.loc[index + 1, 'k方向'] == 'up':
                        df.loc[index, 'k预分型'] = '底'
                    else:
                        df.loc[index, 'k预分型'] = '无'
                else:
                    df.loc[index, 'k预分型'] = '无'
            else:
                df.loc[index, 'k预分型'] = '无'
        return df

    def insertbreaklinedata(self,df):
        df.loc[0, '折线数据'] = 0
        last_top_index = 0
        last_top_type = '顶'
        currnt_top_index = 0
        currnt_top_type = '顶'

        for index in df.index:
            if last_top_index == 0:
                #刚才开始还没有顶底分型，就用收盘价格填充
                df.loc[index, '折线数据'] = df.loc[index, '收盘']
            if df.loc[index, 'k分型'] == '顶' or df.loc[index, 'k分型'] == '底':
                currnt_top_index = index
                currnt_top_type = df.loc[index, 'k分型']
                if last_top_index == 0:
                    pass
                else:
                    if last_top_type == '顶':
                        start_value_str = df.loc[last_top_index, '最高']
                        end_value_str = df.loc[currnt_top_index, '最低']
                    else:
                        start_value_str = df.loc[last_top_index, '最低']
                        end_value_str = df.loc[currnt_top_index, '最高']
                    end_value = float(end_value_str)
                    start_value = float(start_value_str)

                    diff_V = (end_value - start_value) / (currnt_top_index - last_top_index)

                    #开始插入值
                    for subindex in range(last_top_index,currnt_top_index):
                        df.loc[subindex, '折线数据'] = round(((subindex - last_top_index) * diff_V + start_value),2)

                last_top_index = currnt_top_index
                last_top_type  = currnt_top_type
            else:
                pass
                #只处理带分型的数据
        # 开始插入值
        last_index = self.GetDfLastIndex(df)
        for subindex in range(currnt_top_index, last_index+1):
            df.loc[subindex, '折线数据'] = df.loc[subindex, '收盘']

        return df

    def updateTopBottomShape(self,df,last_index):
        #遍历k线
        self.validKcounter = 0
        self.unconfirm_type = ''
        self.unconfirm_index =0
        #last_index = self.GetDfLastIndex(df)
        predf = self.preupdateTopShape(df,last_index)
        predf.loc[0, 'k分型'] = '无'
        self.validKcounter = 0
        self.unconfirm_type = ''
        self.unconfirm_index =0
        for index in predf.index:
            if index > 0 and index < last_index:
                if predf.loc[index, 'k有效位'] == '有效k':
                    self.validKcounter = self.validKcounter + 1

                if self.validKcounter >= 4:
                    if self.unconfirm_type == '底':
                        # 分型确立
                        if predf.loc[index, 'k预分型'] == '顶':
                           self.unconfirm_index = index
                           self.unconfirm_type = '顶'
                           predf.loc[index, 'k分型'] = '顶'
                           self.validKcounter = 0
                           #print("分支0")
                        #底了又底
                        elif predf.loc[index, 'k预分型'] == '底':
                            #底创造新低
                           if float(predf.loc[index, '最低']) <= float(predf.loc[self.unconfirm_index, '最低']):
                               #print(index, "  ", self.unconfirm_index, "底创造新低，覆盖了一次")
                               predf.loc[index, 'k分型'] = '底'
                               predf.loc[self.unconfirm_index, 'k分型'] = '无'
                               self.unconfirm_index = index
                               self.unconfirm_type = '底'
                               self.validKcounter = 0
                               #print("分支1")
                           else:
                               predf.loc[index, 'k分型'] = '无'
                               #self.unconfirm_index = index
                               #self.unconfirm_type = '底'
                               predf.loc[index, 'k分型'] = '无'
                               #self.validKcounter = 0
                               #print("分支2")
                        else:
                            predf.loc[index, 'k分型'] = '无'
                            #print("分支3")
                    elif self.unconfirm_type == '顶':
                        #顶了又顶
                        if predf.loc[index, 'k预分型'] == '顶':
                            #顶创造新高
                            if float(predf.loc[index, '最高']) >= float(predf.loc[self.unconfirm_index, '最高']):
                                #print(index, "  ", self.unconfirm_index, "底创高，覆盖了一次")
                                predf.loc[index, 'k分型'] = '顶'
                                predf.loc[self.unconfirm_index, 'k分型'] = '无'
                                self.unconfirm_index = index
                                self.unconfirm_type = '顶'
                                self.validKcounter = 0
                                #print("分支13")
                            else:
                                predf.loc[index, 'k分型'] = '无'
                                # self.unconfirm_index = index
                                # self.unconfirm_type = '底'
                                predf.loc[index, 'k分型'] = '无'
                                # self.validKcounter = 0
                                #print("分支4")
                        #分型确立
                        elif predf.loc[index, 'k预分型'] == '底':
                           self.unconfirm_index = index
                           self.unconfirm_type = '底'
                           predf.loc[index, 'k分型'] = '底'
                           self.validKcounter = 0
                           #print("分支5")
                        else:
                            predf.loc[index, 'k分型'] = '无'
                            #print("分支11")
                    elif self.unconfirm_type == '':
                        # 首次分型确立
                        if predf.loc[index, 'k预分型'] == '顶':
                           self.unconfirm_index = index
                           self.unconfirm_type = '顶'
                           predf.loc[index, 'k分型'] = '顶'
                           self.validKcounter = 0
                           #print("分支7")
                        # 首次分型确立
                        elif predf.loc[index, 'k预分型'] == '底':
                           self.unconfirm_index = index
                           self.unconfirm_type = '底'
                           predf.loc[index, 'k分型'] = '底'
                           self.validKcounter = 0
                           #print("分支8")
                        else:
                            predf.loc[index, 'k分型'] = '无'
                            #print("分支9")
                    #非顶和底还是无
                    else:
                        predf.loc[index, 'k分型'] = '无'
                        #print("分支10")
                #少于5K不成立
                else:
                    if self.unconfirm_type == '底':
                        # 分型确立
                        if predf.loc[index, 'k预分型'] == '底':
                            #底创造新低
                           if float(predf.loc[index, '最低']) <= float(predf.loc[self.unconfirm_index, '最低']):
                               #print(index, "  ", self.unconfirm_index, "底创造新低，覆盖了一次")
                               predf.loc[index, 'k分型'] = '底'
                               predf.loc[self.unconfirm_index, 'k分型'] = '无'
                               self.unconfirm_index = index
                               self.unconfirm_type = '底'
                               self.validKcounter = 0
                               #print("分支1")
                           else:
                               predf.loc[index, 'k分型'] = '无'
                        else:
                            predf.loc[index, 'k分型'] = '无'
                    elif self.unconfirm_type == '顶':
                        #顶了又顶
                        if predf.loc[index, 'k预分型'] == '顶':
                            #顶创造新高
                            if float(predf.loc[index, '最高']) >= float(predf.loc[self.unconfirm_index, '最高']):
                                #print(index, "  ", self.unconfirm_index, "底创高，覆盖了一次")
                                predf.loc[index, 'k分型'] = '顶'
                                predf.loc[self.unconfirm_index, 'k分型'] = '无'
                                self.unconfirm_index = index
                                self.unconfirm_type = '顶'
                                self.validKcounter = 0
                            else:
                                predf.loc[index, 'k分型'] = '无'
                        else:
                            predf.loc[index, 'k分型'] = '无'
                    else:
                        predf.loc[index, 'k分型'] = '无'
            #最后一天
            else:
                predf.loc[index, 'k分型'] = '无'
                #print("分支12")
            #print(index,":",predf.loc[index, 'k分型'],":",last_index,":",self.validKcounter,":",self.unconfirm_type,":",self.unconfirm_index)
        #print(predf)
        updatedf = self.insertbreaklinedata(predf)
        return  updatedf

    def Get_MaxIndex_MinIndex(self,df):
        Temp_Max = 0
        Temp_Min = 999999999
        Temp_Max_Index = 0
        Temp_Min_Index = 0
        Temp_Index = 0
        for index in df.index:
            if Temp_Min > float(df.loc[index, '最低']):
                Temp_Min = float(df.loc[index, '最低'])
                Temp_Min_Index = index

            if Temp_Max < float(df.loc[index, '最高']):
                Temp_Max = float(df.loc[index, '最高'])
                Temp_Max_Index = index

        if Temp_Min_Index < Temp_Max_Index:
            Temp_Index = Temp_Min_Index
        else:
            Temp_Index = Temp_Max_Index

        return Temp_Index


    def update_ZS_df(self,df):
        init_val = float(df.loc[0, '收盘'])*0.90
        df.loc[0, '中枢顶'] = init_val
        df.loc[0, '中枢底'] = init_val
        #temp_index1 = 0
        temp_index2 = 0
        temp_index3 = 0
        temp_index4 = 0
        temp_index5 = 0
        ZG = init_val
        ZD = init_val
        Last_ZG = init_val
        Last_ZD = init_val
        ZS_Flag = 0
        ZS_Flag_1 = 0
        BI_G = 0
        BI_D = 0
        ZS_Area_index = 0
        BI_Cnt = 0
        temp_ZG = 0
        temp_ZD = 0
        New_ZS_Flag = 0
        Start_Index = self.Get_MaxIndex_MinIndex(df)


        for index in df.index:
            if index < Start_Index:
                continue
            if df.loc[index, 'k分型'] == '顶' or df.loc[index, 'k分型'] == '底':
                temp_index5 = temp_index4
                temp_index4 = temp_index3
                temp_index3 = temp_index2
                temp_index2 = index
                if temp_index5 <= ZS_Area_index:
                    continue
                #5个点判断完毕，需要判断中枢
                elif temp_index5 != 0:
                    if df.loc[temp_index5, 'k分型'] == '顶':
                        if float(df.loc[temp_index5, '最高']) < float(df.loc[temp_index2, '最低']):
                            # 上升趋势
                            #ZG = 0
                            #ZD = 0
                            BI_G = float(df.loc[temp_index3, '最高'])
                            BI_D = float(df.loc[temp_index2, '最低'])
                        elif float(df.loc[temp_index5, '最高']) > float(df.loc[temp_index3, '最高']) and float(df.loc[temp_index4, '最低']) > float(df.loc[temp_index2, '最低']):
                            # 下降趋势
                            #ZG = 0
                            #ZD = 0
                            BI_G = float(df.loc[temp_index3, '最高'])
                            BI_D = float(df.loc[temp_index2, '最低'])
                        else:
                            if ZS_Flag_1 == 1:
                                #第5段是否与上次中枢重叠
                                if not (float(df.loc[temp_index5, '最高']) < Last_ZD or float(df.loc[temp_index4, '最低']) > Last_ZG ):
                                    #新中枢继续往前找
                                    New_ZS_Flag = 1
                                elif float(df.loc[temp_index2, '最低']) > Last_ZG or float(df.loc[temp_index3, '最高']) < Last_ZD:
                                    #不重叠新中枢成立
                                    if float(df.loc[temp_index5, '最高']) <= float(df.loc[temp_index3, '最高']):
                                        ZG = float(df.loc[temp_index5, '最高'])
                                    else:
                                        ZG = float(df.loc[temp_index3, '最高'])
                                    if float(df.loc[temp_index4, '最低']) >= float(df.loc[temp_index2, '最低']):
                                        ZD = float(df.loc[temp_index4, '最低'])
                                    else:
                                        ZD = float(df.loc[temp_index2, '最低'])
                                    ZS_Flag = 1
                                else:
                                    #中枢扩张
                                    BI_G = float(df.loc[temp_index3, '最高'])
                                    BI_D = float(df.loc[temp_index2, '最低'])
                            else:
                                # 中枢
                                if float(df.loc[temp_index5, '最高']) <= float(df.loc[temp_index3, '最高']):
                                    ZG = float(df.loc[temp_index5, '最高'])
                                else:
                                    ZG = float(df.loc[temp_index3, '最高'])
                                if float(df.loc[temp_index4, '最低']) >= float(df.loc[temp_index2, '最低']):
                                    ZD = float(df.loc[temp_index4, '最低'])
                                else:
                                    ZD = float(df.loc[temp_index2, '最低'])
                                ZS_Flag = 1

                    elif df.loc[temp_index5, 'k分型'] == '底':
                        if float(df.loc[temp_index5, '最低']) > float(df.loc[temp_index2, '最高']):
                            # 下降趋势
                            #ZG = 0
                            #ZD = 0
                            BI_D = float(df.loc[temp_index3, '最低'])
                            BI_G = float(df.loc[temp_index2, '最高'])
                        elif float(df.loc[temp_index5, '最低']) < float(df.loc[temp_index3, '最低']) and float(df.loc[temp_index4, '最高']) < float(df.loc[temp_index2, '最高']):
                            # 上升趋势
                            #ZG = 0
                            #ZD = 0
                            BI_D = float(df.loc[temp_index3, '最低'])
                            BI_G = float(df.loc[temp_index2, '最高'])
                        else:
                            if ZS_Flag_1 == 1:
                                #第5段是否与上次中枢重叠
                                if not (float(df.loc[temp_index5, '最低']) > Last_ZG or float(df.loc[temp_index4, '最高']) < Last_ZD ):
                                    #新中枢继续往前找
                                    New_ZS_Flag = 1
                                elif float(df.loc[temp_index2, '最高']) < Last_ZD or float(df.loc[temp_index3, '最低']) > Last_ZG:
                                    #不重叠新中枢成立
                                    if float(df.loc[temp_index5, '最低']) >= float(df.loc[temp_index3, '最低']):
                                        ZD = float(df.loc[temp_index5, '最低'])
                                    else:
                                        ZD = float(df.loc[temp_index3, '最低'])
                                    if float(df.loc[temp_index4, '最高']) <= float(df.loc[temp_index2, '最高']):
                                        ZG = float(df.loc[temp_index4, '最高'])
                                    else:
                                        ZG = float(df.loc[temp_index2, '最高'])
                                    ZS_Flag = 1
                                else:
                                    #中枢扩张
                                    BI_D = float(df.loc[temp_index3, '最低'])
                                    BI_G = float(df.loc[temp_index2, '最高'])
                            else:
                                # 中枢
                                if float(df.loc[temp_index5, '最低']) >= float(df.loc[temp_index3, '最低']):
                                    ZD = float(df.loc[temp_index5, '最低'])
                                else:
                                    ZD = float(df.loc[temp_index3, '最低'])
                                if float(df.loc[temp_index4, '最高']) <= float(df.loc[temp_index2, '最高']):
                                    ZG = float(df.loc[temp_index4, '最高'])
                                else:
                                    ZG = float(df.loc[temp_index2, '最高'])
                                ZS_Flag = 1
                    else:
                        print("处理错误，1111111111111")


                    if ZS_Flag == 1:
                        ZS_Area_index = temp_index2
                        ZS_Flag = 0
                        if ZD > Last_ZG or ZG < Last_ZD:
                        #中枢不重叠
                            Last_ZD = ZD
                            Last_ZG = ZG
                        else:
                        #中枢重叠，保持上一次中枢的值
                            ZD = Last_ZD
                            ZG = Last_ZG
                        ZS_Flag_1 = 1
                    else:
                        if New_ZS_Flag == 0:
                            if BI_D > Last_ZG or BI_G < Last_ZD:
                            #笔与中枢不重叠
                                ZD = Last_ZD
                                ZG = Last_ZG
                            else:
                            #笔与中枢重叠
                                ZD = Last_ZD
                                ZG = Last_ZG
                                #ZS_Area_index = temp_index3

                    if New_ZS_Flag == 0:
                        df.loc[temp_index5, '中枢顶'] = ZG
                        df.loc[temp_index5, '中枢底'] = ZD

                    New_ZS_Flag = 0
                    if ZD > ZG:
                        print("中枢这里判断有问题，请核查！  ")

        pd.set_option('display.max_columns', 1000)
        pd.set_option('display.max_rows', 1000)
        pd.set_option('display.width', 1000)
        pd.set_option('display.max_colwidth', 1000)
        #print(df)

        last_top = 0
        last_bot = 0
        for index in df.index:
            if pd.isna(df.loc[index, '中枢顶']):
                df.loc[index, '中枢顶']  = last_top
            else:
                last_top = float(df.loc[index, '中枢顶'])

            if pd.isna(df.loc[index, '中枢底']):
                df.loc[index, '中枢底']  = last_bot
            else:
                last_bot = float(df.loc[index, '中枢底'])
        #print(df)
        return df

    def GetCondition(self, df):
        condition = 0
        Dn_ZS_Cnt = 0
        Last_Bot_Cnt=0
        Last_Bot_Index = 0
        for index in df.index:
            if index > 0:
                if float(df.loc[index, '中枢底']) < float(df.loc[index-1, '中枢底']):
                    Dn_ZS_Cnt = Dn_ZS_Cnt + 1
                elif float(df.loc[index, '中枢底']) == float(df.loc[index - 1, '中枢底']):
                    pass
                else:
                    Dn_ZS_Cnt = 0

                if df.loc[index, 'k分型'] == "底":
                    Last_Bot_Cnt = 0
                    Last_Bot_Index = index
                else:
                    Last_Bot_Cnt = Last_Bot_Cnt + 1


        if Dn_ZS_Cnt >= 2 and Last_Bot_Cnt < 3 and float(df.loc[Last_Bot_Index, '中枢顶']) < float(df.loc[Last_Bot_Index, '最低']) :
            condition = 1
        else:
            condition =0

        return condition





'''
if __name__ == "__main__":
    StockPictureObj = StockPicture()
'''






