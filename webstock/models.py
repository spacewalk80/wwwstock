from django.db import models
# Create your models here.

#基础交易日历
class StockBasic(models.Model):
    ts_code = models.CharField(max_length=10, primary_key=True)
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=20)
    area = models.CharField(max_length=20)
    industry = models.CharField(max_length=20)
    list_date = models.CharField(max_length=10)

    def __str__(self):
        return self.name

#交易日历数据库
class TradeCalendar(models.Model):
    date = models.CharField(max_length=10, unique=True)  # 交易日期， unique=True，会自动查重。
    is_open = models.BooleanField()  # 是否交易
    exchange = models.CharField(max_length=10)  # 交易所

    def __str__(self):
        return f"{self.date} ({self.exchange}): {'Open' if self.is_open else 'Closed'}"

#股票利润表
class StockIncome(models.Model):
    #适当考虑只获取需要的数据，根据公式书写。 如果需要增加的话，可以重构即可。否则数据量太大。
    #净资产收益率ROE = 净利润/平均股东权益×100 %
    #毛利率=（销售收入−销售成本)/销售收入×100%
    #净利率 = 净利润/销售收入×100 %
    #营业总收入
    #股东权益在资产负债表里
    #其他的都在利润表中。

    ts_code = models.CharField(max_length=10)  # 股票代码
    ann_date = models.DateField()  # 公告日期
    f_ann_date = models.DateField()  # 实际公告日期
    end_date = models.DateField()  # 报告期
    report_type = models.CharField(max_length=10)  # 报告类型
    comp_type = models.CharField(max_length=10)  # 公司类型
    basic_eps = models.FloatField()  # 基本每股收益
    diluted_eps = models.FloatField()  # 稀释每股收益
    total_revenue = models.FloatField()  # 营业总收入
    revenue = models.FloatField()  # 营业收入
    total_cogs = models.FloatField()  # 营业总成本
    operate_profit = models.FloatField()    #营业利润
    total_profit = models.FloatField()    #利润总额
    n_income = models.FloatField()  #净利润(含少数股东损益)
    n_income_attr_p = models.FloatField()  #净利润(不含少数股东损益)
    t_compr_income = models.FloatField()   #综合收益总额
    update_flag =  models.CharField(max_length=10)  #更新标识

    def __str__(self):
        return f"{self.ts_code} - {self.end_date}"

#资产负债表
class StockBalancesheet(models.Model):
    #常用字段
    # ts_code：股票代码
    # ann_date: 公告日期
    # end_date: 公告结束日期
    # otal_hldr_eqy_exc_min_int: 股东权益合计(不含少数股东权益)
    # total_hldr_eqy_inc_min_int: 股东权益合计（含少数股东权益）
    # total_liab: 负债合计
    # total_assets: 资产总计
    #update_flag: 更新标识

    ts_code = models.CharField(max_length=10)
    ann_date = models.DateField()
    end_date = models.DateField()
    total_hldr_eqy_exc_min_int = models.FloatField()
    total_hldr_eqy_inc_min_int = models.FloatField()
    total_liab = models.FloatField()
    total_assets = models.FloatField()
    update_flag =  models.CharField(max_length=10)  #更新标识

    def __str__(self):
        return f"{self.ts_code} - {self.end_date}"

#基本财务数据
class StockFinancials(models.Model):
    ts_code = models.CharField(max_length=10)
    end_date = models.DateField()
    roe = models.DecimalField(max_digits=6, decimal_places=3)  # ROE
    gross_margin = models.DecimalField(max_digits=6, decimal_places=3)  # Gross Margin
    net_margin = models.DecimalField(max_digits=6, decimal_places=3)  #