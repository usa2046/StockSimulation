import tushare as ts
import time
import pandas as pd
import numpy as np

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

if __name__ == "__main__":
    tu = TuShareData()
    #df = tu.getDaily(ts_code='000027.SZ', trade_date='20210527')
    df = tu.getDaily(ts_code='000027.SZ', start_date='20210527', end_date='20210606')
    print(df)
    print(df.columns)
    print(df.describe())
