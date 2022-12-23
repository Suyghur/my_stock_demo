# _*_coding:utf-8_*_
# Created by #Suyghur, on 2022-12-23.
# Description :
import os
from decimal import Decimal

import app_utils
from stock import Stock

if __name__ == '__main__':
    train_path = './app_train'
    test_path = path = './app_test'
    # 债券交易日
    bond_purchase_days = ['2018-01-02', '2018-07-02', '2019-01-02', '2019-7-1']
    # 债券到期日
    bond_mature_days = ['2018-06-29', '2018-12-31', '2019-06-28', '2019-12-31']
    # 导入任意一只股票获取交易日list
    trading_date = app_utils.get_trading_date('./app_test/B1K.csv')
    # 总金额
    total_amount = 100000.00
    # 每个股票交易日上限金额
    daily_limit_amount = 5000.00
    # 债券金额
    bond_amount = 0.00
    # 股票金额
    stock_amount = 0.00
    # 当前余额
    current_balance = 100000.00
    # 股票map
    stock_map = {}

    # 导入股票数据
    for csv in os.listdir(test_path):
        stock_name = csv[:-4]

        test_csv = os.path.join(test_path, csv)
        train_csv = os.path.join(train_path, csv)
        stock = Stock(stock_name, test_csv, train_csv)
        stock_map[stock_name] = stock
    # 获取金叉日期
    golden_cross_date_map = app_utils.get_golden_cross_date_map(stock_map, trading_date)
    # 获取死叉日期
    dead_cross_date_map = app_utils.get_dead_cross_date_map(stock_map, trading_date)
    # 开始交易
    for date in trading_date:
        print('Date: %s' % date)
        # 当前日期是金叉日期
        print('>>> buy')
        if date in golden_cross_date_map.keys():
            stock_list = golden_cross_date_map[date]
            amount = float(Decimal(daily_limit_amount / len(stock_list)).quantize(Decimal('0.00')))
            balance = 0.00
            for stock_name in stock_list:
                stock = stock_map[stock_name]
                balance += stock.buy(date, amount)
                print('------')
                print(stock_name)
                print(balance)
            current_balance -= balance
        print('>>> sell')
        if date in dead_cross_date_map.keys():
            income = 0.00
            stock_list = dead_cross_date_map[date]
            for stock_name in stock_list:
                stock = stock_map[stock_name]
                income += stock.sell(date)
                print('------')
                print(stock_name)
                print(income)
            current_balance += income
        print(current_balance)
        print('------------------------------------------------------------------')
    # for date, stock_list in dead_cross_date_map.items():
    #     print(stock_list)
