from utils.math_functions import pd, np, sample_distance_correlation, sample_distance_elements, gammafnc
from numba import njit, prange
from tqdm import tqdm


def csv_to_clean_dataframe(csvPath):
    df = pd.read_csv(csvPath)
    stockNames = df.iloc[:, 0]  # Will form node names
    cleanDf = df.iloc[:, 1:]
    return df, cleanDf, stockNames


def from_data_to_adjacencyMat(cleanDf, method, lag=1):
    if method == 'pearson' or method == 'kendall':
        return cleanDf.corrwith(cleanDf.shift(periods=lag), method=method).to_numpy()
    elif method == 'mutualInformation':
        pass
    elif method == 'distance':
        N = cleanDf.shape[0]  # T = cleanDf.shape[1]
        adjMat = np.zeros(shape=(N, N))
        # TODO: EFFICIENCY
        for i in tqdm(range(N)):
            XAs = sample_distance_elements(cleanDf.iloc[i, :])
            V2X = sample_distance_correlation(XAs, XAs)
            # TODO: Parallelise
            for j in (range(i, N)):
                YBs = sample_distance_elements(cleanDf.iloc[j, :])
                V2Y = sample_distance_correlation(YBs, YBs)
                if V2X * V2Y <= 0:
                    adjMat[i, j] = 0.
                    adjMat[j, i] = 0.
                else:
                    V2XY = sample_distance_correlation(XAs, YBs)
                    metric = np.power(V2XY * np.power(V2X * V2Y, -0.5), 0.5)
                    adjMat[i, j] = metric
                    adjMat[j, i] = metric
        return adjMat


def threshold_adjMat(adjMat, method, alpha=0.01):
    N = adjMat.shape[0]
    if method == "mutualInformation":
        A = 0
        B = 0
        threshold = gammafnc.ppf(1. - alpha / N, shape=0.5 * (A - 1.) * (B - 1.), scale=N * np.log(2.))
        return np.clip(adjMat, a_min=threshold, a_max=None)
    else:
        pass


def store_adjMatrix(adjMat, dataSetName, method, lag, columnNames=None):
    adjDf = pd.DataFrame(adjMat, columns=columnNames)
    adjDf.to_csv("../data/" + "adjMat_" + dataSetName + "_" + method + "_lag_" + lag + ".gzip", compression="gzip", index=False)
