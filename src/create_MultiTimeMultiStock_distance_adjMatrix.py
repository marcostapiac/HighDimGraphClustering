from utils.math_functions import pd, np
from utils.plotting_functions import visualise_digraph
from utils.data_processing import csv_to_clean_dataframe, from_data_to_adjacencyMat, store_adjMatrix, threshold_adjMat

dataSetName = "MultiFeature_MultiStock_time_series_1300_days"
csvPath = "../data/" + dataSetName + ".gzip"
rawDf, cleanDf, stockFeatureNamesDf = csv_to_clean_dataframe(csvPath,compression='gzip')  # NOTE:
lag = 0

adjMatDistance = from_data_to_adjacencyMat(cleanDf, method='distance', lag=lag)
#adjMatDistance = threshold_adjMat(adjMatDistance)
store_adjMatrix(adjMatDistance, columnNames=np.squeeze(stockFeatureNamesDf.values),dataSetName=dataSetName, method='distance',lag=lag)

