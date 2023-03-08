from utils.data_processing import dropbox_file_to_dataframe, csv_to_clean_dataframe, store_df
from utils.math_functions import np

dataSetName = "OPCL_695_stock_names"
csvPath = "../data/" + dataSetName + ".csv"
_, _, stockNamesDf = csv_to_clean_dataframe(csvPath)

df = dropbox_file_to_dataframe(np.squeeze(stockNamesDf.values), np.array(["high", "low", "OPCL", "pvCLCL", "volume"]))
name = "../data/MultiFeature_MultiStock_time_series_1300_days.gzip"
store_df(df, name, compression='gzip', isIndex=True)
print(df)
