# 为方便演示, 我们随机生成3列正随机数
import time



class StockRuntime:
    def __init__(self):
        self.start_T = time.time()
        self.end_T = time.time()
        print("时间统计模块 初始化完成")

    def PrintRunTime(self,maxlen,index):
        self.end_T = time.time()
        diff_T = self.end_T - self.start_T
        diff_Min = round(diff_T / 60)
        diff_Sec = round(diff_T % 60)
        if index == 0 or maxlen == 0:
            print("当前程序运行了：", diff_Min, "分钟,", diff_Sec, "秒钟！")
        else:
            total_T = diff_T * maxlen / index
            rest_T  = total_T - diff_T
            rest_Min = round(rest_T / 60)
            rest_Sec = round(rest_T % 60)
            print("当前程序运行了：",diff_Min,"分钟,",diff_Sec,"秒钟！","预计还有:",rest_Min,"分钟,",rest_Sec,"秒钟！")






'''
if __name__ == "__main__":
    StockPictureObj = StockPicture()
'''






