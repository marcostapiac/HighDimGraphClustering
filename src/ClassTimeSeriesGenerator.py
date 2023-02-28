from utils.math_functions import np

class TimeSeriesGenerator:

    def __init__(self, n, q, rng=np.random.default_rng()):
        self.numSeries = n
        self.numFeatures = q
        self.rng = rng



class RWTimeSeries(TimeSeriesGenerator):
    def __init__(self, n, q, mean, std, crossCov):
        try:
            assert(crossCov >= 0.)
        except AssertionError:
            print("Please enter a noise correlation value between 0 and 1")
        super().__init__(n=n, q=q)
        self.noiseMean = mean
        self.noiseStd = std
        self.crossCov = crossCov # Generator assumes constant correlation marginals for all stocks

    def indep_simulation(self, tHorizon, initialValue):
        return np.reshape([initialValue, initialValue + self.noiseMean + self.noiseStd*self.rng.normal(loc=0, scale=1., size=tHorizon)], (tHorizon+1,1))

    def portfolio_simulation(self, tHorizon: int, initialValues):
        # TODO
        L = initialValues.shape[0]
        if self.crossCov > 0:
            cov = self.crossCov*np.ones(shape=(L,L)) + (1.-self.crossCov)*np.eye(L)
            print(cov)
            L = np.linalg.cholesky(cov)
            return np.reshape(initialValues, (L,1)) + L@self.rng.normal(size=(L, tHorizon))
        return np.atleast_2d([self.indep_simulation(tHorizon, initialValues[i]) for i in range(L)])



