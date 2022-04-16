import requests
import re
import os
import json
import pandas as pd

class StockStatistics:
    def __init__(self):
        '''
        需要统计数据有：
        .总盈利次数
        .总亏损次数
        .最大盈利
        .平均盈利
        .盈利总额
        .最大亏损
        .平均亏损
        .亏损总额
        .总机会=总盈利次数+总亏损次数
        .盈亏比=平均盈利/平均亏损
        .准确率=总盈利次数/总机会
        .总盈亏=-亏损总额+盈利总额
        '''
        self.win_timers = 0
        self.lost_timers = 0
        self.max_win_val = 0
        self.avg_win_val = 0
        self.total_win_val = 0
        self.max_lost_val = 0
        self.avg_lost_val = 0
        self.total_lost_val = 0
        self.total_changes = 0
        self.win_lost_ratio = 0.0
        self.correct_ratio = 0
        self.total_val = 0.0
        self.cost = 0.0
        self.win_ratio = 0.0
        self.expect_ratio = 0.0
        self.const_val = 10000
        self.total_avg_win = 0
        self.total_days=0
        self.avg_days=0
        print("StockStatistics 类初始化完成")

class StockTEST:
    def __init__(self):
        self.data = StockStatistics()
        print("StcokTEST 类初始化完成")

    def init_data(self):
        self.data.win_timers = 0
        self.data.lost_timers = 0
        self.data.max_win_val = 0
        self.data.avg_win_val = 0
        self.data.total_win_val = 0
        self.data.max_lost_val = 0
        self.data.avg_lost_val = 0
        self.data.total_lost_val = 0
        self.data.total_changes = 0
        self.data.win_lost_ratio = 0.0
        self.data.correct_ratio = 0
        self.data.total_val = 0.0
        self.data.cost = 0.0
        self.data.win_ratio = 0.0
        self.data.expect_ratio = 0.0
        self.data.const_val = 10000
        self.data.total_avg_win = 0.0
        self.data.avg = 0
        self.data.total_days = 0


    def accounts(self,buy,sale,buyindex=0,saleindex=0):#总计每一次卖出时候的数据
        if buy > 0:
            temp1val = self.data.const_val / buy
            self.data.total_days = self.data.total_days+saleindex-buyindex
            if sale > buy :
                self.data.win_timers = self.data.win_timers  + 1
                if (sale - buy)*temp1val > self.data.max_win_val:
                    self.data.max_win_val = (sale - buy)*temp1val
                temp2val = temp1val * (sale - buy)
                self.data.total_win_val = self.data.total_win_val+temp2val
                self.data.cost = self.data.cost + self.data.const_val
            else:
                self.data.lost_timers = self.data.lost_timers + 1
                if (-sale + buy)*temp1val > self.data.max_lost_val:
                    self.data.max_lost_val = (-sale + buy)*temp1val
                temp2val = temp1val * (-sale + buy)
                self.data.total_lost_val = self.data.total_lost_val+temp2val
                self.data.cost = self.data.cost + self.data.const_val
        else:
            print("价格小于0，可能出现服务器数据错误")

    def analysis_data(self):#分析总数据
        self.data.total_val = self.data.total_win_val - self.data.total_lost_val
        self.data.total_changes = self.data.win_timers + self.data.lost_timers
        if self.data.total_changes !=  0:
            self.data.correct_ratio = (self.data.win_timers/self.data.total_changes)
        else:
            self.data.correct_ratio = 0

        if self.data.win_timers !=  0:
            self.data.avg_win_val = (self.data.total_win_val/self.data.win_timers)
        else:
            self.data.avg_win_val = 0

        if self.data.lost_timers !=  0:
            self.data.avg_lost_val = (self.data.total_lost_val / self.data.lost_timers)
        else:
            self.data.avg_lost_val = 0

        if self.data.avg_lost_val != 0:
            self.data.win_lost_ratio = (self.data.avg_win_val / self.data.avg_lost_val)
        else:
            self.data.win_lost_ratio = 0

        if self.data.cost != 0:
            self.data.win_ratio = self.data.total_val / self.data.cost
        else:
            self.data.win_ratio = 0
        if self.data.avg_lost_val != 0 and self.data.avg_win_val != 0:
            self.data.expect_ratio = (self.data.correct_ratio * (self.data.avg_win_val/self.data.avg_lost_val)) - ((1-self.data.correct_ratio) * (self.data.avg_lost_val/self.data.avg_win_val))
        if self.data.cost!= 0:
            self.data.total_avg_win = (self.data.total_win_val - self.data.total_lost_val) / self.data.cost * 10000

        if self.data.total_changes !=  0:
            self.data.avg_days = self.data.total_days / self.data.total_changes

    def statistics(self,df):
        self.init_data()
        buy = 0
        buyindex = 0
        buyflag = 0
        sale = 0
        saleindex = 0
        saleflag = 1
        for index in df.index:
            if df.loc[index, 'buy'] == '买':
                if saleflag == 1:
                    buy = float(df.loc[index, '收盘'])
                    buyindex = index
                    buyflag = 1
                    saleflag = 0
                else:#error state
                    break
            elif df.loc[index, 'buy'] == '卖':
                if buyflag == 1:
                    sale = float(df.loc[index, '收盘'])
                    saleindex = index
                    buyflag = 0
                    saleflag = 1
                    self.accounts(buy,sale,buyindex,saleindex)
                else:#error state
                    print("买卖数目不匹配，请检查买入策略")
                    break
            else:
                pass
        self.analysis_data()
        return self.data








if __name__ == "__main__":
    StockCodeObj = StockTEST()
    print(StockCodeObj.data.win_lost_ratio)

