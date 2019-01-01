import pandas as pd 

def backtest_acct(filename, ref_filename):
	df = pd.read_csv(filename, header=None, names=['name', 'slippage'], index_col='name')
	df_ref = pd.read_csv(ref_filename, header=None, names=['name', 'ref_slippage'], index_col='name')
	df = df.join(df_ref, how='left')
	df['slippage'] = df['ref_slippage']
	df['slippage'].to_csv('input/temp.csv')

def test_run():
	print backtest_acct('input/list_acct_C.csv', 'input/list_BB3.csv')

if __name__ == '__main__':
	test_run()