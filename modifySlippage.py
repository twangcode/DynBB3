import sys, getopt
import pandas as pd

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

def main(argv):
	filename = ''
	new_slippage = ''
	
	try:
		opts, args = getopt.getopt(argv, 'hf:s:')
	except getopt.Getopterror:
		print "modifySlippage.py -f filename -s new_slippage"
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print "modifySlippage.py -f filename -s new_slippage"
		elif opt == '-f':
			filename = arg
		elif opt == '-s':
			new_slippage = float(arg)

	modifySlippage(filename, new_slippage)
	

if __name__ == "__main__":
	main(sys.argv[1:])
