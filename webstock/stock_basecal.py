
# Your script code here
from .models import StockBasic, StockIncome, StockBalancesheet, StockFinancials
from django.db.models import F
import time
import decimal

# 计算基本财务数据，并保存
def calculate_financials():
    print('enter calculate_financials')
    # for stock in StockBasic.objects.all():
    #     incomes = StockIncome.objects.filter(ts_code=stock.ts_code)
    #     balancesheets = StockBalancesheet.objects.filter(ts_code=stock.ts_code)
    #     print(stock.ts_code)
    #     for income, balancesheet in zip(incomes, balancesheets):
    #         print(income.end_date,balancesheet.end_date)
    #         if income.end_date == balancesheet.end_date:
    #             roe = round(income.n_income_attr_p / balancesheet.total_hldr_eqy_exc_min_int, 3)
    #             gross_margin = round((income.revenue - income.total_cogs) / income.revenue, 3)
    #             net_margin = round(income.n_income_attr_p / income.revenue, 3)
    #
    #             print(stock.ts_code,income.end_date)
    #             print(f"ROE for n_income_attr_p {income.n_income_attr_p} total_hldr_eqy_exc_min_int {balancesheet.total_hldr_eqy_exc_min_int}: {roe}")
    #
    #             StockFinancials.objects.update_or_create(
    #                 ts_code=stock.ts_code,
    #                 end_date=income.end_date,
    #                 defaults={
    #                     'roe': roe,
    #                     'gross_margin': gross_margin,
    #                     'net_margin': net_margin
    #                 }
    #             )
    #     #added for test, 只查找一只股票就中断
    #     # break;
    for stock in StockBasic.objects.all():
        # 获取当前股票代码的所有收入记录
        income_records = StockIncome.objects.filter(ts_code=stock.ts_code)

        # 获取与这些收入记录相关的所有资产负债表记录，并存储在字典中
        balance_dict = {balance.end_date: balance for balance in
                        StockBalancesheet.objects.filter(ts_code=stock.ts_code)}
        # print(balance_dict)
        for income in income_records:
            # 直接从字典中获取匹配的资产负债表记录
            balance = balance_dict.get(income.end_date)
            # print(income.end_date)
            # 如果找到匹配的 balance 记录，则计算财务比率
            if balance:
                roe = (income.n_income_attr_p / balance.total_hldr_eqy_exc_min_int) if balance.total_hldr_eqy_exc_min_int else 0
                gross_margin = ((income.revenue - income.total_cogs) / income.revenue) if income.revenue else 0
                net_margin = (income.n_income_attr_p / income.revenue) if income.revenue else 0
                print(stock.ts_code,income.end_date,roe,gross_margin,net_margin)

                roe=round(roe, 3)
                gross_margin = round(gross_margin, 3)
                net_margin = round(net_margin, 3)

                # 检查是否超出范围
                if roe > 1 or roe < -1:
                    roe = 0
                if gross_margin > 1 or gross_margin < -1:
                    gross_margin = 0
                if net_margin > 1 or net_margin < -1:
                    net_margin = 0

                print(roe,gross_margin,net_margin)
                # 更新或创建计算结果
                StockFinancials.objects.update_or_create(
                    ts_code=stock.ts_code,
                    end_date=income.end_date,
                    defaults={
                        'roe': roe,
                        'gross_margin': gross_margin,
                        'net_margin': net_margin
                    }
                )
