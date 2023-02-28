from src.ClassTimeSeriesGenerator import RWTimeSeries
from utils.math_functions import np

numStocks = 10
numFeatures = 1
gaussNoiseMean = 0.
gaussNoiseStd = 1.2
crossCov = 0.
rwGen = RWTimeSeries(n=numStocks, q=numFeatures, mean=gaussNoiseMean, std=gaussNoiseStd, crossCov=crossCov)

tHorizon = 10
initialValues = np.random.exponential(scale=1./3., size=numStocks)
portfolio = rwGen.portfolio_simulation(tHorizon=tHorizon, initialValues=initialValues)