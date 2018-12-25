#!/usr/bin/python2

import pandas as pd 
import numpy as np 
from os.path import join

FILEPATH_CURRENT = '/var/opt/lufgroup/apps/nova_lufcomp/novaStats_ma/data'
FILEPATH_ARCHIVED = '/var/opt/lufgroup/apps/nova_lufcomp/novaStats_ma/data_full_20181117'

# Generate ADR factor dictionary {Product Symbol: ADR factor}
def generate_factor_dict(dict_location='output/symbol_list.data'):
	df = pd.read_csv(dict_location, header=None, sep=' ', names=['product', 'factor'], index_col=['product'])
	prod_dict = df.to_dict()
	return prod_dict['factor']

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

def data_parser(filename, length='6M'):
	old_data = data_reader(join(FILEPATH_ARCHIVED, filename))
	new_data = data_reader(join(FILEPATH_CURRENT, filename))
	data = pd.concat([old_data, new_data]).drop_duplicates().last(length)
	return data

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

# Modify slippage stored in input files
def modifySlippage(filename, new_slippage):
	# decide which file to read:
	BB3_type = filename.split(':')[1]
	bb3_list_filename = 'input/list_{}.csv'.format(BB3_type) 
	# read bb3 list input file into a dataframe
	df = pd.read_csv(bb3_list_filename,header=None,names=['name','slippage'], index_col=['name'])
	# do the modification
	df.ix[filename] = new_slippage
	# write it back to the original bb3_list_file
	df.to_csv(bb3_list_filename, header=False)

def EE_backtest(data, entry, exit, slippage):
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