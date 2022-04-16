# 为方便演示, 我们随机生成3列正随机数
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import pandas as pd
import Stockdata
import StockCode
import Stockmacd
import fileoperate
import datainfo
import StockPicture
import StockShape
import StockRuntime
import StockValidK
import StockTopBot
import Stockvol
import StockStrategy
import StockTEST
import StockGui
import time

import PySide2.QtGui as QtGui
from PySide2.QtWidgets import QApplication, QMessageBox

from apscheduler.schedulers.blocking import BlockingScheduler
import threading

class Stockmain:
    def __init__(self):
        self.stockcode = StockCode.StockCode()
        self.stockdata = Stockdata.KlineData()
        self.Stockmacd = Stockmacd.Macd()
        self.fileOperateObj = fileoperate.fileoprt()
        self.fileinfoObj = datainfo.dirinfo()
        self.StockPicture = StockPicture.StockPicture()
        self.StockShapeObj = StockShape.StockShape()
        self.StockRuntimeObj = StockRuntime.StockRuntime()
        self.StockValidKObj = StockValidK.StockValidK()
        self.StockTopKObj = StockTopBot.StockTopK()
        self.StockVolObj = Stockvol.StockVol()
        self.StockStrategy = StockStrategy.StockStrategy()
        self.StockTEST = StockTEST.StockTEST()

        self.StockGui  = StockGui.Stats(self.delete_picture,self.flash_Qlist,self.image,self.remove,self.enter,self.flash_local_Qlist,self.QComoBoxChanged)


        self.code = []
        self.match_code = []
        self.pd_list = []
        self.test_cal = False
        self.max_number = 55
        self.data_type = 102
        #0是周K
        #1是缠论
        self.strategy  = 0
        self.flt_list = ["1","5","15","30","60","120","240","1200"]

    def TouchAllDir(self):
        #试图创建所有空文件夹
        for key in self.fileinfoObj.data_dict:
            self.fileOperateObj.SetPath(self.fileinfoObj.data_dict[key][0])
            self.fileOperateObj.TouchSetDir()
            #如果有文件需求，就创建文件
            if self.fileinfoObj.data_dict[key][1] != "":
                self.fileOperateObj.SetFullPath(self.fileinfoObj.data_dict[key][1])
                f = self.fileOperateObj.Createfile()
                f.close()

    def Removefile(self):
        self.fileOperateObj.SetPath(StockObj.fileinfoObj.data_dict['data'][0])
        datapath = StockObj.fileOperateObj.GetSetPath()
        self.fileOperateObj.RemoveDir(datapath)


        self.fileOperateObj.SetPath(StockObj.fileinfoObj.data_dict['picture'][0])
        datapath = StockObj.fileOperateObj.GetSetPath()
        self.fileOperateObj.RemoveDir(datapath)
    def printprice(self):
        clrflag = 0
        while 1:
            time.sleep(2)
            code = self.StockGui.ui.comboBox_code.currentText()
            pre_code = code[:6]
            if len(code) >= 6:
                pre_code = code[:6]
                if pre_code.isdigit():
                    df = self.StockVolObj.get_vol_data(pre_code)
                    if df is None:
                        pass
                    else:
                        if clrflag != 0:
                            clrflag = 0
                            self.StockGui.ui.label_tip.setStyleSheet("background-color: rgb(0, 150, 60);font-size:13px;color:black");
                        else:
                            clrflag = 1
                            self.StockGui.ui.label_tip.setStyleSheet("background-color: rgb(0, 200, 10);font-size:13px;color:black");
                        log = str(df['f57'])+ str(df['f58'])+"  now:"+str(df['f43'])+"  high:"+str(df['f44'])+"  low:"+str(df['f45'])+"  open:"+str(df['f46'])
                        self.StockGui.ui.label_tip.setText(log)
                        #print(df)
            print("printprice.....")



    def loadinfo_ComboBox(self):
        key = 'Collections'
        filepath = StockObj.fileOperateObj.Get_Dict_FullPath_Filename(StockObj.fileinfoObj.data_dict[key][0],'collection.txt')
        StockObj.fileOperateObj.Touchfile(filepath)
        self.fileOperateObj.fullpath_filename = filepath
        f_list = self.fileOperateObj.Read_FullPath_File(self.fileOperateObj.fullpath_filename)
        print(f_list)
        for item in self.flt_list:
            self.StockGui.ui.comboBox_flt.addItem(item)
        self.StockGui.ui.comboBox_flt.setCurrentIndex(3)
        if len(f_list) == 0:
            pass
        else:
            for item in f_list:
                self.StockGui.ui.comboBox_code.addItem(item)
            self.StockGui.ui.comboBox_code.setCurrentIndex(0)

    def update_CollectionCode(self):
        #试图创建所有空文件夹
        code = self.StockGui.ui.comboBox_code.currentText()

        pre_code = code[:6]
        flag = 0
        key = 'Collections'
        self.fileOperateObj.SetPath(self.fileinfoObj.data_dict[key][0])
        self.fileOperateObj.TouchSetDir()
        #如果有文件需求，就创建文件
        if self.fileinfoObj.data_dict[key][0] != "":
            filepath=StockObj.fileOperateObj.Get_Dict_FullPath_Filename(StockObj.fileinfoObj.data_dict[key][0], 'collection.txt')
            self.fileOperateObj.fullpath_filename = filepath
            StockObj.fileOperateObj.Touchfile(filepath)
            f_list = self.fileOperateObj.Read_FullPath_File(self.fileOperateObj.fullpath_filename)

            if len(f_list) == 0:
                pass
            else:
                for item in f_list:
                    if pre_code in item:
                        f_list[f_list.index(item)] = code.replace('\n','') + '\n'
                        flag = 1
                        break
                    else:
                        pass

            if flag == 0:
                f_list.append(code.replace('\n','')+'\n')

            self.StockGui.ui.comboBox_code.clear()
            for item in f_list:
                self.StockGui.ui.comboBox_code.addItem(item)
                if code[:6] in item:
                    self.StockGui.ui.comboBox_code.setCurrentIndex(f_list.index(item))

            print(f_list,"33333333333")
            self.fileOperateObj.Write_lines(self.fileOperateObj.fullpath_filename,f_list)



    def Gen_SZ_ZS_Picture(self,number = 1023,min_type = 30,Code = '000001'):
        SZ_Number = number
        SZ_min_type = min_type
        code = Code.replace('\n','')
        df = self.stockdata.get_xl_k_history(code[:6], SZ_Number, SZ_min_type)
        condition =0
        if df is not None:
            df = df.rename(columns={'day': '日期', 'open': '开盘', 'close': '收盘', 'high': '最高', \
                                          'low': '最低', 'volume': '成交量'})
            df = self.Stockmacd.fill_macd(df)
            df = self.StockValidKObj.LoopValidK(df, SZ_Number - 1)
            df = self.StockTopKObj.updateTopBottomShape(df, SZ_Number - 1)
            df = self.StockTopKObj.update_ZS_df(df)
            self.fileOperateObj.SetPath(StockObj.fileinfoObj.data_dict['picture'][0])
            self.fileOperateObj.SetFullPath(code + str(min_type) + '分钟'+ ".jpg")
            filename = self.fileOperateObj.GetFullPath_Filename()
            df12 = self.Stockmacd.Covert_Macd_df(df)
            self.StockPicture.SavePicture(df12, filename, code+ str(min_type) + '分钟', 1)
            condition = 1
        return condition

    def QComoBoxChanged(self):
        self.StockGui.ui.label_tip.setStyleSheet("background-color: rgb(55, 250, 66);font-size:16px;color:black");
        self.StockGui.ui.label_tip.setText("下拉框活动中")

    def enter(self):
        self.StockGui.ui.label_tip.setStyleSheet("background-color: rgb(55, 250, 66);font-size:16px;color:black");
        self.StockGui.ui.label_tip.setText("按下回车")


    def delete_picture(self):
        #self.StockGui.ui.listWidget_Path.clear()
        code = self.StockGui.ui.comboBox_code.currentText()
        pre_code = code[:6]
        key = 'Collections'
        self.fileOperateObj.SetPath(self.fileinfoObj.data_dict[key][0])
        self.fileOperateObj.TouchSetDir()
        # 如果有文件需求，就创建文件
        if self.fileinfoObj.data_dict[key][0] != "":
            filepath = StockObj.fileOperateObj.Get_Dict_FullPath_Filename(StockObj.fileinfoObj.data_dict[key][0], 'collection.txt')
            self.fileOperateObj.fullpath_filename = filepath
            StockObj.fileOperateObj.Touchfile(filepath)
            f_list = self.fileOperateObj.Read_FullPath_File(self.fileOperateObj.fullpath_filename)
            if len(f_list) == 0:
                self.StockGui.ui.label_tip.setStyleSheet("background-color: rgb(0, 0, 33);font-size:16px;color:black")
                self.StockGui.ui.label_tip.setText("list无需清空")
            else:
                for item in f_list:
                    if pre_code in item:
                        f_list.pop(f_list.index(item))
                        break
                    else:
                        pass
            self.StockGui.ui.comboBox_code.clear()
            for item in f_list:
                self.StockGui.ui.comboBox_code.addItem(item)
            self.fileOperateObj.Write_lines(self.fileOperateObj.fullpath_filename, f_list)

    def flash_Qlist(self):
        # 采用interval固定间隔模式，每隔五秒只执行一次

        self.StockGui.ui.label_tip.setStyleSheet("background-color: rgb(0, 50, 250);font-size:16px;color:black")
        self.StockGui.ui.label_tip.setText("开始刷新")
        code = self.StockGui.ui.comboBox_code.currentText()
        if len(code) >= 6:
            pre_code = code[:6]
            if pre_code.isdigit():
                self.update_CollectionCode()
                #flt = self.StockGui.ui.lineEdit_Flt.text().strip()
                flt = self.StockGui.ui.comboBox_flt.currentText()
                number = self.StockGui.ui.lineEdit_Number.text().strip()

                if flt == '5' or  flt == '1' or  flt == '15' or  flt == '30' or  flt == '60' or  flt == '120'  or  flt == '240':
                    pass
                else:
                   flt = '30'

                num = 1023
                if number != '':
                    num = int(number)
                    if num > 1023:
                        num = 1023

                condition = self.Gen_SZ_ZS_Picture(num, flt,code)
                if condition == 1:
                    self.StockGui.ui.listWidget_Path.clear()
                    itemlist = self.fileOperateObj.Get_Picture_Pathlist(self.fileinfoObj.data_dict['picture'][0])
                    for item in itemlist:
                        self.StockGui.ui.listWidget_Path.addItem(item)
                    self.StockGui.ui.label_tip.setStyleSheet("background-color: rgb(0, 250, 0);font-size:16px;color:black")
                    self.StockGui.ui.label_tip.setText("刷新全部成功")
                else:
                    self.StockGui.ui.label_tip.setStyleSheet("background-color: rgb(255, 0, 0);font-size:16px;color:black")
                    self.StockGui.ui.label_tip.setText("刷新失败请检查网络")
            else:
                self.StockGui.ui.label_tip.setStyleSheet("background-color: rgb(255, 0, 0);font-size:16px;color:black")
                self.StockGui.ui.label_tip.setText("股票代码前6位都应该为数字")
        else:
            self.StockGui.ui.label_tip.setStyleSheet("background-color: rgb(255, 0, 0);font-size:16px;color:black")
            self.StockGui.ui.label_tip.setText("股票代码小于6位")

    def flash_local_Qlist(self):

        self.StockGui.ui.listWidget_Path.clear()

        itemlist = self.fileOperateObj.Get_Picture_Pathlist(self.fileinfoObj.data_dict['picture'][0])
        for item in itemlist:
            self.StockGui.ui.listWidget_Path.addItem(item)
        self.StockGui.ui.label_tip.setStyleSheet("background-color: rgb(99, 250, 77);font-size:16px;color:black")
        self.StockGui.ui.label_tip.setText("刷新全部成功")



    def remove(self):
        #info = self.ui.lineEdit_Code.text()
        self.StockGui.ui.listWidget_Path.clear()
        self.Removefile()
        self.TouchAllDir()
        self.StockGui.ui.label_tip.setStyleSheet("background-color: rgb(44, 250,77);font-size:16px;color:black");
        self.StockGui.ui.label_tip.setText("picture已被清空")


    def image(self):
        #print(self.StockGui.ui.listWidget_Path.currentItem().text())
        imagefile=self.StockGui.ui.listWidget_Path.currentItem().text()
        png = QtGui.QPixmap(imagefile).scaled(self.StockGui.ui.label_show.width(), self.StockGui.ui.label_show.height())
        self.StockGui.ui.label_show.setPixmap(png)
        self.StockGui.ui.label_show.setPixmap(png)




if __name__ == "__main__":
    app = QApplication([])
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = os.path.split(curPath)[0]
    sys.path.append(rootPath)




    StockObj = Stockmain()
    #StockObj.Removefile()
    StockObj.TouchAllDir()
    StockObj.loadinfo_ComboBox()

    thread = threading.Thread(target=StockObj.printprice)
    thread.start()
    print("----------------")

    #查字典获取文件名称
    filename = StockObj.fileOperateObj.Get_Dict_FullPath_Filename(StockObj.fileinfoObj.data_dict['code'][0],'code.txt')
    #更新所有代码到指定路径
    StockObj.stockcode.auto_update_code(filename)
    Codelist,Codedf = StockObj.fileOperateObj.Read_ValidCode_File(filename)

    if StockObj.test_cal == True:
        StockObj.fileOperateObj.SetPath(StockObj.fileinfoObj.data_dict['csv'][0])
        StockObj.fileOperateObj.SetFullPath('TEST.csv')
        StockObj.fileOperateObj.TouchSetDir()
        filename = StockObj.fileOperateObj.GetFullPath_Filename()
        csvfile =  StockObj.fileOperateObj.Createfile()
        print('changes' , \
              ',avg_days',\
              ',win_lost_ratio' , \
              ',correct_ratio', \
              ',expect' , \
              ',avgwin' ,\
              ',avglost' , \
              ',totalwin' , \
              ',maxlost' ,\
              file=csvfile)

   # StockObj.Gen_SZ_ZS_Picture(1023,30)
   # StockObj.Gen_SZ_ZS_Picture(1023,5)
    #StockObj.Gen_SZ_ZS_Picture(1023, 1)

    StockObj.StockGui.Gui_Show()
    app.exec_()

    for CodeItem_i in Codelist:
        break
        CodeItem = CodeItem_i[:6]
        condition =1# StockObj.StockVolObj.get_condition(CodeItem)

        if condition == 1:
            df = StockObj.stockdata.get_k_history(CodeItem, StockObj.max_number, StockObj.data_type)
            if df is None:
                condition = 0
            else:
                if StockObj.test_cal == False:
                    if StockObj.strategy == 0:
                        #df6 = StockObj.StockStrategy.filldata(df)
                        df = StockObj.Stockmacd.fill_macd(df)
                        condition,df6 = StockObj.StockStrategy.getcondition(df)
                    elif StockObj.strategy == 1:
                        df = StockObj.Stockmacd.fill_macd(df)
                        validk_df = StockObj.StockValidKObj.LoopValidK(df,StockObj.max_number-1)
                        df6 = StockObj.StockTopKObj.updateTopBottomShape(validk_df,StockObj.max_number-1)
                        df6 = StockObj.StockTopKObj.update_ZS_df(df6)
                        condition = StockObj.StockTopKObj.GetCondition(df6)
                    else:
                        condition = 0



                if StockObj.test_cal == True:
                    condition ,df1= StockObj.StockStrategy.getcondition(df)
                    condition = 0
                    data = StockObj.StockTEST.statistics(df1)
                    print(CodeItem,'  机会：%-5s'%(data.total_changes), \
                          '平均持有：%-10.3f' % (data.avg_days), \
                          ',盈亏比：%-10.3f'%(data.win_lost_ratio),',准确率：%-10.3f'%(data.correct_ratio),\
                          ',期望值：%-10.3f'%(data.expect_ratio), \
                          ',平均盈利：%-10.3f' % (data.avg_win_val),
                          ',平均亏损：%-10.3f' % (data.avg_lost_val), \
                          ',总均盈利：%-10.3f' % (data.total_avg_win), \
                          ',最大亏损：%-10.3f' % (data.max_lost_val), \
                          )
                    print('%-5s'%(data.total_changes), \
                          ',%-10.3f'% (data.avg_days), \
                          ',%-10.3f'%(data.win_lost_ratio),\
                          ',%-10.3f'%(data.correct_ratio),\
                          ',%-10.3f'%(data.expect_ratio), \
                          ',%-10.3f' % (data.avg_win_val),
                          ',%-10.3f' % (data.avg_lost_val), \
                          ',%-10.3f' % (data.total_avg_win),\
                          ',%-10.3f' % (data.max_lost_val), \
                          file=csvfile)
                    if data.total_changes != 0:
                        pd.set_option('display.max_colwidth', 500)
                        pd.set_option('display.max_rows', None)
                        #print(df)

        if Codelist.index(CodeItem_i) % 100 == 0:
            print("总共有",len(Codelist),"个","当前是第",Codelist.index(CodeItem_i),"个",end='  ,')
            StockObj.StockRuntimeObj.PrintRunTime(len(Codelist),Codelist.index(CodeItem_i))



        if condition >= 1:
            print("到买点了，需要关注:",CodeItem)
            if 0:#"002114" in CodeItem:
                pd.set_option('display.max_colwidth', 500)
                pd.set_option('display.max_rows', 500)
                print(df6)
            if StockObj.strategy == 0:
                StockObj.fileOperateObj.SetPath(StockObj.fileinfoObj.data_dict['picture'][0])
                StockObj.fileOperateObj.SetFullPath(CodeItem_i + ".jpg")
                filename = StockObj.fileOperateObj.GetFullPath_Filename()
                df2 = StockObj.Stockmacd.Covert_Macd_df(df6)
                StockObj.StockPicture.SavePicture(df2, filename, CodeItem_i,StockObj.strategy)
            elif StockObj.strategy == 1:
                StockObj.fileOperateObj.SetPath(StockObj.fileinfoObj.data_dict['picture'][0])
                StockObj.fileOperateObj.SetFullPath(CodeItem_i + ".jpg")
                filename = StockObj.fileOperateObj.GetFullPath_Filename()
                df2 = StockObj.Stockmacd.Covert_Macd_df(df6)
                StockObj.StockPicture.SavePicture(df2, filename, CodeItem_i,StockObj.strategy)
            else:
                pass

    if StockObj.test_cal == True:
        StockObj.fileOperateObj.Closefile(csvfile)









