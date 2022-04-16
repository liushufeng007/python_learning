# 为方便演示, 我们随机生成3列正随机数
import os
import shutil
import StockCode
import pandas as pd
import datainfo
from pathlib import Path

class fileoprt:
    def __init__(self):
        self.setpath = ''
        self.current_path = ''
        self.fullpath_filename = ''
        self.StockCodeObj = StockCode.StockCode()

        print("fileoprt 初始化完成")

    def GetSetPath(self):
        return self.setpath

    def SetPath(self, path: str = ''):
        self.current_path = os.getcwd()
        self.setpath = self.current_path + '\\' + path

    def SetFullPath(self,filename:str =''):
        if self.setpath == '':
            print("路径未设定，需要先设置路径")
        else:
            self.fullpath_filename = self.setpath +'\\' + filename

    def TouchSetDir(self):
        # 判断当前路径是否存在
        if os.path.exists(self.setpath):
            pass
        else:
            os.makedirs(self.setpath)

    def Touchfile(self,filepath):
        # 判断当前路径是否存在
        try:
            with open(filepath, 'r') as fh:
                fh.close()
        except:
            filename = open(filepath, 'w')
            filename.close()

    def Createfile(self):
        filename = open(self.fullpath_filename, 'w')
        return filename

    def Closefile(self,file):
        file.close()

    def GetFullPath_Filename(self):
        return self.fullpath_filename

    def GetPath(self):
        return self.fullpath_filename

    def Read_FullPath_File(self,filename):
        templist = []
        with open(filename, 'r') as f1:
            for item in f1.readlines():
                templist.append(item)
        f1.close()
        return templist

    def Read_ValidCode_File(self,codepath):
        df = pd.read_csv(codepath, dtype={"f12":str}, parse_dates=True)
        templist = []
        for index in df.index:
            code = df.loc[index, 'f12']
            name = df.loc[index, 'f14']
            condition = 1
            for key in  self.StockCodeObj.unused_code_dict:
                #print(code , '  ', self.StockCodeObj.unused_code_dict[key])
                if self.StockCodeObj.unused_code_dict[key] in code[0:3]:
                    condition = 0
                else:
                    pass

            if condition == 1:
                item = code + ""+name
                templist.append(item)
        return templist,df

    def Get_Dict_FullPath_Filename(self,path,filename):
        curpath = os.getcwd()
        fullpath = curpath + '\\'+path+'\\' + filename
        return fullpath

    def RemoveDir(self,dir_path):
        try:
            shutil.rmtree(dir_path)
        except:
            print("文件夹：",dir_path,"不存在")

    def Get_Dict_FullPath_Filename(self,path,filename):
        curpath = os.getcwd()
        fullpath = curpath + '\\'+path+'\\' + filename
        return fullpath

    def getallfiles(self,curpath):
        allfile = []
        # 遍历这个路径下的所有路径，文件，文件夹
        for dirpath, dirnames, filenames in os.walk(curpath):
            # for dir in dirnames:
            # allfile.append(os.path.join(dirpath,dir))
            for name in filenames:
                allfile.append(os.path.join(dirpath, name))
        # 返回所有带路径文件名称
        return allfile

    def Get_Picture_Pathlist(self,path):
        currentpath = os.getcwd()
        currentpath = currentpath + '\\'+path
        allfile = self.getallfiles(currentpath)
        return allfile

    def Write_lines(self,filename,f_list):
        with open(filename, 'w') as f1:
            f1.writelines(f_list)
            f1.close()


'''
if __name__ == "__main__":
    fileOperateObj = fileoprt()
    fileOperateObj.SetPath("test\\ok")
    fileOperateObj.SetFullPath("file.txt")
    fileOperateObj.TouchSetDir()
    print(fileOperateObj.fullpath_filename)
    f = fileOperateObj.Createfile()
    fileOperateObj.Closefile(f)
    print("买点来了")
'''


