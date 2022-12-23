# _*_coding:utf-8_*_
# Created by #Suyghur, on 2022-12-23.
# Description :
import os
from decimal import Decimal

import pandas as pd

import app_utils
from stock import Stock

if __name__ == '__main__':
    pd.set_option('display.max_rows', None)
    # pd.set_option('display.max_columns', 10)
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
    stock_value = 0.00
    # 股票收益
    stock_income = 0.00
    # 股票收益率
    stock_rate = 0.00
    own_stock_list = []
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
    data = {
        'Date': trading_date,
        'BondAmount': [],
        'StockIncome': [],
        'StockValue': [],
        'StockRate': [],
        'Balance': []
    }
    # 开始交易
    for date in trading_date:
        stock_rate = stock_income / total_amount
        # 当前日期是债券交易日期
        if date in bond_purchase_days:
            if stock_rate < 0.03:
                if current_balance >= 10000.00:
                    print('当前日期 %s 股票收益小于债券,股票收益率: %f' % (date, stock_rate))
                    bond_amount += 10000.00
                    current_balance -= bond_amount
                else:
                    max_value_stock = app_utils.get_max_value_stock(stock_map, own_stock_list)
                    print(max_value_stock)

        # 当前日期是金叉日期
        if date in golden_cross_date_map.keys() and current_balance >= daily_limit_amount:
            stock_list = golden_cross_date_map[date]
            amount = daily_limit_amount / len(stock_list)
            balance = 0.00
            for stock_name in stock_list:
                stock = stock_map[stock_name]
                balance = balance + stock.buy(date, amount)
                if stock_name not in own_stock_list:
                    own_stock_list.append(stock_name)
                # 计算持股市值
                stock_value = stock_value + stock.market_value
                stock_map[stock_name] = stock
            current_balance = current_balance - daily_limit_amount + balance
        # 当前日期是死叉日期
        if date in dead_cross_date_map.keys():
            stock_list = dead_cross_date_map[date]
            income = 0.00
            for stock_name in stock_list:
                stock = stock_map[stock_name]
                income = income + stock.sell(date)
                # 卖出成功
                if income > 0 and stock_name in own_stock_list:
                    own_stock_list.remove(stock_name)
                    # 计算持股市值
                    stock_value = stock_value - stock.market_value
                    current_balance = current_balance + stock.market_value
                    stock_map[stock_name] = stock
            stock_income = stock_income + income
        data['BondAmount'].append(bond_amount)
        data['StockIncome'].append(stock_income)
        data['StockValue'].append(stock_value)
        data['StockRate'].append(stock_rate)
        data['Balance'].append(current_balance)
    df = pd.DataFrame(data)
    print(df)
