#!/usr/bin/python2

""" Functions for Spread object """

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

def data_parser(filename, length='6M'):
	old_data = data_reader(join(FILEPATH_ARCHIVED, filename))
	new_data = data_reader(join(FILEPATH_CURRENT, filename))
	data = pd.concat([old_data, new_data]).drop_duplicates().last(length)
	return data