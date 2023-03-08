from utils.math_functions import pd, np
from utils.plotting_functions import visualise_digraph
from utils.data_processing import csv_to_clean_dataframe, from_data_to_adjacencyMat, store_adjMatrix, threshold_adjMat

dataSetName = "OPCL_20000103_20201231"
csvPath = "../data/"+dataSetName+".csv"
rawDf, cleanDf, stockNamesDf = csv_to_clean_dataframe(csvPath) # NOTE: NAN values removed
lag = 0

adjMatSpearman = from_data_to_adjacencyMat(cleanDf, method='spearman', lag=lag)
# adjMatSpearman = threshold_adjMat(adjMatSpearman)
store_adjMatrix(adjMatSpearman, columnNames=np.squeeze(stockNamesDf.values), dataSetName=dataSetName, method='spearman', lag=lag)
