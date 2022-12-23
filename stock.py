# _*_coding:utf-8_*_
# Created by #Suyghur, on 2022-12-23.
# Description :
from decimal import Decimal

import pandas
import pandas as pd


class Stock:
    # 股票名称
    name = ''
    # 持有股数
    count = 0
    # 成本价
    cost_price = 0
    # 市值
    market_value = 0
    # 收益
    income = 0
    # 交易日期
    trading_date = []
    # 金叉日期
    golden_cross_date = []
    # 死叉日期
    dead_cross_date = []
    # 数据源
    __df = pandas.DataFrame

    def __init__(self, name: str, test_csv_path: str, train_csv_path: str):
        self.name = name
        test_df = pd.DataFrame(pd.read_csv(test_csv_path))
        train_df = pd.DataFrame(pd.read_csv(train_csv_path))

        self.__df = pd.concat([train_df.tail(20), test_df], axis=0, ignore_index=True)
        self.__df['Ma5'] = self.__df['Close'].rolling(5).mean()
        self.__df['Ma20'] = self.__df['Close'].rolling(20).mean()

        self.__df['GoldenCross'] = (self.__df['Ma5'] > self.__df['Ma20']) & (self.__df['Ma5'].shift(1) < self.__df['Ma20'].shift(1))
        self.__df['DeadCross'] = (self.__df['Ma5'] < self.__df['Ma20']) & (self.__df['Ma5'].shift(1) > self.__df['Ma20'].shift(1))

        self.__df.groupby('Date')['GoldenCross'].sum()
        self.__df.groupby('Date')['DeadCross'].sum()

        self.trading_date = list(test_df['Date'].values)
        self.golden_cross_date = list(self.__df.query('GoldenCross == True')['Date'].values)
        self.dead_cross_date = list(self.__df.query('DeadCross == True')['Date'].values)

    def buy(self, date: str, amount: float) -> float:
        if self.count > 0:
            return amount
        sql = 'Date == "%s"' % date
        self.cost_price = self.__df.query(sql)['Low'].values[0]
        self.count = int(amount / self.cost_price)
        self.market_value = self.count * self.cost_price
        self.income = 0.00
        return amount - self.market_value

    def sell(self, date: str) -> float:
        if self.count <= 0:
            # print('当前日期 %s, %s 的持股数小于等于0，不交易' % (date, self.name))
            return 0.00
        sql = 'Date == "%s"' % date
        price = self.__df.query(sql)['High'].values[0]
        self.income = self.count * (price - self.cost_price)
        self.count = 0
        return self.income

    def is_golden_cross_date(self, target_date: str):
        return target_date in self.golden_cross_date

    def is_dead_cross_date(self, target_date: str):
        return target_date in self.dead_cross_date
