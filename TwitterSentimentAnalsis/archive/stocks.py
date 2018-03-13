#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: Taranpreet singh
Module: Importing Financial data in python using 'pandas_datareader' library
"""
import matplotlib.pyplot as plt
from pandas_datareader.data import DataReader
# date time to use date objects
from datetime import date


class stockdata():
    def getStockQuotes(self,stocksymbol,source,start,end):
        print stocksymbol
        print source
        print start
        print end

        start = date(2016, 10, 11)
        end = date(2017, 10, 21)
        output_file="stock_raw_data/"+stocksymbol+".csv"

        # DataReader is a function to import, there are different sources available to import data
        # such as google fin, yahoo fin,fred, Oanda(for exchange rates)

        # for eg Importing FB data from google
        stock = DataReader(stocksymbol, source, start, end)
        stock.to_csv(output_file)