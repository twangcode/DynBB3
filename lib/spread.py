"""The spread object"""

from DynBB3Tools import *

RATIO_DICT = None

class spread():
	def __init__(self, filename, length='6M', start_date=None, end_date=None):
		# read in attributes from args 
		self.name = filename.split(':')[2][:-5]
		self.start_date = start_date
		self.end_date = end_date
		self.length = length

		# Parse Data:
		self.data = data_parser(filename, length)

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
	def get_hedge_ratio(self, ratio_dict=RATIO_DICT):
		if ratio_dict is None:
			ratio_dict = generate_factor_dict()
			RATIO_DICT = ratio_dict
		if self.hedge_ratio is None:
			self.hedge_ratio = generate_ratio_list(self.name, ratio_dict)
		return self.hedge_ratio

	def backtest(self, entry, exit, slippage):
		# Run backtest:
		[sharpeRatio,total_profit, num_trades] = EE_backtest(self.data, entry, exit, slippage)
		return [sharpeRatio, total_profit, num_trades]


def test_run():
	test_spread = spread('S:BB3_TEN:GBL-ZN+XE6.data')
	print "spread name is: ", test_spread.get_name()
	print "start date is: ", test_spread.get_start_date()
	print "end date is: ", test_spread.get_end_date()
	print "hedge ratios are: ", test_spread.get_hedge_ratio()
	print "Sharpe ratio is: ", test_spread.backtest(entry=2.0, exit=0.75, slippage=10)
	# print "\nTotal runtime is: {} seconds.\n".format(run_time)

if __name__ == '__main__':
	test_run()
