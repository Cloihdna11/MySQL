import pandas as pd
import Backtest as bt
from pandas._testing import assert_frame_equal
import unittest
from unittest import mock




class Test_Backtest(unittest.TestCase):
  
    def test_importStratDF(self):
        result = bt.importStratDF()
        self.assertIsNotNone(result)


    def test_importHistoricalDF(self):
        result = bt.importHistoricalDF()       
        self.assertIsNotNone(result)

    def test_populate_trade_table_row(self):
        StratDF = bt.importStratDF()
        HistoricalDF = bt.importHistoricalDF()
        result = bt.populate_trade_table_row('7/8/2020',StratDF.iloc[1],HistoricalDF)
        self.assertIsNotNone(result)

    def test_GetMaturityDate(self):
        result = bt.GetMaturityDate('7/8/2020', 90)
        self.assertIsNotNone(result)

    def test_GetVolSurface(self):
        result = bt.GetVolSurface()
        self.assertIsNotNone(result)

           
if __name__ == '__main__':
    unittest.main()
