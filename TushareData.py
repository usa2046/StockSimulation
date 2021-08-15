import tushare as ts
import time
import pandas as pd
import numpy as np
import datetime

# 核心代码，设置显示的最大列、宽等参数，消掉打印不完全中间的省略号
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

#ts.set_token('5622b32a445df8a1372aedd831c2b2d109fbd418a7201ab1b4b0fcce')

#df = pro.query('trade_cal',
#               exchange='',
#               start_date='20180901',
#               end_date='20181001',
#               fields='exchange, cal_date, is_open, pretrade_date',
#               is_open='')
#print(df)

class TuShareData():
    pro = ts.pro_api('5622b32a445df8a1372aedd831c2b2d109fbd418a7201ab1b4b0fcce')

    def __init__(self):
        return

    def getDaily(self, ts_code, trade_date='', start_date='', end_date=''):
        for _ in range(3):
            try:
                if trade_date:
                    df = self.pro.daily(ts_code=ts_code, trade_date=trade_date)
                else:
                    df = self.pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
            except:
                time.sleep(1)
            else:
                return df

    def getAllStockByDate(self, start_date='', end_date=None):
        date_list = self.create_assist_date(start_date=start_date, end_date=end_date)
        stocks = []
        for date in date_list:
            try:
                df = self.pro.daily(trade_date=date)
                if len(df) == 0:
                    continue
                stocks.append(df)
                print("> load:", date)
            except:
                continue
        table, basic = self.sort_table(stocks)
        return table, basic

    def sort_table(self, stocks):
        '''
        整理表格
        '''
        table = {}
        basic = {}
        basic_all = self.getAllStockBasic()
        for stock in stocks:
            stock_num = len(stock)
            if not table: # 第一次 table 为空，初始化键值
                for i in range(stock_num):
                    line = stock.loc[i, :].values
                    # 0 ts_code
                    # 1 trade_date
                    # 2 open
                    # 3 high
                    # 4 low
                    # 5 close
                    # 6 pre_close
                    # 7 change
                    # 8 pct_chg
                    # 9 vol
                    # 10 amount
                    table[line[0]] = []
                    if line[0] in basic_all.keys():
                        basic[line[0]] = basic_all[line[0]]
                    else:
                        basic[line[0]] = []
            temp_tabel = {}
            for i in range(stock_num):
                line = stock.loc[i, :].values
                code = line[0]
                temp_tabel[code] = line
            for key in table.keys():
                if key in temp_tabel.keys():
                    table[key].append(temp_tabel[key]) # 追加新数据
                else:
                    data = table[key][-1]
                    data[2] = data[5]
                    data[3] = data[5]
                    data[4] = data[5]
                    data[6] = data[5]
                    data[7] = '0.00'
                    data[8] = '0.00'
                    table[key].append(data)  # 重复上一日期的数据
        return table, basic



    def create_assist_date(self, start_date, end_date=None):
        '''
        获取日期序列，end_date 如果为 None，则截至到当前时间
        '''
        if end_date == None:
            end_date = datetime.datetime.now().strftime('%Y%m%d')
        start_date = datetime.datetime.strptime(start_date, '%Y%m%d')
        end_date = datetime.datetime.strptime(end_date, '%Y%m%d')
        date_list = []
        date_list.append(start_date.strftime('%Y%m%d'))
        while start_date < end_date:
            start_date += datetime.timedelta(days=+1)
            date_list.append(start_date.strftime('%Y%m%d'))
        return date_list

    def save_table_to_file(self, table):
        '''
        把 table 的数据保存在文件中
        '''
        #list = np.array([])
        #for key in sorted(table.keys()):
        #    list = np.vstack((list, table[key]))
        #np.savetxt("./table.txt", list, fmt='%s')
        pass

    def getAllStockBasic(self):
        basic_data = self.pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
        basic = {}
        basic_data_num = len(basic_data)
        for i in range(basic_data_num):
            line = basic_data.loc[i, :].values
            code = line[0]
            basic[code] = line
        return basic


if __name__ == "__main__":
    tu = TuShareData()
    #df = tu.getDaily(ts_code='000027.SZ', trade_date='20210527')
    #df = tu.getDaily(ts_code='000027.SZ', start_date='20210527', end_date='20210606')
    #print(df)
    #print(df.columns)
    #print(df.describe())
    #table = tu.get_all_stock_by_date(start_date='20210722')
    #tu.save_table_to_file(table)
    #print(table.keys())
    tu.getAllStockName()
