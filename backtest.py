#!/usr/bin/python2

import sys, getopt
from lib.spread import *
from lib.DynBB3Tools import *

def main(argv):
	
### read filename, slippage, sharpe_threshold from argument:	
	filename = ''
	slippage = 10
	sharpe_threshold = 0
	length = '180D'
	try:
		opts, args = getopt.getopt(argv, 'hf:s:r:l:')
	except getopt.GetoptError:
		print 'backtest.py -f filename -s slippage -r sharpe_threshold -l length'
		sys.exit(2)
	
	for opt, arg in opts:
		if opt == '-h':
			print 'backtest.py -f filename -s slippage -r sharpe_threshold -l length'
			sys.exit(1)
		elif opt == '-f':
			filename = arg
		elif opt == '-s':
			slippage = float(arg)
		elif opt == '-r':
			sharpe_threshold = arg
		elif opt == '-l':
			length = arg
		else:
			usage()
			sys.exit(2)

### generate spread object:
	test_spread = spread(filename, length=length)
	
### Backtest starts:
	entries = [1, 1.5, 2, 2.5, 3, 3.5, 4]
	exits = [0.5, 0.75, 1.0]
	print 'File name is: ', filename
	print 'slippage is: ', slippage
	print 'sharpe_threshold is: ', sharpe_threshold
	print 'length is: ', length
	print 'Hedge Ratios are: ', test_spread.get_hedge_ratio()
	print 'Start date: ', test_spread.get_start_date()
	print 'End date: ', test_spread.get_end_date()

	for entry in entries:
		for exit in exits:
			try:
				(sr, profit, num_trades) = test_spread.backtest(entry, exit, slippage)
				if sr > float(sharpe_threshold):
					print (entry, entry*exit), '\t', ("%6.2f" % sr,\
											profit, num_trades,\
											"%6.2f" % (profit/num_trades*2))
			except IOError as e:
				print "file IO error{0}: {1}".format(e.errno, e.strerror)
				print 'backtest.py -f filename -s slippage -r sharpe_threshold -l length'
				sys.exit(2)
	
	try:
		modifySlippage(filename, slippage)
		print "modified {} slippage to {}".format(filename, slippage)
	except:
		print "something went wrong trying to modify {} slippage".format(filename)
		sys.exit(2)
	
				
if __name__ == "__main__":
	main(sys.argv[1:])
