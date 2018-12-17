"""The spread object"""

import pandas as pd 
import numpy as np 
import time
from DynBB3Tools import *

class spread():
	def __init__(self, filename, length='6M', start_date=None, end_date=None):
		# read in attributes from args 
		self.name = filename[2:-5]
		self.start_date = start_date
		self.end_date = end_date
		self.length = length

		# Parse Data:
		self.data = data_parser(filename)

		# Hedge Ratio:
		self.hedge_ratio = None
	
	def print_name(self):
		print self.name
	def get_name(self):
		return self.name
	def print_data(self):
		print self.data
	def get_data(self):
		return self.data

	def get_start_date(self):
		if self.start_date is not None:
			return self.start_date
		else:
			return self.data.index[0]

	def get_end_date(self):
		if self.end_date is not None:
			return self.end_date
		else:
			return self.data.index[-1]

	# Get Hedge Ratio:
	def get_hedge_ratio(self, ratio_dict):
		if self.hedge_ratio is not None:
			return self.hedge_ratio
		else:
			self.hedge_ratio = generate_ratio_list(self.name, ratio_dict)

	def get_Sharpe_Ratio(self, entry, exit, slippage):
		if self.sharpeRatio is not None:
			return self.sharpeRatio
		else:
			# Load Data
			data = self.data
			# Run backtest:
			[self.sharpeRatio, self.total_profit, self.num_trades] = backtest(data, entry, exit, slippage)
			return self.sharpeRatio


def test_run():
	test_spread = spread('S:GBL-ZN+XE6.data')
	print "\nTotal runtime is: {} seconds.\n".format(run_time)

if __name__ == '__main__':
	test_run()
