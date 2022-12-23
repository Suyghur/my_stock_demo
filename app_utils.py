# _*_coding:utf-8_*_
# Created by #Suyghur, on 2022-12-23.
# Description :
import pandas as pd

from stock import Stock


def get_trading_date(csv_path: str) -> list:
    df = pd.DataFrame(pd.read_csv(csv_path))
    return list(df['Date'])


def get_max_value_stock(stock_map: dict, stock_list: list) -> str:
    tmp_value = 0.00
    tmp_name = ''
    for stock_name in stock_list:
        stock = stock_map[stock_name]
        if stock.market_value > tmp_value:
            tmp_value = stock.market_value
            tmp_name = stock_name
    return tmp_name


def get_golden_cross_date_map(stock_map: dict, trading_date: list):
    date_map = {}
    for date in trading_date:
        stock_list = []
        for stock in stock_map.values():
            if stock.is_golden_cross_date(date):
                stock_list.append(stock.name)
        if len(stock_list) != 0:
            date_map[date] = stock_list
    return date_map


def get_dead_cross_date_map(stock_map: dict, trading_date: list) -> dict:
    date_map = {}
    for date in trading_date:
        stock_list = []
        for stock in stock_map.values():
            if stock.is_dead_cross_date(date):
                stock_list.append(stock.name)
        if len(stock_list) != 0:
            date_map[date] = stock_list
    return date_map
