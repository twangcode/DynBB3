import pandas as pd 

bb3_file_by_type = ['list_BB3.csv',\
				 	'list_BB3_FIX.csv', \
				 	'list_BB3_FLY.csv', \
				 	'list_BB3_TEN.csv']

bb3_file_by_acct = ['list_acct_A.csv',\
				 	'list_acct_B.csv', \
				 	'list_acct_C.csv', \
				 	'list_acct_D.csv', \
				 	'list_acct_E.csv', \
				 	'list_acct_F.csv', \
				 	'list_acct_I.csv']



def read_all_csv(csv_file_list):
	df_list = []
	for file in csv_file_list:
		temp_df = pd.read_csv(file, header=None, names=['name', 'ref_slippage'], index_col='name')
		df_list.append(temp_df)
	df = pd.concat(df_list)
	return df

def backtest_acct(filename, df_ref):
	df = pd.read_csv(filename, header=None, names=['name', 'slippage'], index_col='name')
	df = df.join(df_ref, how='left')
	df['slippage'] = df['ref_slippage']
	return df['slippage']

def main():
	df_ref = read_all_csv(bb3_file_by_type)
	for file in bb3_file_by_acct:
		df = backtest_acct(file, df_ref)
		df.to_csv(file)

if __name__ == '__main__':
	main()