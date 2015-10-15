# machine-learning-market-maker
Implementation of a Bayesian-style market maker in the vein of 'Intelligent Market-Making in Artificial Financial Markets' by Sanmay Das

Member Variables:  
	Symbol: Ticker for security  
	Distribution: A map of prices with a probability for each price  
	Pa: Ask price, double  
	Pb: Bid price, double  
	Alpha: Percentage of noisy informed traders, double  
	Noise: Noise magnitude of noisy informed traders, double  
	Shift: Difference from 0-profit market maker, double  
	TruePrice: 'True price' traded upon by our model  
