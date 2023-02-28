import numpy as np
import pandas as pd
from scipy.stats import pearsonr, kendalltau
from scipy.special import digamma
from scipy.stats import gamma as gammafnc


def sample_distance_elements(vector):
    assert isinstance(vector[0], np.float64)  # p = 1 for our US_CRSP_NYSE
    T = vector.shape[0]
    tileVec = np.tile(vector, (T, 1))
    absDiffMat = np.abs(tileVec - tileVec.T)
    absDiffMat[1, 2] = 8.
    aDotDot = np.sum(absDiffMat) * np.power(T, -2.)
    sumXjs = np.tile(np.sum(absDiffMat, axis=1), (T, 1)).T * np.power(T, -1.)
    sumXks = np.tile(np.sum(absDiffMat, axis=0), (T, 1)) * np.power(T, -1.)
    Aks = absDiffMat - sumXks - sumXjs + aDotDot
    return Aks


def sample_distance_correlation(Aks, Bks):
    assert (Aks.shape[0] == Bks.shape[0] == Aks.shape[1] == Bks.shape[1])
    T = Aks.shape[0]
    ones = np.ones(shape=(T, 1))
    return np.power(T, -2.) * ones.T @ np.multiply(Aks, Bks) @ ones
