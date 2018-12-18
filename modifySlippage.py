import pandas as pd

def modifySlippage(filename, new_slippage):
	# decide which file to read:
	BB3_type = filename.split(':')[1]
	# read in all slippage as dict:
	df = pd.read_csv("input/list_{}.csv".format(BB3_type),header=['name', 'slippage'])
	return df

def test_run():
	filename = 'S:BB3_TEN:GBL-ZN+XE6.data'
	new_slippage = 15
	print modifySlippage(filename, new_slippage)

if __name__ == "__main__":
	test_run()
