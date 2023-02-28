from utils.math_functions import pd, np
from utils.plotting_functions import visualise_digraph
from utils.data_processing import csv_to_clean_dataframe, from_data_to_adjacencyMat, store_adjMatrix, threshold_adjMat

dataSetName = "OPCL_20000103_20201231"
csvPath = "../data/"+dataSetName+".csv"
rawDf, cleanDf, stockNames = csv_to_clean_dataframe(csvPath)
lag = 1

adjMatPearson = from_data_to_adjacencyMat(cleanDf, method='pearson', lag=lag)
#adjMatPearson = threshold_adjMat(adjMatPearson)
store_adjMatrix(adjMatPearson, columnNames=stockNames.array,dataSetName=dataSetName, method='pearson',lag=lag)

adjMatKendall = from_data_to_adjacencyMat(cleanDf, method='kendall', lag=lag)
#adjMatPearson = threshold_adjMat(adjMatKendall)
store_adjMatrix(adjMatPearson, columnNames=stockNames.array,dataSetName=dataSetName, method='kendall',lag=lag)

adjMatDistance = from_data_to_adjacencyMat(cleanDf, method='distance', lag=lag)
#adjMatPearson = threshold_adjMat(adjMatDistance)
store_adjMatrix(adjMatPearson, columnNames=stockNames.array, dataSetName=dataSetName, method='distance', lag=lag)

print(adjMatPearson.shape, adjMatKendall.shape, adjMatDistance.shape)