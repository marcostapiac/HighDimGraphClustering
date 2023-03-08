from utils.math_functions import pd, np
from utils.plotting_functions import visualise_digraph
from utils.data_processing import csv_to_clean_dataframe, from_data_to_adjacencyMat, store_adjMatrix, threshold_adjMat

dataSetName = "OPCL_20000103_20201231"
csvPath = "../data/" + dataSetName + ".csv"
rawDf, cleanDf, stockNames = csv_to_clean_dataframe(csvPath)  # NOTE:
lag = 0

adjMatDistance = from_data_to_adjacencyMat(cleanDf, method='distance', lag=lag)
# adjMatDistance = threshold_adjMat(adjMatDistance)
store_adjMatrix(adjMatDistance, columnNames=stockNames.array, dataSetName=dataSetName, method='distance', lag=lag)
