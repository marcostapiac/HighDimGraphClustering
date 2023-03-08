from utils.math_functions import pd, np
from utils.plotting_functions import visualise_digraph
from utils.data_processing import csv_to_clean_dataframe, from_data_to_adjacencyMat, store_adjMatrix, threshold_adjMat

dataSetName = "pvCLCL_20000103_20201231"
csvPath = "../data/" + dataSetName + ".csv"
rawDf, cleanDf, stockNames = csv_to_clean_dataframe(csvPath)  # NOTE:
print(cleanDf.shape)
lag = 0

adjMatKendall = from_data_to_adjacencyMat(cleanDf, method='kendall', lag=lag)
#adjMatKendall = threshold_adjMat(adjMatKendall)
store_adjMatrix(adjMatKendall, columnNames=stockNames.array,dataSetName=dataSetName, method='kendall',lag=lag)

