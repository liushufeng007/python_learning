# 为方便演示, 我们随机生成3列正随机数
import pandas as pd


class Macd:
    def __init__(self):
        self.today_dif = 0.0
        self.Tdiff = 0.1
        self.macd_df = 0
        print("macd 初始化完成")


    # 在k线基础上计算MACD，并将结果存储在df上面(dif,dea,bar)
    def fill_macd(self, df, fastperiod=12, slowperiod=26, signalperiod=9):
        ewma12 = df['开盘'].ewm(span=fastperiod, adjust=False).mean()
        ewma26 = df['收盘'].ewm(span=slowperiod, adjust=False).mean()
        df['Ma89'] = df['收盘'].ewm(span=89, adjust=False).mean()
        df['Ma20'] = df['收盘'].ewm(span=20, adjust=False).mean()
        df['Ma10'] = df['收盘'].ewm(span=10, adjust=False).mean()
        df['Ma5'] =  df['收盘'].ewm(span=5, adjust=False).mean()
        df['dif'] = ewma12 - ewma26
        df['dea'] = df['dif'].ewm(span=signalperiod, adjust=False).mean()
        df['bar'] = (df['dif'] - df['dea']) * 2
        df['vol60']=df['成交量'].ewm(span=60, adjust=False).mean()
        # print(df)
        df['最高_'] = df['最高']
        df['最低_'] = df['最低']
        df['收盘_'] = df['收盘']
        df['开盘_'] = df['开盘']


        return df

    # 在k线基础上计算MACD，并将结果存储在df上面(dif,dea,bar)
    def calc_macd(self, df, fastperiod=12, slowperiod=26, signalperiod=9):
        ewma12 = df['close'].ewm(span=fastperiod, adjust=False).mean()
        ewma26 = df['close'].ewm(span=slowperiod, adjust=False).mean()
        df['dif'] = ewma12 - ewma26
        df['dea'] = df['dif'].ewm(span=signalperiod, adjust=False).mean()
        df['bar'] = (df['dif'] - df['dea']) * 2
        return df

    def func_for(self, df):
        num_encode = {'col_1': {'YES': 1, 'NO': 0},
                      'col_2': {'WON': 1, 'LOSE': 0, 'DRAW': 0}}
        df.replace(num_encode, inplace=True)

        currentval = 0.0
        lastvalue = 0.0

        for index in df.index:
            currentval = df.loc[index, 'bar']
            if currentval < 0.0:
                if lastvalue > 0.0:
                    df.loc[index, 'lable'] = 'down'
                    # print('UP',df.loc[index, 'bar'], currentval,lastvalue)
                else:
                    df.loc[index, 'lable'] = 'null'
            else:
                if currentval > 0.0:
                    if lastvalue < 0.0:
                        df.loc[index, 'lable'] = 'up'
                        # print('DN', df.loc[index, 'bar'], currentval, lastvalue)
                    else:
                        df.loc[index, 'lable'] = 'null'
                else:
                    df.loc[index, 'lable'] = 'null'
            lastvalue = currentval

        self.today_dif = df.loc[index, 'dif']
        # print(df)
        return df

    def IsShouldBuy(self, updata, dndata):
        currentdata = 0.0
        last1data = 0.0
        last2data = 0.0
        last3data = 0.0
        upcondition = 0
        dncondition = 0

        for item in updata:
            last3data = last2data
            last2data = last1data
            last1data = currentdata
            currentdata = item

        # print(last3data, '-', last2data, '-', last1data, '-', currentdata)

        if currentdata > last1data + self.Tdiff:
            if last1data > last2data + self.Tdiff:
                #if last2data > last3data + self.Tdiff:
                upcondition = 1

        for item in dndata:
            last3data = last2data
            last2data = last1data
            last1data = currentdata
            currentdata = item
        # print(last3data, '-', last2data, '-', last1data, '-', currentdata)
        if currentdata > last1data + self.Tdiff:
            if last1data > last2data + self.Tdiff:
                #if last2data > last3data + self.Tdiff:
                    dncondition = 1

        condition = 0
        if upcondition == 1 and dncondition == 1 and self.today_dif > 0.1:
            condition = 1
            # print("up:",updata)
            # print("dn",dndata)
            # print(last3data, '-', last2data, '-', last1data, '-', currentdata)
        return condition

    def Capture_Valid_Data(self, df):
        up = []
        dn = []

        for index in df.index:
            if df.loc[index, 'lable'] == 'up':
                data = df.loc[index, 'dif']
                up.append(data)
            elif df.loc[index, 'lable'] == 'down':
                data = df.loc[index, 'dif']
                dn.append(data)

        # print(up,'\n',dn)
        return up, dn

    def Covert_Macd_df(self, df1):
        df = df1
        df['日期'] = pd.to_datetime(df['日期'])
        df.set_index('日期', inplace=True)
        df = df.rename(columns={'日期': 'datetime', '开盘': 'open',
                                '收盘': 'closes', '最高': 'highs',
                                '最低': 'lows', '成交量': 'volume'})




        # 成交额, 振幅, 涨跌幅, 涨跌额, 换手率
        #df = df.drop(labels=['成交额', '振幅', '涨跌幅', '涨跌额', '换手率'], axis=1)  # axis=1 表示按列删除，删除gender列
        #print(df)
        df[['closes', 'highs', 'lows']] = df[['highs', 'lows', 'closes']]
        df = df.rename(columns={'closes': 'high', 'highs': 'low', 'lows': 'close'})


        self.macd_df = self.calc_macd(df)
        return self.macd_df

    def Get_MacdDf(self):
        return self.macd_df

    def Macd_BuyCondition(self, df):
        # 将日期作为行索引
        macd_data = df
        macd_data = self.func_for(macd_data)
        up, dn = self.Capture_Valid_Data(macd_data)
        condition = self.IsShouldBuy(up, dn)

        if condition == 1:
            pass

        return condition


'''
if __name__ == "__main__":
    MacdObj = Macd()
    data = pd.read_csv('000895.csv', parse_dates=True)
    condition = MacdObj.Macd_BuyCondition(data)
    if condition == 1:
        print("买点来了")
    else:
        print("买点还没有到达")
'''
