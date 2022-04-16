# 为方便演示, 我们随机生成3列正随机数
import pandas as pd

class StockValidK:
    def __init__(self):
        self.df = 0
        self.par = {"up": 1,
               "dn": 0
               }
        self.direct = self.par['up']
        print("stock Valid kline 初始化完成")

    def GetDfLastIndex(self,df):
        for index in df.index:
            pass
        return index

    #获取最小和最大值
    def GetMaxMinVal(self,value1,value2):
        #获取当前有效的K线值
        if value1 >= value2:
            max = value1
            min = value2
        else:
            max = value2
            min = value1
        return max,min

    #处理两个k包含关系
    def GetContainerInfo(self,CurentMax,CurentMin,NextMax,NextMin):
        retval = 0
        p_max = CurentMax
        p_min = CurentMin
        if CurentMax >= NextMax and CurentMin <= NextMin:
            #当前包含下一根k
            retval = 1
            if self.direct == self.par["up"]:
                p_max = CurentMax
                p_min = NextMin
            else:
                p_max = NextMax
                p_min = CurentMin
        elif CurentMax <= NextMax and CurentMin >= NextMin:
            # 当前被下一根k包含
            retval = 2
            if self.direct == self.par["up"]:
                p_max = NextMax
                p_min = CurentMin
            else:
                p_max = CurentMax
                p_min = NextMin
        else:
            #不存在包含关系判断方向
            if CurentMax >= NextMax and CurentMin >= NextMin:
                self.direct = self.par["dn"]
            else:
                self.direct = self.par["up"]

        return retval,p_max,p_min

    def LoopValidK(self,df,last_index):

        #遍历k线
        self.direct = self.par["up"]
        #last_index = self.GetDfLastIndex(df)
        #传如参数df的值无法修改，只能创建新值修改
        df.loc[0, '有效最高'] = float(df.loc[0, '最高'])
        df.loc[0, '有效最低'] = float(df.loc[0, '最低'])
        df.loc[0, 'k方向'] = 'up'

        for index in df.index:
           if index < last_index:
               current_max = float(df.loc[index, '有效最高'])
               current_min = float(df.loc[index, '有效最低'])
               next_max = float(df.loc[index+1, '最高'])
               next_min = float(df.loc[index+1, '最低'])
               #当前K线方向
               if self.direct == self.par["up"]:
                   df.loc[index, 'k方向'] = 'up'
               else:
                   df.loc[index, 'k方向'] = 'dn'
               #获取合并后的K值
               container_type,validmax,validmin = self.GetContainerInfo(current_max , current_min , next_max , next_min)

               #更新下一根K值
               if container_type == 0:
                   df.loc[index, 'k有效位'] = '有效k'
                   df.loc[index + 1, '有效最高'] = next_max
                   df.loc[index + 1, '有效最低'] = next_min
               else:
                   df.loc[index, 'k有效位'] = '无效k'
                   df.loc[index + 1, '有效最高'] = validmax
                   df.loc[index + 1, '有效最低'] = validmin
           else:
               df.loc[index, 'k有效位'] = '有效k'
               df.loc[index, '有效最高'] = float(df.loc[index, '最高'])
               df.loc[index, '有效最低'] = float(df.loc[index, '最低'])
               if self.direct == self.par["up"]:
                   df.loc[index, 'k方向'] = 'up'
               else:
                   df.loc[index, 'k方向'] = 'dn'
        df = df.drop(labels=['最高','最低'], axis=1)  # axis=1 表示按列删除，删除gender列
        df = df.rename(columns={'有效最高': '最高', '有效最低': '最低'})

        return  df







'''
if __name__ == "__main__":
    StockPictureObj = StockPicture()
'''






