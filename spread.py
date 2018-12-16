"""The spread object"""

import pandas as pd 
import numpy as np 
from os.path import join
import time

FILEPATH_CURRENT = '/var/opt/lufgroup/apps/nova_lufcomp/novaStats_ma/data'
FILEPATH_ARCHIVED = '/var/opt/lufgroup/apps/nova_lufcomp/novaStats_ma/data_full_20181117'

# Parse 'S:BB3xxx.data' file, return an pandas.dataframe.
def data_reader(filename):
	df = pd.read_csv(filename, sep=' ', header=None, parse_dates=[[0,1]], \
		usecols=[0, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29], index_col='0_1')
	df.columns = ['N_points', 'Price', \
					'6H_EMA', '6H_SMA', '6H_STDDEV', \
					'12H_EMA', '12H_SMA', '12H_STDDEV', \
					'2D_EMA', '2D_SMA', '2D_STDDEV', \
					'5D_EMA', '5D_SMA', '5D_STDDEV']
	df.index.names = ['Date']
	return df

# Look up a product in the ADR factor dictionary
def look_up(prod, ratio_dict):
	if prod in ratio_dict:
		return float(ratio_dict[prod])
	else:
		return 'nan'

# extract each product and its coefficient in the spread
# Returns a ratio list
def generate_ratio_list(spread_name, ratio_dict):
	ratio_list = []
	default_coefficient = 1.0
	
	# First, break down the spread name into pieces:
	block_list = spread_name.replace('+', ' ').replace('-', ' ').split(' ')
	# Second, for each piece, extract product name, coefficient and calculate coeff*ratio
	for block in block_list:
		coefficient = ''
		while not block[0].isalpha():
	 		coefficient = coefficient + block[0]
	 		block = block[1:]
	 	# Get the product name: 
	 	# after get rid of the coefficient, what's left is the product name
	 	prod_name = block
	 	# Get the coefficient:
	 	if not coefficient:
	 		coefficient = default_coefficient
	 	else:
	 		coefficient = float(coefficient)
	 	# Get the ratio:
	 	ratio = look_up(block, ratio_dict)
	 	if ratio is 'nan': 
	 		return "You don't have {} in the database".format(prod_name)
	 	# Calculate coefficient * ratio
	 	ratio_list.append(coefficient * ratio)

	# Normalize ratio_list and return it 	
	return [round(x / min(ratio_list), 3) for x in ratio_list]

def backtest(data, entry, exit, slippage):
	# Generate bollinger bands accoring to EMA and STDDEV:
	data['UpperBand'] = data['2D_EMA'] + data['2D_STDDEV'] * entry
	data['LowerBand'] = data['2D_EMA'] - data['2D_STDDEV'] * entry
	data['LongExit'] = data['LowerBand'] + data['2D_STDDEV'] * entry * exit
	data['ShortExit'] = data['UpperBand'] - data['2D_STDDEV'] * entry * exit
	# generate trades according to bands
	data['Position'] = None
	data['Position'] = np.where(data['Price'] > (data['UpperBand'] + slippage), -1, None)
	data['Position'] = np.where(data['Price'] < (data['LowerBand'] - slippage), 1, data['Position'])
	data['Position'] = np.where((data['Price'] > (data['LongExit'] + slippage)) & (data['Price'] < (data['ShortExit'] - slippage)), 0, data['Position'])
	data['Position'] = data['Position'].fillna(method='ffill')
	data['Position'] = data['Position'].fillna(0)
	data['Trade'] = data['Position'] - data['Position'].shift(1)
	data['Trade'] = np.where(data['Trade'].isnull(), data['Position'], data['Trade'])
	num_trades = data['Trade'].abs().sum()
	# calculate cumulated pnl:
	data['Cost'] = data['Trade'] * data['Price']
	data['MarketValue'] = data['Price'] * data['Position']
	data['cumPnL'] = data['MarketValue'] - data['Cost'].cumsum()
	total_profit = data['cumPnL'].tail(1).values[0]
	# calculate pnl and sharpe ratio
	data['PnL'] = data['cumPnL'] - data['cumPnL'].shift(1)
	sharpeRatio = data['PnL'].mean() / data['PnL'].std() * np.sqrt(len(data))
	return sharpeRatio, total_profit, num_trades


class spread():
	def __init__(self, filename):
		self.name = filename[2:-5]

		# Parse Data:
		old_data = data_reader(join(OLDPATH, filename))
		new_data = data_reader(join(FILEPATH, filename))
		self.data = pd.concat([old_data, new_data]).drop_duplicates().last('6M')

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
