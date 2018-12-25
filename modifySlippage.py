#!/usr/bin/python2

import sys, getopt
import pandas as pd
from lib.DynBB3Tools import *

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
