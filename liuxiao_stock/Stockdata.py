import pandas as pd
import requests
import  json
import time

class KlineData:
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
            'Host': 'push2his.eastmoney.com',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'http://quote.eastmoney.com/',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53'
        }

        self.SH_EastmoneyHeaders = {
            'Host': '.push2his.eastmoney.com',
            'Accept': 'zh-CN,zh;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Referer': 'http://quote.eastmoney.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
        }

        self.SH_url_Part_2 = 'http://'
        self.SH_url_Part_1 = ''
        self.SH_url_Part0 = ".push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery112404359223404054122_1637716407382&secid=1."
        self.SH_url_part1_code = '000000'
        self.SH_url_part2 = '&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&klt='
        self.SH_url_part3_klt = '101'
        self.SH_url_part4 = '&fqt='
        self.SH_url_part5_fqt = '0'
        self.SH_url_part6 = '&end=20500101&lmt='
        self.SH_url_part7_number = '120'        #爬取的天数
        self.SH_url_part8 = '&_=1637716407413'




        self.url_part0 = 'http://92.push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery112405038487584858229_1637452862689&secid=0.'
        self.url_part1_code = '000000'
        self.url_part2 = '&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&klt='
        self.url_part3_klt = '101'
        self.url_part4 = '&fqt='
        self.url_part5_fqt = '0'
        self.url_part6 = '&end=20500101&lmt='
        self.url_part7_number = '120'        #爬取的天数
        self.url_part8 = '&_=1637452862713'
        self.url  = ''



        '''
        新浪网数据
        https://quotes.sina.cn/cn/api/jsonp_v2.php/var%20_sh000001_15_1646794572798=/CN_MarketDataService.getKLineData?symbol=sh000001&scale=30&ma=no&datalen=2023
        '''
        self.SH_XL_Headers = {
            'authority': 'quotes.sina.cn',
            #'method': 'GET',
            #'path': '/cn/api/jsonp_v2.php/var%20_sh000001_15_1646794572798=/CN_MarketDataService.getKLineData?symbol=sh000001&scale=30&ma=no&datalen=1203',
            'scheme':'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': 'QUOTES-SINA-CN=',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Mobile Safari/537.36 Edg/99.0.1150.30'
       }
        self.url_xl_part0 = 'https://quotes.sina.cn/cn/api/jsonp_v2.php/var%20_sh'
        self.url_xl_part1_code = '000001'
        self.url_xl_part2 = '_15_1646794572798=/CN_MarketDataService.getKLineData?symbol=sh'
        self.url_xl_part3 = '&scale='
        self.url_xl_part4_klt = '30'
        self.url_xl_part5 = '&ma=no&datalen='
        self.url_xl_part6_number = '1203'  # 爬取的天数
        self.url_xl = ''

        print("klines OBJ 初始化完毕")

    def update_ulr(self,code: str, number: int = 400, klt: int = 101, fqt: int = 1):
        self.url_part1_code = str(code)
        self.url_part3_klt = str(klt)
        self.url_part5_fqt = str(fqt)
        self.url_part7_number = str(number)
        #拼接url
        self.url = self.url_part0 + self.url_part1_code+ self.url_part2+ \
                   self.url_part3_klt+ self.url_part4+ self.url_part5_fqt+ \
                   self.url_part6+ self.url_part7_number+ self.url_part8
        #print(self.url_part3_klt, " ",self.url)

    def update_SH_ulr(self,code: str, number: int = 400, klt: int = 101, fqt: int = 1 , urlcode: str = '35'):
        self.SH_url_part1_code = str(code)
        self.SH_url_part3_klt = str(klt)
        self.SH_url_part5_fqt = str(fqt)
        self.SH_url_part7_number = str(number)
        self.SH_url_Part_1 = urlcode
        self.SH_EastmoneyHeaders['Host'] = urlcode+self.SH_EastmoneyHeaders['Host']
        #拼接url
        self.url = self.SH_url_Part_2 + self.SH_url_Part_1 + self.SH_url_Part0 + self.SH_url_part1_code+ self.SH_url_part2+ \
                   self.SH_url_part3_klt+ self.SH_url_part4+ self.SH_url_part5_fqt+ \
                   self.SH_url_part6+ self.SH_url_part7_number+ self.SH_url_part8


    def update_SH_xl_ulr(self,code: str, number: int = 400, klt: int = 30):
        #klt 5 unit= minute
        #    240 = day
        self.url_xl_part0 = 'https://quotes.sina.cn/cn/api/jsonp_v2.php/var%20_sh'
        self.url_xl_part1_code = str(code)
        self.url_xl_part2 = '_15_1646794572798=/CN_MarketDataService.getKLineData?symbol=sh'
        self.url_xl_part3 = '&scale='
        self.url_xl_part4_klt = str(klt)
        self.url_xl_part5 = '&ma=no&datalen='
        self.url_xl_part6_number = str(number)  # 爬取的天数
        self.url_xl = self.url_xl_part0+self.url_xl_part1_code+self.url_xl_part2+self.url_xl_part1_code+self.url_xl_part3+self.url_xl_part4_klt+self.url_xl_part5+self.url_xl_part6_number

    def update_SZ_xl_ulr(self,code: str, number: int = 400, klt: int = 30):
        #klt 5 unit= minute
        #    240 = day
        self.url_xl_part0 = 'https://quotes.sina.cn/cn/api/jsonp_v2.php/var%20_sz'
        self.url_xl_part1_code = str(code)
        self.url_xl_part2 = '_15_1646794572798=/CN_MarketDataService.getKLineData?symbol=sz'
        self.url_xl_part3 = '&scale='
        self.url_xl_part4_klt = str(klt)
        self.url_xl_part5 = '&ma=no&datalen='
        self.url_xl_part6_number = str(number)  # 爬取的天数
        self.url_xl = self.url_xl_part0+self.url_xl_part1_code+self.url_xl_part2+self.url_xl_part1_code+self.url_xl_part3+self.url_xl_part4_klt+self.url_xl_part5+self.url_xl_part6_number


    def get_k_history(self,code: str, number: int = 400, klt: int = 101, fqt: int = 1) -> pd.DataFrame:
        '''
        功能获取k线数据
            code : 6 位股票代码
            beg: 开始日期 例如 20200101
            end: 结束日期 例如 20200201
            klt: k线间距 默认为 101 即日k
                klt:1 1 分钟
                klt:5 5 分钟
                klt:101 日
                klt:102 周
            fqt: 复权方式
                不复权 : 0
                前复权 : 1
                后复权 : 2
        '''
        #定义列名称
        columns = list(self.EastmoneyKlines.values())
        #尝试最多三次
        for tryindex in range(1,4):
            try:
                if code[0] == '6' or code == '000001':
                    #拼接url
                    self.update_SH_ulr(code,number,klt,fqt,self.urlcode[tryindex])
                    # 请求数据
                    reponse = requests.get(self.url, headers=self.SH_EastmoneyHeaders)
                else:
                    self.update_ulr(code,number,klt,fqt)
                    # 请求数据
                    reponse = requests.get(self.url, headers=self.EastmoneyHeaders)
                #提取字典数据
                data = reponse.text[42:-2]
                #print(data)

                #字符串转字典
                reponse_dict = json.loads(data)
                #提取数据
                data = reponse_dict['data']
                #print(data)
                break
            except:
                print(code,"  数据请求失败", tryindex  ,"次.",self.url)
                #print(reponse.text)
                data = None
                #失败了，就等一秒再次尝试重新连接服务器
                #time.sleep(1)

        if data is None:
            df = None
            print("什么数据都没有拉取到，检查一下url：",self.url)
            pass
        else:
            # 提取有效的K线数据
            klines = data['klines']
            #按行转换，放入数据框架
            rows = []
            #print(klines)
            for _kline in klines:
                kline = _kline.split(',')
                rows.append(kline)
                #print(kline)


            if len(rows) < number:
                df = None
                print(code,":次新股，上市天数过少，忽略这个股票！确认一下url是不是可行",self.url)
            else:
                #转换数据格式
                df = pd.DataFrame(rows, columns=columns)
        return df


    def get_xl_k_history(self,code: str, number: int = 50, klt: int = 101, fqt: int = 1) -> pd.DataFrame:

        #尝试最多三次
        for tryindex in range(1,4):
            try:
                if code[0] == '6' or code == '000001':
                    #拼接url
                    self.update_SH_xl_ulr(code,number,klt)
                    print(self.url_xl)
                    #print(self.SH_XL_Headers)
                    # 请求数据
                    reponse = requests.get(self.url_xl,headers = self.SH_XL_Headers,timeout=15)

                else:
                    self.update_SZ_xl_ulr(code,number,klt)
                    # 请求数据
                    reponse = requests.get(self.url_xl,headers = self.SH_XL_Headers,timeout=15)
                #print(reponse.text)
                #提取字典数据
                data_ = reponse.text[81:-2]
                data = pd.read_json(data_,orient ='records')
                break
            except:
                print(code,"  数据请求失败", tryindex  ,"次.",self.url)
                #print(reponse.text)
                data = None
                #失败了，就等一秒再次尝试重新连接服务器
                #time.sleep(1)

        if data is None:
            df = None
            print("什么数据都没有拉取到，检查一下url：",self.url)
            pass
        else:
            df = data
        return df

'''
if __name__ == "__main__":
    KlineDataObj = KlineData()
    # 股票代码
    code = '000895'
    print(f'正在获取 {code} 的 k线数据......')
    # 根据股票代码、开始日期、结束日期获取指定股票代码指定日期区间的k线数据
    df = KlineDataObj.get_k_history(code)
    # 保存k线数据到表格里面
    df.to_csv(f'{code}.csv', encoding='utf-8-sig', index=None)
    print(f'股票代码：{code} 的 k线数据已保存到代码目录下的 {code}.csv 文件中')
'''