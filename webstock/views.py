from django.shortcuts import render
from django.http import HttpResponse
from datetime import  datetime
from django.http import JsonResponse
from .models import StockBasic
from .models import TradeCalendar
from .models import StockIncome
from .models import StockBalancesheet
from .stock_basecal import calculate_financials
from django.conf import settings   #引用settings.py中的常量
import tushare as ts
import pandas as pd
import time
#定义首页
def index(request):
    #取得当前时间
    nowtime = datetime.now

    #封装变量
    context = {
        'nowtime':nowtime,
    }
    return render(request, 'index.html',context )

def stock_base_list(request):
    return render(request, 'stock_base_list.html')


def format_date(date_str):
    return datetime.strptime(date_str, '%Y%m%d').strftime('%Y-%m-%d')

def update_stock_trade_calendar():
    pro = ts.pro_api(settings.TUSHARE_TOKEN)
    today = datetime.today().strftime('%Y%m%d')
    print(today)
    df = pro.trade_cal(start_date='20200101', end_date=today)  # 获取从2020年1月1日到现在的交易日历数据

    for index, row in df.iterrows():
        TradeCalendar.objects.update_or_create(
            date=row['cal_date'],
            defaults={
                'is_open': bool(row['is_open']),
                'exchange': row['exchange']
            }
        )

#获得股票基本数据。
def update_stock_basic_data():
# 设置 Tushare token
    ts.set_token(settings.TUSHARE_TOKEN)
    print("enter update_stock_basic_data")
    # 初始化 pro 接口
    pro = ts.pro_api()

    # 获取股票基本信息数据
    stock_basic_data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')

    # 遍历并存储数据
    for index, row in stock_basic_data.iterrows():
        StockBasic.objects.update_or_create(
            ts_code=row['ts_code'],
            defaults={
                'symbol': row['symbol'],
                'name': row['name'],
                'area': row['area'],
                'industry': row['industry'],
                'list_date': row['list_date']
            }
        )
    # return JsonResponse({'status': 'success', 'message': 'Stock basic data updated successfully'})


#获取利润表
def update_stock_income():
    print("update_stock_income_first")
    pro = ts.pro_api(settings.TUSHARE_TOKEN)
    today = datetime.today().strftime('%Y%m%d')
    print(today)

    # 获取所有股票代码
    stock_list = StockBasic.objects.all().values_list('ts_code', flat=True)

    for ts_code in stock_list:
        print(f"Fetching income data for stock: {ts_code}")
        # ts_code # 股票代码 ann_date # 公告日 f_ann_date # 实际公告日 end_date # 报告期 report_type  # 报告类型 comp_type   # 公司类型 basic_eps  # 基本每股收益
        # diluted_eps # 稀释每股收益 total_revenue # 营业总收入 revenue  # 营业收入 total_cogs  # 营业总成本 operate_profit   #营业利润 total_profit   #利润总额
        # n_income  #净利润(含少数股东损益) n_income_attr_p #净利润(不含少数股东损益)  t_compr_income  #综合收益总额 update_flag #更新标识
        #end data为实际的季报日期。
        #0   600000.SH  20231028   20231028  20230930           1         2       0.88
        single_stock_income = pro.income(ts_code=ts_code, start_date='20200101', end_date='today',
                         fields='ts_code,ann_date,f_ann_date,end_date,report_type,comp_type,basic_eps,diluted_eps,'
                                'total_revenue,revenue,total_cogs,operate_profit,total_profit,n_income,n_income_attr_p,'
                                't_compr_income,update_flag')
        # pd.set_option('display.max_columns',None)
        print(single_stock_income)
        time.sleep(0.5)
        for index, row in single_stock_income.iterrows():
            # 使用0替换NaN数据
            row = row.fillna(0)

            #格式转换
            end_date_formatted = format_date(row['end_date'])
            ann_date_formatted = format_date(row['ann_date'])
            f_ann_date_formatted = format_date(row['f_ann_date'])

            StockIncome.objects.update_or_create(
                ts_code=row['ts_code'],
                # end_date=row['end_date'],
                end_date=end_date_formatted,
                update_flag=row['update_flag'],
                defaults={
                    # 'ann_date': row['ann_date'],
                    'ann_date': ann_date_formatted,
                    # 'f_ann_date': row['f_ann_date'],
                    'f_ann_date': f_ann_date_formatted,
                    'report_type': row['report_type'],
                    'comp_type': row['comp_type'],
                    'basic_eps': row['basic_eps'],
                    'diluted_eps': row['diluted_eps'],
                    'total_revenue': row['total_revenue'],
                    'revenue': row['revenue'],
                    'total_cogs': row['total_cogs'],
                    'operate_profit': row['operate_profit'],
                    'total_profit': row['total_profit'],
                    'n_income': row['n_income'],
                    'n_income_attr_p': row['n_income_attr_p'],
                    't_compr_income': row['t_compr_income']
                    # 其他需要存储的字段...
                }
            )
        #just for test
        # break;

#获取资产负债表
def update_stock_balancesheet():
    print("update_stock_balancesheet")
    pro = ts.pro_api(settings.TUSHARE_TOKEN)
    today = datetime.today().strftime('%Y%m%d')
    print(today)

    # 获取所有股票代码
    stock_list = StockBasic.objects.all().values_list('ts_code', flat=True)

    for ts_code in stock_list:
        print(f"Fetching balancesheet data for stock: {ts_code}")
        # 常用字段
        # ts_code：股票代码
        # ann_date: 公告日期
        # end_date: 公告结束日期
        # total_hldr_eqy_exc_min_int: 股东权益合计(不含少数股东权益)
        # total_hldr_eqy_inc_min_int: 股东权益合计（含少数股东权益）
        # total_liab: 负债合计
        # total_assets: 资产总计
        # update_flag: 更新标识

        single_balancesheet_data = pro.balancesheet(ts_code=ts_code, start_date='20200101', end_date='today',
                         fields='ts_code,ann_date,end_date,total_hldr_eqy_exc_min_int,total_hldr_eqy_inc_min_int,'
                                'total_liab,total_assets,update_flag')
        # pd.set_option('display.max_columns',None)
        print(single_balancesheet_data)
        time.sleep(0.5)
        for index, row in single_balancesheet_data.iterrows():
            # 使用0替换NaN数据
            row = row.fillna(0)

            #格式转换
            end_date_formatted = format_date(row['end_date'])
            ann_date_formatted = format_date(row['ann_date'])

            StockBalancesheet.objects.update_or_create(
                ts_code=row['ts_code'],
                #end_date=row['end_date'],
                end_date=end_date_formatted,
                update_flag=row['update_flag'],
                defaults={
                    # 'ann_date': row['ann_date'],
                    'ann_date': ann_date_formatted,
                    'total_hldr_eqy_exc_min_int': row['total_hldr_eqy_exc_min_int'],
                    'total_hldr_eqy_inc_min_int': row['total_hldr_eqy_inc_min_int'],
                    'total_liab': row['total_liab'],
                    'total_assets': row['total_assets'],
                    'update_flag': row['update_flag']
                    # 其他需要存储的字段...
                }
            )
        #just for test
        # break;


#获得股票基本数据。
def update_stock_basic_datalist(request):
    print("enter update_stock_basic_datalist")
    # #交易日历
    #update_stock_trade_calendar()
    # #基本股票列表
    #update_stock_basic_data()
    #利润表
    update_stock_income()
    #资产负债表
    update_stock_balancesheet()
    #获得财务数据
    # calculate_financials()
    return JsonResponse({'status': 'success', 'message': 'Stock basic data updated successfully'})

def add_schedul_action():
    #add for test
    print("enter add_schedul_action")


