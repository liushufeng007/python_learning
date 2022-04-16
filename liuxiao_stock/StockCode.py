import requests
import re
import os
import json
import pandas as pd
from pandas.io.json import json_normalize


class StockCode:
    def __init__(self):
        self.pre_url = 'http://push2.eastmoney.com/api/qt/clist/get?cb=jQuery11230016586148909391918_1634227877970&fid=f184&po=1&pz=50&pn='
        self.last_url = '&np=1&fltt=2&invt=2&fields=f2%2Cf3%2Cf12%2Cf13%2Cf14%2Cf62%2Cf184%2Cf225%2Cf165%2Cf263%2Cf109%2Cf175%2Cf264%2Cf160%2Cf100%2Cf124%2Cf265%2Cf1&ut=b2884a393a59ad64002292a3e90d46a5&fs=m%3A0%2Bt%3A6%2Bf%3A!2%2Cm%3A0%2Bt%3A13%2Bf%3A!2%2Cm%3A0%2Bt%3A80%2Bf%3A!2%2Cm%3A1%2Bt%3A2%2Bf%3A!2%2Cm%3A1%2Bt%3A23%2Bf%3A!2%2Cm%3A0%2Bt%3A7%2Bf%3A!2%2Cm%3A1%2Bt%3A3%2Bf%3A!2'
        self.npage_url = ''
        self.unused_code_dict = {1:"300",2:"688",3:"301",4:"900"}
        self.EastmoneyHeaders = {
            'Host': 'push2.eastmoney.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.47',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'http://data.eastmoney.com/',
            }
        self.df = pd.DataFrame()
        print("StcokCode 类初始化完成")

    #组装url，根据页编号更新到npagenum_url变量中
    def update_npage_url(self,pagenumber):
        self.npage_url = self.pre_url + str(pagenumber)+self.last_url

    #获取股票编号是否是有用的
    def get_code_is_valid(self,item):
        retval = 1
        #过滤掉创业版本
        for key in self.unused_code_dict:
            # 过滤掉
            if self.unused_code_dict[key] in item[:3]:
                retval = 0
            #有效的股票编号
            else:
                pass
        return retval

    #获取一个网页中的代码所有的股票编号
    def get_onepage_code(self,pagenumber):
        #更新页编号
        self.update_npage_url(pagenumber)

        #获取网页数据股票编号
        reponse = requests.get( self.npage_url, headers=self.EastmoneyHeaders)
        #数据格式转换
        self.reponse_str = reponse.text
        # 提取字典数据
        data_dict = reponse.text[44:-2]
        # 字符串转字典
        reponse_dict = json.loads(data_dict)
        # 提取数据
        data = reponse_dict['data']
        print("当前已经更新到第 "+str(pagenumber)+" 页了！")
        return data

    #获取整个A股的所有股票编号
    def get_allpage_code(self):
        allcode = []
        allrows = []
        #一页一页的获取股票代码，最终放到list中
        for i in range(1, 200):
            data = self.get_onepage_code(i)
            if data != None:
                data_dif = data['diff']
                for item in data_dif:
                    allrows.append(item)
            else:
                print("当前网页所有股票代码数据已经更新完毕。")
                break
        pd1 = pd.DataFrame(allrows)
        return pd1

    #把所有的代码存到指定文件路径
    def save_code(self,filename_path,df):
        df.to_csv(filename_path, encoding='utf-8-sig', index=None)
        return True

    def auto_update_code(self,filename):
        # 判断当前路径是否存在
        if os.path.exists(filename):
            print("股票代码已经存在不需要更新了！")
            pass
        else:
            # 拆分文件路径信息，获取文件路径和文件名称
            (file_path, tempfilename) = os.path.split(filename)
            if os.path.exists(file_path):
                pass
            else:
                print("文件夹不存在，重新创建")
                # 路径不存在就创建此路径，创建多层路径
                os.makedirs(file_path)
            # 获取网页所有的股票代码
            pd1 = self.get_allpage_code()
            self.save_code(filename, pd1)


'''
if __name__ == "__main__":
    StockCodeObj = StockCode()
    # 获取当前路径
    current_path = os.getcwd()
    Target_path = current_path + "\code\code.txt"
    StockCodeObj.auto_update_code(Target_path)
'''