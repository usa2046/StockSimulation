import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from windowUI import Ui_MainWindow
from TushareData import TuShareData
import numpy as np
#from PyechartsData import KLineHtml
from PyechartsData2 import saveToHtml
import time
import threading
import math


class StockSimulation(QMainWindow, Ui_MainWindow):
    tu = TuShareData()
    klinehtml = saveToHtml()
    #klinehtml = KLineHtml()
    datafram = [] # tushare 数据
    kline_data_ori = []
    kline_data_cur = []
    kline_index = 0
    money_distr = 200000 # 可分配资金
    money_market = 0 # 市值
    holding_num = 0 # 持股数量
    position_cost = 0 # 持仓成本  （总支出-总收入）
    price = 0 # 当前股票价格
    price_change = 0.0 # 股价波动
    buy_num_temp = 0  # 准备购买的股数
    buy_money_temp = 0  # 准备购买的金额
    sell_num_temp = 0 # 准备卖的股数
    sell_money_temp = 0 # 准备卖的金额
    stock_cost_list = []    # 股票成本   持仓成本/持股数量
    money_distr_list = []
    money_market_list = []
    predict_op = 0 # 预测结果（操作）
    predict_state = 0 # 0 待预测   1 已预测，待执行
    auto_predict_state = 0 # 0 未运行  1 运行中
    ave_p = 0
    lbuy_p = 0
    lsell_p = 0
    last_money_all = 0
    high_p = 0


    def __init__(self, *args, **kwargs):
        super(StockSimulation, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.initUI()
        self.initEvent()

    def initData(self):
        self.money_distr = 100000 # 可分配资金
        self.money_market = 0 # 市值
        self.holding_num = 0 # 持股数量
        self.position_cost = 0 # 持仓成本  （总支出-总收入）
        self.price = 0 # 当前股票价格
        self.buy_num_temp = 0  # 准备购买的股数
        self.buy_money_temp = 0  # 准备购买的金额
        self.sell_num_temp = 0 # 准备卖的股数
        self.sell_money_temp = 0 # 准备卖的金额
        self.stock_cost_list = []    # 股票成本   持仓成本/持股数量
        self.money_distr_list = []
        self.money_market_list = []
        self.predict_op = 0 # 预测结果（操作）
        self.predict_state = 0 # 0 待预测   1 已预测，待执行
        self.auto_predict_state = 0 # 0 未运行  1 运行中
        self.ave_p = 0
        self.lbuy_p = 0
        self.lsell_p = 0
        self.last_money_all = 0
        self.high_p = 0

    def initEvent(self):
        self.pushButton_reset.clicked.connect(self.EventButtonResetClicked)
        self.pushButton_keep.clicked.connect(self.EventPushbuttonKeepClicked)
        self.horizontalSlider_buy.sliderMoved.connect(self.EventSliderBuyModed)
        self.horizontalSlider_sell.sliderMoved.connect(self.EventSliderSellModed)
        self.pushButton_buy.clicked.connect(self.EventPushbuttonBuyClicked)
        self.pushButton_sell.clicked.connect(self.EventPushbuttonSellClicked)
        self.pushButton_predict.clicked.connect(self.EventPushbuttonPredictClicked)
        self.pushButton_auto_predict.clicked.connect(self.EventPushbuttonAutoPredictClicked)

    def initUI(self):
        self.browser = QWebEngineView()
        #self.browser.load(QUrl('file:///C:/Users/%E8%B0%AD%E9%94%90/Desktop/LKfilter/data3.html'))
        self.browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        widget_info = QWidget()
        widget_info2 = QWidget()
        widget_buy = QWidget()
        widget_sell = QWidget()
        widget_predict = QWidget()
        widget_info.setLayout(self.horizontalLayout_info)
        widget_info2.setLayout(self.horizontalLayout_info2)
        widget_buy.setLayout(self.horizontalLayout_buy)
        widget_sell.setLayout(self.horizontalLayout_sell)
        widget_predict.setLayout(self.horizontalLayout_predict)
        self.verticalLayout.addWidget(widget_info)
        self.verticalLayout.addWidget(widget_info2)
        self.verticalLayout.addWidget(self.browser)
        self.verticalLayout.addWidget(widget_buy)
        self.verticalLayout.addWidget(widget_sell)
        self.verticalLayout.addWidget(widget_predict)
        self.centralwidget.setLayout(self.verticalLayout)

        self.lineEdit_Id.setText("002230.SZ")
        self.lineEdit_start_time.setText('20190101')
        self.lineEdit_end_time.setText('20200601')

        self.EventButtonResetClicked()


    def getTushareData(self, ts_code, start_date, end_date):
        # 获取的原始数据
        df = self.tu.getDaily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        self.datafram = df
        n0 = df.values[:, 1:2]
        n1 = df.values[:, 2:3]
        n2 = df.values[:, 3:4]
        n3 = df.values[:, 4:5]
        n4 = df.values[:, 5:6]
        n5 = df.values[:, 9:10]
        num = np.hstack((n0, n1, n4, n3, n2, n5))
        self.kline_data_ori = []
        for i in range(len(num)):
            self.kline_data_ori.append(num[len(num)-i-1, :])
        self.kline_data_ori = np.array(self.kline_data_ori)


    def creatHtml(self):
        # 压入其他指标
        data = np.hstack((self.kline_data_cur, np.array(self.stock_cost_list)))
        data = np.hstack((data, np.array(self.money_market_list)))
        data = np.hstack((data, np.array(self.money_distr_list)))
        data = self.klinehtml.split_data(data.tolist())
        self.klinehtml.draw_charts(data)
        dir_path = os.path.dirname(os.path.abspath(__file__))
        dir_path = os.path.join(dir_path, "data.html")
        #self.browser.load(QUrl('file:///C:/Users/98548/Desktop/LKfilter/data3.html'))
        self.browser.load(QUrl.fromLocalFile(dir_path))

    def EventButtonResetClicked(self):
        self.initData()
        self.getTushareData(self.lineEdit_Id.text(), self.lineEdit_start_time.text(), self.lineEdit_end_time.text())
        self.kline_data_cur = self.kline_data_ori[0:20, :]
        self.price = self.kline_data_cur[-1, 2]
        for _ in range(20):
            self.stock_cost_list.append([self.price])
            self.money_market_list.append([0])
            self.money_distr_list.append([self.money_distr])
        self.kline_index = 20
        self.creatHtml()

    def onoDayPast(self):
        if self.kline_index >= len(self.kline_data_ori):
            return
        self.kline_data_cur = np.vstack((self.kline_data_cur,
                                         self.kline_data_ori[self.kline_index:self.kline_index+1, :]))
        self.kline_index += 1
        if self.price != 0:
            self.price_change = (self.kline_data_cur[-1, 2] - self.price) / self.price
        self.price = self.kline_data_cur[-1, 2] # 获取当前股价
        self.ave_p = 0
        self.ave_p += self.kline_data_cur[-1, 2]
        self.ave_p += self.kline_data_cur[-2, 2]
        self.ave_p += self.kline_data_cur[-3, 2]
        self.ave_p += self.kline_data_cur[-4, 2]
        self.ave_p += self.kline_data_cur[-5, 2]
        self.ave_p = self.ave_p / 5

    def printInfo(self):
        print("------------------------------------")
        print("总值     ：", self.money_market + self.money_distr)
        print("可分配资金：", self.money_distr)
        print("市值     ：", self.money_market)
        #print("股价成本  ：", self.stock_cost)
        print("当前股价  ：", self.price)

    def refreshLabelInfo(self):
        self.label_price.setText(str(self.price))
        self.label_price_change.setText(str('%.2f' %(self.price_change * 100)))
        self.label_money_all.setText(str(int(self.money_distr + self.money_market)))
        self.label_market.setText(str(int(self.money_market)))
        self.label_hold_num.setText(str(self.holding_num))

    def EventSliderBuyModed(self):
        value = self.horizontalSlider_buy.value()
        value = self.money_distr * value / 1000
        self.buy_num_temp = int((value + 1) / (self.price * 100)) * 100 # 准备购买的股数
        self.buy_money_temp = self.buy_num_temp * self.price
        self.label_buy.setText(str(int(self.buy_money_temp)))


    def EventSliderSellModed(self):
        if self.holding_num == 0:
            self.label_sell.setText(str(0))
            return
        value = self.horizontalSlider_sell.value()
        self.sell_num_temp = int(self.holding_num / 100 * value / 1000 + 1) * 100 # 准备卖出的股数
        self.sell_money_temp = self.sell_num_temp / self.holding_num * self.money_market # 准备卖出的金额
        self.label_sell.setText(str(int(self.sell_money_temp)))

    def EventPushbuttonBuyClicked(self):
        if self.kline_index >= len(self.kline_data_ori):
            return
        if self.buy_num_temp == 0:
            return
        self.holding_num += self.buy_num_temp
        self.position_cost += self.buy_money_temp
        self.stock_cost_list.append([float('%.2f' % (self.position_cost / self.holding_num))])
        self.money_distr -= self.buy_money_temp
        self.onoDayPast() # 过了一天，股价变化
        self.money_market = self.holding_num * self.price # 计算市值
        self.money_market_list.append([self.money_market])
        self.money_distr_list.append([self.money_distr])
        self.creatHtml()
        self.EventSliderBuyModed()
        self.EventSliderSellModed()
        self.printInfo()
        self.refreshLabelInfo()
        self.resetButtonStyleSeet()

    def EventPushbuttonSellClicked(self):
        if self.kline_index >= len(self.kline_data_ori):
            return
        if self.money_market <= 0:
            return
        if self.sell_num_temp == 0:
            return
        self.holding_num -= self.sell_num_temp
        self.position_cost -= self.sell_money_temp
        if self.holding_num == 0:
            self.stock_cost_list.append(self.stock_cost_list[-1])
            self.position_cost = 0 # 清空持仓成本，因为清仓时这个值不一定为空
        else:
            self.stock_cost_list.append([float('%.2f' % (self.position_cost / self.holding_num))])
        self.money_distr += self.sell_money_temp
        self.onoDayPast()
        self.money_market = self.holding_num * self.price # 计算市值
        self.money_market_list.append([self.money_market])
        self.money_distr_list.append([self.money_distr])
        self.creatHtml()
        self.EventSliderBuyModed()
        self.EventSliderSellModed()
        self.printInfo()
        self.refreshLabelInfo()
        self.resetButtonStyleSeet()

    def EventPushbuttonKeepClicked(self):
        if self.kline_index >= len(self.kline_data_ori):
            return
        self.stock_cost_list.append(self.stock_cost_list[-1])
        self.onoDayPast()
        self.money_market = self.holding_num * self.price # 计算市值
        self.money_market_list.append([self.money_market])
        self.money_distr_list.append([self.money_distr])
        self.creatHtml()
        self.EventSliderBuyModed()
        self.EventSliderSellModed()
        self.printInfo()
        self.refreshLabelInfo()
        self.resetButtonStyleSeet()


    def resetButtonStyleSeet(self):
        self.pushButton_buy.setStyleSheet("")
        self.pushButton_sell.setStyleSheet("")
        self.pushButton_keep.setStyleSheet("")
        self.pushButton_predict.setStyleSheet("")
        self.pushButton_predict.setText("预测")
        self.predict_state = 0

    def doPredict2(self):
        cost_p = self.stock_cost_list[-1][0]
        # 第一次买入
        if self.price < 0.97 * self.ave_p and self.holding_num == 0:
            self.lbuy_p = self.price
            self.lsell_p = self.price
            self.last_money_all = self.money_distr
            return 1, self.money_distr * 0.3
        if self.holding_num == 0:
            return 0, 0
        # 买入
        if self.price < cost_p:
            self.lsell_p = self.price
            self.high_p = self.price
            if self.money_distr + self.money_market < 0.3 * self.last_money_all:
                return -1, self.money_market
            if self.lbuy_p - self.price > 0.05 * cost_p:
                rate = (cost_p - self.price) / cost_p
                va = self.money_distr * (math.exp(4 * rate) - 1)/ 3
                self.lbuy_p = self.price
                if va / self.price < 100:
                    return 0, 0
                return 1, va
        # 卖出
        else:
            if self.price > self.high_p:
                self.high_p = self.price
            if self.price - self.lsell_p > 0.02 * cost_p:
                self.lbuy_p = self.price
                rate = (self.price - cost_p) / cost_p
                va = self.money_market * (math.exp(1 * rate) - 1) / 3
                self.lsell_p = self.price
                if va / self.price < 100:
                    return 0, 0
                return -1, va
            if self.high_p - self.price > 0.05 * self.high_p:
                rate = (self.high_p - self.price) / self.high_p
                va = self.money_distr * (math.exp(4 * rate) - 1)/3
                self.high_p = self.price
                self.lbuy_p = self.price
                return 1, va

        return 0, 0



    def doPredict(self):
        '''
        :return: 参数1：-1卖出 0保持 1买入     参数2：操作金额
        '''
        op = 0 # 操作类型
        va = 0 # 金额
        stock_cost = self.stock_cost_list[-1][0] # 股票成本
        # 入仓点
        if self.price_change < -0.01 and self.holding_num == 0:
            op = 1
            va = self.price * 200 # 买入100股
            return op, va
        # 买
        if self.price_change <= -0.02 or (stock_cost - self.price)/stock_cost >= 0.04:
            a = stock_cost
            b = self.price
            n = self.holding_num
            r = 0.6 # 股票成本和当前价格的接近率
            p = b + (a - b) * r
            m = n * (a - p) / (p - b) # 需要购买的股数
            m = int(m / 100 + 1) * 100
            op = 1
            va = self.price * m
            print(m, va, self.money_distr)
            if m > 100 and va < self.money_distr:
                return op, va
            else:
                op = 0
        # 卖
        if (self.price - stock_cost)/stock_cost > 0.03 and self.holding_num > 0:
            op = -1
            va = self.price * self.holding_num
            return op, va
        # 保持
        #if abs(self.price_change) < 0.02 and abs(stock_cost - self.price)/stock_cost < 0.05:
        #    op = 0
        #    return op, va
        return op, va

    def changeValueToPercent(self, op, va):
        if op == 1:
            va = int(self.horizontalSlider_buy.maximum() * va / self.money_distr) + 1
            if va > self.horizontalSlider_buy.maximum():
                va = self.horizontalSlider_buy.maximum()
        elif op == -1:
            va = int(self.horizontalSlider_sell.maximum() * va / self.money_market) + 1
            if va > self.horizontalSlider_sell.maximum():
                va = self.horizontalSlider_sell.maximum()
        if va < 0:
            va = 0
        return op, va


    def EventPushbuttonPredictClicked(self):
        if self.predict_state == 0: # 预测
            op, va = self.doPredict2()
            op, va = self.changeValueToPercent(op, va)
            if 0 == op:
                self.pushButton_keep.setStyleSheet("background-color: green")
            elif -1 == op:
                self.pushButton_sell.setStyleSheet("background-color: green")
                self.horizontalSlider_sell.setValue(va)
                self.EventSliderSellModed()
            elif 1 == op:
                self.pushButton_buy.setStyleSheet("background-color: green")
                self.horizontalSlider_buy.setValue(va)
                self.EventSliderBuyModed()
            self.predict_op = op
            self.pushButton_predict.setText("执行")
            self.pushButton_predict.setStyleSheet("background-color: green")
            self.predict_state = 1
        elif self.predict_state == 1: # 执行
            if self.predict_op == 0:
                self.EventPushbuttonKeepClicked()
            elif self.predict_op == -1:
                self.EventPushbuttonSellClicked()
            elif self.predict_op == 1:
                self.EventPushbuttonBuyClicked()
            self.predict_state = 0
            self.resetButtonStyleSeet()

    def autoPredict(self):
        while True:
            if self.kline_index >= len(self.kline_data_ori):
                break
            if self.auto_predict_state == 0:
                break
            self.pushButton_predict.click()
            time.sleep(0.08)

    def EventPushbuttonAutoPredictClicked(self):
        if self.auto_predict_state == 0:
            self.auto_predict_state = 1
            t = threading.Thread(target=self.autoPredict)
            t.start()
            self.pushButton_auto_predict.setStyleSheet("background-color: green")
        else:
            self.auto_predict_state = 0
            self.pushButton_auto_predict.setStyleSheet("")


    def mousePressEvent(self, event):
        pos = event.pos()
        #print(pos.x(), pos.y())

    def statisDistribute(self,data):
        x_data = []
        y_data = []
        for i in range(200):
            x_data.append(str(i))
            y_data.append(0)
        num = 0
        for d in data:
            num += 1
            if num > 100000:
                break
            d += 5
            d = d * 20
            #d = d * 10
            if d > 200:
                d = 199
            if d < 0:
                d = 0
            d = int(d)
            y_data[d] += 1
        self.klinehtml.draw_bar(x_data, y_data)

    def analysisKline(self, kline):
        #print(self.datafram)
        data = self.datafram['change'].values
        data = np.random.randn(100000)
        self.statisDistribute(data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = StockSimulation()
    win.show()
    sys.exit(app.exec_())
    #win.analysisKline(win.kline_data_ori)
    #win.klinehtml.draw_bar([])
