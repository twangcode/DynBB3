"""The spread object"""

import pandas as pd 
import numpy as np 
from os.path import join
import time
from DynBB3Tools import *

class spread():
	def __init__(self, filename, length='6M', start_date=None, end_date=None):
		self.name = filename[2:-5]

		# Parse Data:
		old_data = data_reader(join(OLDPATH, filename))
		new_data = data_reader(join(FILEPATH, filename))
		self.data = pd.concat([old_data, new_data]).drop_duplicates().last(length)

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

	# Get Hedge Ratio:
	def get_hedge_ratio(self, ratio_dict):
		if self.hedge_ratio is not None:
			return self.hedge_ratio
		else:
			self.hedge_ratio = generate_ratio_list(self.name, ratio_dict)

	def get_Sharpe_Ratio(self, entry, exit, slippage):
		if self.sharpeRatio is not None:
			retuen self.sharpeRatio
		else:
			# Load Data
			data = self.data
			# Run backtest:
			[self.sharpeRatio, self.total_profit, self.num_trades] = backtest(data, entry, exit, slippage)
			return self.sharpeRatio


		

def test_run():
	start_time = time.time()
	filename = 'S:BB3_TEN:GBL-ZN+XE6.data'
	print spread(filename).EE_Sharpe_Ratio(2, .5, 15)
	run_time = time.time() - start_time
	print "\nTotal runtime is: {} seconds.\n".format(run_time)

if __name__ == '__main__':
	test_run()
