#!/usr/bin/python2

"""The backtest object"""

class bt():
	def __init__(self, pnl_data):
		self.data = pnl_data

		self.total_pnl = self.data.tail(1).values[0]