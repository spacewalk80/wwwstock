# 导入tushare
import pandas as pd
import tushare as ts
# from sqlalchemy import create_engine
import mysql.connector
import numpy as np

# engine_ts = create_engine('mysql://admin_stock:2002Tcl2005Ck@127.0.0.1:3306/wwwstock?charset=utf8&use_unicode=1')
# engine_ts = create_engine("mysql://admin_stock:2002Tcl2005Ck@localhost:3306/wwwstock")


class StockGetData:
    def __init__(self):
        # # 初始化数据库
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="admin_stock",
            passwd='@002Tcl@005Ck',
            database="wwwstock"
        )
        self.mycursor=self.mydb.cursor()
        # set tushare token
        ts.set_token('ef3323e5b01d9b5b6e3824f5d74bd58a88690d53192818142d70f746')
    def create_tables(self):
        sql = "create table stock_basic (ts_code varchar(10) primary key, symbol varchar(6), name varchar(10), area varchar(5), industry varchar(10), market varchar(10),list_date varchar(10))"
        self.mycursor.execute(sql)
    #读取并显示
    def read_basic_data(self):
       sql = "SELECT * FROM stock_basic LIMIT 20"
       self.mycursor.execute(sql)
       df_out = self.mycursor.fetchall()
       print(df_out)
       return df_out

    def write_basic_data(self, df):
        dataset = np.array(df)
        datalist = dataset.tolist()
        sql = "insert into stock_basic(ts_code,symbol,name,area,industry,market,list_date) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        try:
            # 执行sql语句
            # self.mycursor.executemany(sql, datalist)
            self.mycursor.executemany(sql, datalist)
            # 提交到数据库执行
            self.mydb.commit()

        except Exception as e:
            print(e)
            # 如果发生错误则回滚
            self.mydb.rollback()
        # # 关闭游标
        # cursor.close()
        # # 关闭数据库连接
        # db.close()

    def get_basic_data(self):
        pro = ts.pro_api()
        df = pro.stock_basic()
        print(df)
        return df

if __name__ == '__main__':
    # 设置token
    # ts.set_token('ef3323e5b01d9b5b6e3824f5d74bd58a88690d53192818142d70f746')

    # 以上方法只需要在第一次或者token失效后调用，完成调取tushare数据凭证的设置，正常情况下不需要重复设置。也可以忽略此步骤，直接用pro_api('your token')完成初始化
    # 初始化pro接口
    #pro = ts.pro_api()

    # 如果上一步骤ts.set_token('your token')无效或不想保存token到本地，也可以在初始化接口里直接设置token:
    # pro = ts.pro_api('your token')

    # 数据调取
    #查询当前所有正常上市交易的股票列表
    # data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    # print(data)

    #查询当前所有正常上市交易的股票列表
    # data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    # print(data)

    #查询股票日历
    # df = pro.trade_cal(exchange='', start_date='20230101', end_date='20231231')

    #查询股票曾用名
    # df = pro.namechange(ts_code='600848.SH', fields='ts_code,name,start_date,end_date,change_reason')

    #查询上市公司基本信息
    # df = pro.stock_company(exchange='SZSE', fields='ts_code,chairman,manager,secretary,reg_capital,setup_date,province')

    #IPO新股列表
    # df = pro.new_share(start_date='20230901', end_date='20231018')

    #日线数据，未复权
    # df = pro.query('daily', ts_code='000001.SZ', start_date='20230701', end_date='20231118')
    #周线数据
    # df = pro.weekly(ts_code='000001.SZ', start_date='20230101', end_date='20231101',
    #                 fields='ts_code,trade_date,open,high,low,close,vol,amount')
    #月线数据
    # df = pro.monthly(ts_code='000001.SZ', start_date='20230101', end_date='20231101',
    #                 fields='ts_code,trade_date,open,high,low,close,vol,amount')
    # print(df)
    stock_getdata = StockGetData()
    df = stock_getdata.get_basic_data()
    stock_getdata.create_tables()
    stock_getdata.write_basic_data(df)
    # df_out=stock_getdata.read_basic_data()



