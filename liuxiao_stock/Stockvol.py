import pandas as pd
import requests
import  json
import time

class StockVol:
    def __init__(self):
        self.EastmoneyKlines = {
                'f51': '日期',
                'f52': '开盘',
                'f53': '收盘',
                'f54': '最高',
                'f55': '最低',
                'f56': '成交量',
                'f57': '成交额',
                'f58': '振幅',
                'f59': '涨跌幅',
                'f60': '涨跌额',
                'f61': '换手率',
            }

        self.urlcode = {
            1 : '35',
            2 : '58',
            3 : '5',
            4 : '46'
        }

        self.EastmoneyHeaders = {
            'Host': 'push2.eastmoney.com',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'http://quote.eastmoney.com/',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62'
        }

        self.url_part0 = 'http://push2.eastmoney.com/api/qt/stock/get?ut=fa5fd1943c7b386f172d6893dbfba10b&invt=2&fltt=2&fields='
        self.url_part1 = 'f43,f57,f58,f169,f170,f46,f44,f51,f168,f47,f164,f163,f116,f60,f45,f52,f50,f48,f167,f117,f71,f161,f49,f530,f135,f136,f137,f138,f139,f141,f142,f144,f145,f147,f148,f140,f143,f146,f149,f55,f62,f162,f92,f173,f104,f105,f84,f85,f183,f184,f185,f186,f187,f188,f189,f190,f191,f192,f107,f111,f86,f177,f78,f110,f262,f263,f264,f267,f268,f250,f251,f252,f253,f254,f255,f256,f257,f258,f266,f269,f270,f271,f273,f274,f275,f127,f199,f128,f193,f196,f194,f195,f197,f80,f280,f281,f282,f284,f285,f286,f287,f292'
        self.url_part2 = '&secid='
        self.url_part3 = '0'
        self.url_part4 = '.'
        self.url_part5 = '000888'
        self.url_part6 = '&cb=jQuery112408530341965801769_1643255915432&_=1643255915433'
        self.url  = ''


        print("klines OBJ 初始化完毕")

    def update_ulr(self,code: str,  kind: int =1):
        self.url_part5 = str(code)
        self.url_part3 = str(kind)
        #拼接url
        self.url = self.url_part0 + self.url_part1+ self.url_part2+ \
                   self.url_part3+ self.url_part4+ self.url_part5+  self.url_part6
        #print(self.url_part3_klt, " ",self.url)
        '''
        http://push2.eastmoney.com/api/qt/stock/get?ut=fa5fd1943c7b386f172d6893dbfba10b&invt=2&fltt=2&fields=f43,f57,f58,f169,f170,f46,f44,f51,f168,f47,f164,f163,f116,f60,f45,f52,f50,f48,f167,f117,f71,f161,f49,f530,f135,f136,f137,f138,f139,f141,f142,f144,f145,f147,f148,f140,f143,f146,f149,f55,f62,f162,f92,f173,f104,f105,f84,f85,f183,f184,f185,f186,f187,f188,f189,f190,f191,f192,f107,f111,f86,f177,f78,f110,f262,f263,f264,f267,f268,f250,f251,f252,f253,f254,f255,f256,f257,f258,f266,f269,f270,f271,f273,f274,f275,f127,f199,f128,f193,f196,f194,f195,f197,f80,f280,f281,f282,f284,f285,f286,f287,f292&secid=0.000888&cb=jQuery112408530341965801769_1643255915432&_=1643255915433
        http://push2.eastmoney.com/api/qt/stock/get?ut=fa5fd1943c7b386f172d6893dbfba10b&invt=2&fltt=2&fields=f43,f57,f58,f169,f170,f46,f44,f51,f168,f47,f164,f163,f116,f60,f45,f52,f50,f48,f167,f117,f71,f161,f49,f530,f135,f136,f137,f138,f139,f141,f142,f144,f145,f147,f148,f140,f143,f146,f149,f55,f62,f162,f92,f173,f104,f105,f84,f85,f183,f184,f185,f186,f187,f188,f189,f190,f191,f192,f107,f111,f86,f177,f78,f110,f262,f263,f264,f267,f268,f250,f251,f252,f253,f254,f255,f256,f257,f258,f266,f269,f270,f271,f273,f274,f275,f127,f199,f128,f193,f196,f194,f195,f197,f80,f280,f281,f282,f284,f285,f286,f287,f292&secid=1.600036&cb=jQuery112405755262098051888_1643251256938&_=1643251256991
        '''
    def get_vol_data(self,code: str) -> pd.DataFrame:
        #尝试最多三次
        for tryindex in range(1,4):
            try:
                if code[0] == '6':
                    #拼接url
                    self.update_ulr(code,1)
                    # 请求数据
                    reponse = requests.get(self.url, headers=self.EastmoneyHeaders)
                else:
                    self.update_ulr(code,0)
                    # 请求数据
                    reponse = requests.get(self.url, headers=self.EastmoneyHeaders)
                #提取字典数据
                data = reponse.text[42:-2]
                #字符串转字典
                reponse_dict = json.loads(data)
                #提取数据
                data = reponse_dict['data']
                break
            except:
                print(code,"  数据请求失败", tryindex  ,"次.",self.url)
                data = None
                #失败了，就等一秒再次尝试重新连接服务器
                time.sleep(1)
        if data is None:
            print(code, " ：数据请求失败,url是：", self.url)
        return data

    def get_condition(self,code):
        data = self.get_vol_data(code)
        '''
        print(data['f168'])#换手率
        print(data['f116']) # 总市值
        print(data['f50'])#量比
        print(data['f170'])  # 涨幅
        '''
        condition = 0
        if data is None:
            pass
        else:
            #print(type(data['f170']))
            if isinstance(data['f170'],float)  and isinstance(data['f168'],float) and isinstance(data['f50'],float)  and isinstance(data['f116'],float):
                #if data['f170'] > 3 and data['f170'] < 5:  # 涨幅3~5%
                    #if data['f168'] > 5 and data['f168'] < 10:#换手率5~10
                        #if data['f50'] > 1 and data['f50'] < 5:  # 量比1~5
                            #if data['f116'] > 5000000000 and data['f116'] < 20000000000:  # 总市值50~200亿
                                #condition = 1
                if data['f116'] > 50000000 :  # 总市值50~200亿
                    condition = 1
            else:
                print(code,"数据没有找到，丢弃此股票！")
        return  condition








'''
if __name__ == "__main__":
    KlineDataObj = KlineData()
    # 股票代码
    code = '002271'
    print(f'正在获取 {code} 的 k线数据......')
    # 根据股票代码、开始日期、结束日期获取指定股票代码指定日期区间的k线数据
    condition = KlineDataObj.get_condition(code)
    # 保存k线数据到表格里面
    #print(condition)
    #df.to_csv(f'{code}.csv', encoding='utf-8-sig', index=None)
    #print(f'股票代码：{code} 的 k线数据已保存到代码目录下的 {code}.csv 文件中')
'''
