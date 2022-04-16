# 为方便演示, 我们随机生成3列正随机数
from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PyQt5.QtGui import QPixmap
import PySide2.QtGui as QtGui
import fileoperate

class Stats:

    def __init__(self,func_del,func_flash,func_imageshow,func_rmv,func_enter,func_flash_local,func_CodeChanged):
        # 从文件中加载UI定义

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('canlun.ui')
        self.ui.listWidget_Path.setObjectName("pitcure")

        #self.ui.lineEdit_Code.returnPressed.connect(func_enter)


        #self.ui.lineEdit_Flt.returnPressed.connect(func_enter)
        #self.ui.lineEdit_NetWork.returnPressed.connect(func_enter)
        self.ui.lineEdit_Number.returnPressed.connect(func_enter)
        self.ui.pushButton_flash_local.clicked.connect(func_flash_local)
        self.ui.pushButton_dellist.clicked.connect(func_del)
        self.ui.pushButton_flash.clicked.connect(func_flash)
        self.ui.pushButton_rmv_al.clicked.connect(func_rmv)
        self.ui.listWidget_Path.currentItemChanged.connect(func_imageshow)  # 这是点击item会返回item的名称:ps我使用qtDesigner绘制的TabWidget。
        self.ui.comboBox_code.currentIndexChanged.connect(func_CodeChanged)

    def delete_picture(self):
        info = self.ui.lineEdit_Code.text()
        print(info)

    def flash_Qlist(self):
        itemlist = self.Get_Picture_Pathlist()
        for item in itemlist:
            self.ui.listWidget_Path.addItem(item)
        self.ui.label_tip.setStyleSheet("background-color: rgb(0, 250, 0);font-size:16px;color:black");
        self.ui.label_tip.setText("刷新成功")

    def remove(self):
        #info = self.ui.lineEdit_Code.text()
        self.ui.listWidget_Path.clear()
        self.ui.label_tip.setStyleSheet("background-color: rgb(0, 250, 0);font-size:16px;color:black");
        self.ui.label_tip.setText("当前目录已经被清空")


    def image(self):
        print(self.ui.listWidget_Path.currentItem().text())
        imagefile=self.ui.listWidget_Path.currentItem().text()
        png = QtGui.QPixmap(imagefile).scaled(self.ui.label_show.width(), self.ui.label_show.height())
        self.ui.label_show.setPixmap(png)
        self.ui.label_show.setPixmap(png)
        #self.ui.label_show.setStyleSheet("background-color: rgb(250, 0, 0);font-size:16px;color:black");


    def Gui_Show(self):
        #app = QApplication([])
        self.ui.show()
        #app.exec_()


if __name__ == "__main__":

    app = QApplication([])
    stats = Stats()
    stats.ui.show()
    app.exec_()









