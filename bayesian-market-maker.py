import numpy
import matplotlib.pyplot as plt
import pandas.io.data as web
import datetime

from scipy.stats import norm

class NaiveMarketMaker:

	def __init__(self, StockTicker, a, s):
		self.setSymbol = StockTicker
		self.setAlpha = a
		self.setNoise = s

	def getInitialPrice(self):
		# Check google finance and get current price
		#
		return(100) # placeholder value

	def getVolatility(self):
		# Check google finance and calculate volatility
		#
		return(.05) # placeholder value

	def initialize(self):
		# Fills out the base distribution using the normal CDF
		# For our purposes the tick size is $.01
		#
		# Inputs vol and V0 should be historical volatility and the current price
		
		self.Distribution = {} # Distribution is dictionary with {Price : Probability(Price)}
		self.TruePrice = []

		self.V0 = self.getInitialPrice # Checks google finance and gets price
		self.vol = self.getVolatility # Calculates volatility from google finance

		Vmin = self.V0 - 4 * self.vol * self.V0
		Vmax = self.V0 + 4 * self.vol * self.V0 - .01

		V = 0
		i = 0
		while((Vmin + i) <= Vmax):
			V = Vmin + i
			self.Distribution[round(V, 2)] = norm.cdf(-4 * self.vol * self.V0 + i + .01, 0, self.vol * self.V0) - norm.cdf(-4 * self.vol * self.V0 + i, 0, self.vol * self.V0)

			i += .01

		self.Pb = self.V0 - self.vol * self.V0 * 0.5
		self.Pa = self.V0 + self.vol * self.V0 * 0.5

		self.TruePrice.append(self.V0)

		return(self.Pa, self.Pb)

	def updateDensity(self, OrderSide):
		# Updates the probability densities
		#
		# Getting BUY indicates that our ASK PRICE is hit (someone buys from us)
		# Getting SELL indicates that our BID PRICE is hit (someone sells to us)

		if OrderSide == "SELL":
			for price in self.Distribution:
				if price <= self.Pb:
					post = (1 - self.Alpha) * 0.5 + self.Alpha * norm.cdf(self.Pb - price, 0, self.Noise * self.V0)
					self.Distribution[price] = post * self.Distribution[price] / 0.5
				else:
					post = (1 - self.Alpha) * 0.5 + self.Alpha * (1 - norm.cdf(price - self.Pb, 0, self.Noise * self.V0))
					self.Distribution[price] = post * self.Distribution[price] / 0.5
		else:
			for price in self.Distribution:
				if price <= self.Pa:
					post = (1 - self.Alpha) * 0.5 + self.Alpha * (1 - norm.cdf(self.Pa - price, 0, self.Noise * self.V0))
					self.Distribution[price] = post * self.Distribution[price] / 0.5
		
		return

	def updateSpread(self):
		# Updates the bid-ask spread
		#
		# Add functionality to check the specific price we are hit at and to update that

		cumSum1 = 0
		cumSum2 = 0

		for price in self.Distribution:
			if price <= self.Pb:
				a = self.Pb - price
				cumSum1 += (0.5 - 0.5 * self.Alpha + self.Alpha * norm.cdf(a, 0, self.Noise * self.V0)) * self.Distribution[price] * price
			else:
				a = price - self.Pb
				cumSum2 += (0.5 - 0.5 * self.Alpha + self.Alpha * (1 - norm.cdf(a, 0, self.Noise * self.V0))) * self.Distribution[price] * price
			
		newPb = 2 * (cumSum1 + cumSum2)

		cumSum1 = 0
		cumSum2 = 0

		for price in self.Distribution:
			if price <= self.Pa:
				a = self.Pa - price
				cumSum1 += (0.5 - 0.5 * self.Alpha + self.Alpha * (1 - norm.cdf(a, 0, self.Noise * self.V0))) * self.Distribution[price] * price
			else:
				a = price - self.Pa
				cumSum2 += (0.5 - 0.5 * self.Alpha + self.Alpha * norm.cdf(a, 0, self.Noise * self.V0)) * self.Distribution[price] * price

		newPa = 2 * (cumSum1 + cumSum2)
		
		self.Pb = newPb
		self.Pa = newPa

		(self.TruePrice).append((self.Pa + self.Pb)/2) # Add the true price to our list
		return(self.Pa, self.Pb) # Returns Pa and Pb so that we can input the new orders

	def writeData(self):
		# Write vector to an array so we can graph it
		data = np.array(self.TruePrice)
		#plt.plot(data)
		#plt.show()
		return
	
	def run(self):
		# A loop that executes the strategy
		#
		# CONTAINED WITHIN API
		return

	def placeOrder(self):
		# Places an order on a security
		#
		# CONTAINED WITHIN API
		return

	def close(self):
		# Closes out of all positions
		#
		# CONTAINED WITHIN API
		return


