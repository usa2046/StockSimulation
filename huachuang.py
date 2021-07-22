#import requests, json
#
#url="http://webapi.cninfo.com.cn/api/stock/p_stock2101"
#headers={}
#requests_param = {
#    "client_id": "E9TMsWuPTHIbY4XwgIOywN8T7bO3rFaN",
#    "client_secret": "HJVA1VnAl4YJ8ek7INkPunSa1FvdKVhe",
#    "scode": "002812",
#    "format": "json"
#}
#response = requests.post(url=url, data=json.dumps(requests_param))
#print(response.text)

import pywinauto
import pywinauto.clipboard
import pywinauto.application
from pywinauto.application import Application
import time

import cv2
import numpy as np
from PIL import ImageGrab

def Color():
    print("\033[1;30m 字体颜色30m \033[0m")
    print("\033[1;31m 字体颜色31m \033[0m")
    print("\033[1;32m 字体颜色32m \033[0m")
    print("\033[1;33m 字体颜色33m \033[0m")
    print("\033[1;34m 字体颜色34m \033[0m")
    print("\033[1;35m 字体颜色35m \033[0m")
    print("\033[1;36m 字体颜色36m \033[0m")
    print("\033[1;37m 字体颜色37m \033[0m")
    print("\033[1;38m 字体颜色38m \033[0m")

    print(" 背景颜色40m \033[1;40m    \033[0m")
    print(" 背景颜色41m \033[1;41m    \033[0m")
    print(" 背景颜色42m \033[1;42m    \033[0m")
    print(" 背景颜色43m \033[1;43m    \033[0m")
    print(" 背景颜色44m \033[1;44m    \033[0m")
    print(" 背景颜色45m \033[1;45m    \033[0m")
    print(" 背景颜色46m \033[1;46m    \033[0m")
    print(" 背景颜色47m \033[1;47m    \033[0m")

def printc(type, str):
    if type == 1: # 卖
        print("\033[1;31m%s\033[0m" % (str))
    elif type == -1: # 买
        print("\033[1;32m%s\033[0m" % (str))
    elif type == 2: # except
        print("\033[1;37m%s\033[0m" % (str))
    else:
        print("\033[1;38m%s\033[0m" % (str))


class HuaChuang():
    app = None

    def __init__(self):
        try:
            self.app = pywinauto.application.Application()
            self.app.connect(title='网上股票交易系统5.0')
            self.top_hwnd = pywinauto.findwindows.find_window(title='网上股票交易系统5.0')
            self.dialog_hwnd = pywinauto.findwindows.find_windows(top_level_only=False, class_name='#32770', parent=self.top_hwnd)[0]
            self.main_win = self.app.window(handle=self.top_hwnd)
            self.dialog_win = self.app.window(handle=self.dialog_hwnd)
            self.tree_win = self.main_win.child_window(class_name="SysTreeView32")
            printc(0, "已连接股票交易软件！")
        except:
            printc(0, "请先打开交易软件并登录！")
            exit(0)

    def pop_up_window_confirmation(self, type=0):
        '''弹出窗口中确认交易，有两次弹框
        :param type: 0-买卖单弹出框 1-全撤单弹出框
        '''

        while True:
            try:
                top = pywinauto.findwindows.find_windows(top_level_only=True, class_name='#32770')[0]
                top_win = self.app.window(handle=top)
                time.sleep(0.1)
                if type == 0:
                    top_win.Button0.click()
                else:
                    top_win.Button3.click()
                printc(0, ">> Pop up window confirmation 1")
                break
            except:
                printc(2, "except: Pop up window confirmation 1")
                time.sleep(0.5)
        while True:
            try:
                top = pywinauto.findwindows.find_windows(top_level_only=True, class_name='#32770')[0]
                top_win = self.app.window(handle=top)
                time.sleep(0.1)
                top_win.Button0.click()
                printc(0, ">> Pop up window confirmation 2")
                break
            except:
                printc(2, "excpet: Pop up window confirmation 2")
                time.sleep(0.5)

    def buy(self, code, price, num):
        '''买入
        :param code:  股票代码
        :param price: 股票价格
        :param num:   股票数量
        '''
        self.tree_win.get_item(r"\买入[F1]").click()
        while True:
            try:
                self.dialog_hwnd = pywinauto.findwindows.find_windows(top_level_only=False,
                                                                      class_name='#32770',
                                                                      parent=self.top_hwnd)[0]
                self.dialog_win = self.app.window(handle=self.dialog_hwnd)
                self.dialog_win.Edit1.set_edit_text(code)
                time.sleep(0.1) # 价格有初始值，延迟长点避免叠加
                self.dialog_win.Edit2.set_edit_text(price)
                self.dialog_win.Edit3.set_edit_text(num)
                self.dialog_win.Button1.click()
                printc(0, ">> Press 'buy' button")
                break
            except:
                printc(2, "except: Press 'buy' button")
                time.sleep(0.5)
        self.pop_up_window_confirmation()
        printc(-1, "[买入委托] 代码：%8s 价格：%8s 数量：%8s 市值：%d" %
               (code.ljust(8), price.ljust(8), num.ljust(8), float(price)*int(num)))

    def sell(self, code, price, num):
        '''卖出
        :param code:  股票代码
        :param price: 股票价格
        :param num:   股票数量
        '''
        self.tree_win.get_item(r"\卖出[F2]").click()
        while True:
            try:
                self.dialog_hwnd = \
                    pywinauto.findwindows.find_windows(top_level_only=False, class_name='#32770', parent=self.top_hwnd)[0]
                self.dialog_win = self.app.window(handle=self.dialog_hwnd)
                self.dialog_win.Edit1.set_edit_text(code)
                time.sleep(0.1) # 价格有初始值，延迟长点避免叠加
                self.dialog_win.Edit2.set_edit_text(price)
                self.dialog_win.Edit3.set_edit_text(num)
                self.dialog_win.Button1.click()
                printc(0, ">> Press 'sell' button")
                break
            except:
                printc(2, "except: Press 'sell' button")
                time.sleep(0.5)
        self.pop_up_window_confirmation()
        printc(1, "[卖出委托] 代码：%8s 价格：%8s 数量：%8s 市值：%d" %
               (code.ljust(8), price.ljust(8), num.ljust(8), float(price)*int(num)))

    def cancellations(self):
        '''全撤
        '''
        self.dialog_hwnd = \
            pywinauto.findwindows.find_windows(top_level_only=False, class_name='#32770', parent=self.top_hwnd)[0]
        self.dialog_win = self.app.window(handle=self.dialog_hwnd)
        time.sleep(0.1)  # 价格有初始值，延迟长点避免叠加
        self.dialog_win.Button4.click()
        self.pop_up_window_confirmation(type=1)
        printc(1, "[委托全撤] 所有委托单已撤销")

    def exception_dell(self):
        '''异常处理，关闭所有弹出窗口，检查数据，恢复异常'''
        pass

    def read_stock(self):
        '''读取持有股票信息
        '''
        self.dialog_win.CVirtualGridCtrl.right_click(coords=(30, 30))
        self.main_win.type_keys('C')
        data = pywinauto.clipboard.GetData()
        print(data)
        #self.stock_hwnd = \
        #    pywinauto.findwindows.find_windows(top_level_only=False, class_name='CVirtualGridCtrl', parent=self.top_hwnd)[0]
        #self.stock_win = self.app.window(handle=self.stock_hwnd)
        #print(self.stock_win.print_control_identifiers())

if __name__ == "__main__":
    huachuang = HuaChuang()
    #huachuang.buy("000027", "9.54", "100")
    #huachuang.sell("002497", "24.9", "100")
    #huachuang.cancellations()
    huachuang.read_stock()
    #img = ImageGrab.grab(bbox=(0, 0, 100, 100))
    #img = np.array(img.getdata(), np.uint8).reshape(img.size[1], img.size[0], 3)
    #cv2.imshow("1", img)
    #cv2.waitKey(0)





