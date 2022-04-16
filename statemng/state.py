import json
import pandas as pd
import requests
import calendar
import datetime
import numpy as np
import os
import time

class StateMng:
    def __init__(self):
        curpath = os.getcwd()
        fullpath = curpath + '\\' + "state.csv"
        df = pd.read_csv(fullpath)
        module_name = df.loc[0, 'Module__']
        self.df = df
        self.module = module_name
        self.init_func = "void  " + module_name+"_Init(void)"
        self.main_state_func = "void  " + module_name + "_MainTask(void)"
        self.main_state_type = module_name+"State" +"_e"
        self.main_state_val = module_name + "_mainctrl_status"
        self.main_laststate_val = module_name + "_lastmainctrl_status"
        self.state_table = module_name + "_Func_Tbl"
        self.state_enum_list = []
        for index in df.index:
            if pd.isnull(df.loc[index, 'State__']):
                break
            temp_str = str(df.loc[index, 'State__']) + "_STATE" + "_E_" + str(index)
            self.state_enum_list.append(temp_str)
        self.module_main_state = self.module+"Main_State" +"_e"
        self.handle_func_ptr = self.module + 'State_Handle_Ptr'
        self.func_para = "(" + "STATE_UINT8 "+"channel"+ ")"
        self.handle_table = self.module + "_handle_func_tbl"
        self.maxch = self.module+'Max_CH '
        print("init...")

    def print_main_state_type_def(self,filename):
        print('\n', file=filename)
        print('/***************************enum define begin************************************/', file=filename)
        print('typedef enum{',file=filename)
        for item in self.state_enum_list:
            print("     "   + item+',', file=filename)
        print("}"+self.module_main_state + ";", file=filename)
        print('/***************************enum define end************************************/', file=filename)
        print('\n', file=filename)

    def print_datatype(self,filename):
        print('\n', file=filename)
        print('/***************************datatype define begin************************************/', file=filename)
        print('#define STATE_UINT8 ' + self.df.loc[0, 'datatype__'], file=filename)
        print('#define STATE_SINT8 ' + self.df.loc[1,'datatype__'], file=filename)
        print('#define STATE_UINT16 ' + self.df.loc[2, 'datatype__'], file=filename)
        print('#define STATE_SINT16 ' + self.df.loc[3,'datatype__'], file=filename)
        print('#define STATE_UINT32 ' + self.df.loc[4, 'datatype__'], file=filename)
        print('#define STATE_SINT32 ' + self.df.loc[5,'datatype__'], file=filename)
        print('/***************************datatype define end************************************/', file=filename)
        print('\n', file=filename)

    def print_c_head(self,filename):
        print('#include   "' + self.module +'.h"',file=filename)
        print('/***************************************************************', file=filename)
        print('copyright from private LiuXiao',file=filename)
        print('if you have any question,you can contact me by email 461445092@qq.com', file=filename)
        date = datetime.datetime.now()
        print(date,file=filename)
        print('***************************************************************/', file=filename)

    def print_c_head(self,filename):
        print('#include   "' + self.module +'.h"',file=filename)
        print('/***************************************************************', file=filename)
        print('copyright from private LiuXiao',file=filename)
        print('if you have any question,you can contact me by email 461445092@qq.com', file=filename)
        date = datetime.datetime.now()
        print(date,file=filename)
        print('***************************************************************/', file=filename)

    def print_c_define_mainctrl_val(self, filename):
        print("\n", file=filename)
        print('/***************************************************************/', file=filename)
        print(self.module_main_state + ' ' + self.main_state_val + "["+self.maxch+"]"+";", file=filename)
        print(self.module_main_state + ' ' + self.main_laststate_val + "["+self.maxch+"]"+";", file=filename)
        print('/***************************************************************/', file=filename)

    def print_c_define_statement_func(self, filename):
        print("\n", file=filename)
        print('/***************************static function statement begin************************************/', file=filename)
        for index in df.index:
            if pd.isnull(df.loc[index, 'State__']):
                break
            print('static '+self.module_main_state + ' '+self.module + "_handle_entry_"+str(df.loc[index, 'State__']) + self.func_para+ ";", file=filename)
            print('static '+self.module_main_state + ' '+self.module  + "_handle_during_" + str(df.loc[index, 'State__']) + self.func_para + ";",file=filename)
            print('static '+self.module_main_state + ' '+self.module  + "_handle_exit_" + str(df.loc[index, 'State__']) + self.func_para + ";",file=filename)
            print('\n',file=filename)

        print('/***************************static function statement end  ************************************/', file=filename)
        print("\n", file=filename)

    def print_c_handle_table(self, filename):
        print("\n", file=filename)
        print('/***************************table begin************************************/', file=filename)
        print('const '+self.module_main_state+ " "+self.handle_table+'[' + str(len(self.state_enum_list)) +'][3] = \n {', file=filename)
        for index in df.index:
            if pd.isnull(df.loc[index, 'State__']):
                break
            print('    ('+self.module_main_state + ') '+self.module + "_handle_entry_"+str(df.loc[index, 'State__']) + ",", file=filename)
            print('    (' + self.module_main_state + ') ' + self.module + "_handle_during_" + str(df.loc[index, 'State__']) + ",", file=filename)
            print('    (' + self.module_main_state + ') ' + self.module + "_handle_exit_" + str(df.loc[index, 'State__']) + ",", file=filename)
        print('};\n',file=filename)
        print('/***************************table end  ************************************/', file=filename)
        print("\n", file=filename)

    def print_c_define_func(self, filename):
        print("\n", file=filename)
        print('/***************************static function define begin************************************/', file=filename)
        print("\n\n", file=filename)
        for index in df.index:
            if pd.isnull(df.loc[index, 'State__']):
                break
            print('/***************************'+ str(df.loc[index, 'State__'])+'_entry***********************************/',file=filename)
            print('static '+self.module_main_state + ' '+self.module + "_handle_entry_"+str(df.loc[index, 'State__']) + self.func_para, file=filename)
            print('{\n/*please fill your code*/\n'+'    return '+ self.state_enum_list[0] +';'+'\n}\n\n', file=filename)
            print('/***************************' + str(df.loc[index, 'State__']) + '_during***********************************/', file=filename)
            print('static '+self.module_main_state + ' '+self.module  + "_handle_during_" + str(df.loc[index, 'State__']) + self.func_para,file=filename)
            print('{\n/*please fill your code*/\n'+'    return '+ self.state_enum_list[index] +';'+'\n}\n\n', file=filename)
            print('/***************************' + str(df.loc[index, 'State__']) + '_exit***********************************/', file=filename)
            print('static '+self.module_main_state + ' '+self.module  + "_handle_exit_" + str(df.loc[index, 'State__']) + self.func_para,file=filename)
            print('{\n/*please fill your code*/\n'+'    return '+ self.state_enum_list[0] +';'+'\n}\n\n', file=filename)

        print('\n',file=filename)
        print('/***************************static function define end  ************************************/', file=filename)
        print("\n", file=filename)

    def print_c_define_init_func(self, filename):
        print("\n", file=filename)
        print('/***************************init function define begin************************************/', file=filename)
        print(self.init_func +";", file=filename)
        print('{', file=filename)
        print("    STATE_UINT32 fl_index_u32 = 0;  \n\n    for(fl_index_u32 = 0 ; fl_index_u32 < " + self.maxch + '; fl_index_u32++)',file=filename)
        print("    {", file=filename)
        print("        "+self.main_state_val + '[fl_index_u32]=' + self.state_enum_list[0]+ ';', file=filename)
        print("        " + self.main_laststate_val + '[fl_index_u32]=' + self.state_enum_list[0] + ';', file=filename)
        print('    }', file=filename)

        print('\n}', file=filename)
        print('/***************************init function define end  ************************************/', file=filename)
        print("\n", file=filename)

    def print_c_define_main_func(self, filename):
        print("\n", file=filename)
        print('/***************************main function define begin************************************/', file=filename)
        print(self.main_state_func +";", file=filename)
        print('{', file=filename)
        print("    STATE_UINT32 fl_index_u32 = 0;  \n\n    for(fl_index_u32 = 0 ; fl_index_u32 < " +self.maxch + '; fl_index_u32++)', file=filename)
        print("    {\n",file=filename)

        print("        "+"if("+self.main_state_val+"[fl_index_u32] <= "+ str(self.state_enum_list[len(self.state_enum_list)-1])+")", file=filename)
        print("        {",file=filename)
        print("            "+self.main_state_val+"[fl_index_u32]=" + self.handle_table+"["+self.main_state_val+"[fl_index_u32]]"+"[1]" + "(fl_index_u32)" + ";",file=filename)
        print("        }", file=filename)
        print("        else", file=filename)
        print("        {",file=filename)
        print("            "+self.main_state_val+"[fl_index_u32]=" + self.state_enum_list[0]+";",file=filename)
        print("        }", file=filename)

        print("    \n",file=filename)
        print("        "+"if("+self.main_state_val+"[fl_index_u32] <= "+ str(self.state_enum_list[len(self.state_enum_list)-1])+")", file=filename)
        print("        {",file=filename)
        print("            "+"if("+self.main_laststate_val+"[fl_index_u32] != "+ self.main_state_val+"[fl_index_u32]"+")", file=filename)
        print("            {",file=filename)
        print("                (void)"+self.handle_table+"["+self.main_laststate_val+"[fl_index_u32]]"+"[2]" + "(fl_index_u32)" + ";",file=filename)
        print("            }", file=filename)
        print("        }", file=filename)
        print("        else", file=filename)
        print("        {",file=filename)
        print("            "+self.main_state_val+"[fl_index_u32]=" + self.state_enum_list[0]+";",file=filename)
        print("        }", file=filename)

        print("    \n",file=filename)
        print("        "+"if("+self.main_state_val+"[fl_index_u32] <= "+ str(self.state_enum_list[len(self.state_enum_list)-1])+")", file=filename)
        print("        {",file=filename)
        print("            "+"if("+self.main_laststate_val+"[fl_index_u32] != "+ self.main_state_val+"[fl_index_u32]"+")", file=filename)
        print("            {",file=filename)
        print("                (void)"+self.handle_table+"["+self.main_state_val+"[fl_index_u32]]"+"[0]" + "(fl_index_u32)" + ";",file=filename)
        print("            }", file=filename)
        print("        }", file=filename)
        print("        else", file=filename)
        print("        {",file=filename)
        print("            "+self.main_state_val+"[fl_index_u32]=" + self.state_enum_list[0]+";",file=filename)
        print("        }", file=filename)

        print('    }', file=filename)

        print("    \n",file=filename)
        print("    "+self.main_laststate_val+"[fl_index_u32]="+ self.main_state_val+"[fl_index_u32];", file=filename)

        print('\n}', file=filename)
        print('/***************************main function define end  ************************************/', file=filename)
        print("\n", file=filename)

    def print_h_main_ctrlfunc_type(self, filename):

        print('/*****************************main control function begin**********************************/', file=filename)
        print('typedef  ' + self.module_main_state + "  ( * " + self.handle_func_ptr + ")" + self.func_para+";" ,file=filename)
        print('/*********************************main control function end*******************************/', file=filename)

    def print_h_head(self,filename):
        print('#ifndef (__'+self.module+'_H__)',file=filename)
        print('#define (__' + self.module + '_H__)', file=filename)
        print('/***************************************************************', file=filename)
        print('copyright from private LiuXiao',file=filename)
        print('if you have any question,you can contact me by email 461445092@qq.com', file=filename)
        date = datetime.datetime.now()
        print(date,file=filename)
        print('***************************************************************/', file=filename)
        print('\n\n', file=filename)
        print('#define '+ self.maxch+"  " +str(int(self.df.loc[0,"MaxCh__"])), file=filename)

    def print_h_end(self,filename):
        print("\n", file=filename)
        print('/***************************extern function begin************************************/', file=filename)
        print("extern  "+ self.init_func +";", file=filename)
        print("extern  " + self.main_state_func +";", file=filename)
        print('/***************************extern function end************************************/', file=filename)
        print("\n", file=filename)
        print('#endif', file=filename)

    def print_context(self,str,filename):
        print('str',file=filename)

    def print_n_line_blank(self,n,filename):
        for index in range(0,n):
            print('\n',file=filename)

if __name__ == "__main__":
    curpath = os.getcwd()
    fullpath = curpath + '\\' + "state.csv"
    df = pd.read_csv(fullpath)
    print(df)
    StateMngObj = StateMng()

    module_name = df.loc[0, 'Module__']

    file_h = open(module_name+'.h', 'w')
    file_c = open(module_name+'.c', 'w')

    #output *.h file
    StateMngObj.print_h_head(file_h)
    StateMngObj.print_datatype(file_h)
    StateMngObj.print_main_state_type_def(file_h)
    StateMngObj.print_h_main_ctrlfunc_type(file_h)
    #StateMngObj.print_n_line_blank(3,file_h)
    StateMngObj.print_h_end(file_h)
    print("header file write success...")

    #output *.c file
    StateMngObj.print_c_head(file_c)
    StateMngObj.print_c_define_mainctrl_val(file_c)
    StateMngObj.print_c_define_statement_func(file_c)
    StateMngObj.print_c_handle_table(file_c)
    StateMngObj.print_c_define_func(file_c)
    StateMngObj.print_c_define_init_func(file_c)
    StateMngObj.print_c_define_main_func(file_c)
    print("source file write success...")

    file_h.close()
    file_c.close()
    print("close file success...")





#打包命令
#Pyinstaller -F -w -i chengzi.ico py_word.py
#Pyinstaller -F -c -i chengzi.ico py_word.py