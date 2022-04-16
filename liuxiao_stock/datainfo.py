# 为方便演示, 我们随机生成3列正随机数
import os

class dirinfo:
    def __init__(self):
        self.data_dict = {"data":["data",""],
                          "code":["code",""],
                          "cfg" :["config", "cfg.ini"],
                          "klinedata":["data",""],
                          "picture":["picture",""],
                          "csv": ["csv", ""],
                          "Collections": ["Collections", ""]
                          }
        print("data info 数据初始化完成")


if __name__ == "__main__":
    datainfoObj = dirinfo()
    print(datainfoObj.data_dict['data'][0])




