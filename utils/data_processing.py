from utils.math_functions import pd, np, gammafnc
from tqdm import tqdm
import dcor
import dropbox
import io, re
from dropbox.exceptions import AuthError


def connect_dropbox():
    try:
        DROPBOX_ACCESS_TOKEN = 'sl.BaLIasOV2RIax2wEFeXHuiCX6W9t05Ygd_Vp_3GzE_7kYcgoMk8twq2xHJPppEGFVkqBGfeXjQ8HKppG5MQXdgIdbcuSQiuUya8hoqAjgFLgrfJ97vdAyTF8hEBV1oef7Wqyn-k'
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    except AuthError as e:
        print('Error connecting to Dropbox with access token: ' + str(e))
    else:
        return dbx


def dropbox_file_to_dataframe(stockNames, featureNames):
    """ Return dataframe containing |stockNames|x|featureNames| by T_Horizon"""
    dbx = connect_dropbox()
    result = dbx.files_list_folder("/US_CRSP_NYSE/Yearly/", recursive=True)
    entries = result.entries
    filePaths = []
    while result.has_more:
        result = dbx.files_list_folder_continue(cursor=result.cursor)
        entries += result.entries
    for entry in entries:
        if ".csv.gz" in entry.name:
            filePaths.append(entry.path_display)
    filePaths = sorted(filePaths, reverse=True)  # Reverse-chronological order

    names = [stock + "_" + feature for stock in stockNames for feature in featureNames]
    df = pd.DataFrame(names, columns=['ticker'])
    df.index = [stock + "_" + feature for stock in stockNames for feature in featureNames]
    for i in tqdm(range(len(filePaths))):
        filePath = filePaths[i]
        try:
            metadata, f = dbx.files_download(filePath)
        except Exception as e:
            print('Error downloading Dropbox file: ' + str(e))
        else:
            with io.BytesIO(f.content) as stream:
                df1 = pd.read_csv(stream, compression='gzip', index_col=0)
            df1.index = df1.iloc[:, 0]
            try:
                df1 = df1.iloc[:, 1:].loc[stockNames, featureNames].stack()
                df1.index = df.index
            except KeyError or ValueError as e:
                # TODO: ValueError arises when new df1 has 1 element less than df --> which element, and why?
                pass
                """invalidStockNames = re.findall('\[.*?]', e.args[0])[0]
                print(np.searchsorted(stockNames, invalidStockNames))
                validStockNames = np.delete(stockNames, np.argwhere(np.where((stockNames == invalidStockNames).all())))
                print(validStockNames)

                #df1 = df1.iloc[:, 1:].loc[validStockNames, featureNames].stack()
                #df1 = pd.concat(
                #    [df1, pd.DataFrame([np.nan for _ in range(len(invalidStockNames) * len(featureNames))],index=invalidStockNames)], join='inner', axis=1)
                #df1 = pd.DataFrame([np.nan for _ in range(len(df.index))])
                df1.index = df.index # Need to preserve row labels for correct concatenation"""
            else:
                dfNames = np.append(df.columns.values, [
                    "X" + filePath.replace(re.findall('\/.*\/', filePath)[0], "").replace(".csv.gz", "")])
                df = pd.concat([df, df1], ignore_index=False, axis=1)
                df.columns = dfNames  # Keep column names as time format
    df.set_index('ticker', inplace=True) # Remove row indexing for convenience later on
    return df


def csv_to_clean_dataframe(csvPath, compression=None):
    df = pd.read_csv(csvPath, compression=compression)
    cleanDf = df.dropna(axis=0)
    stockNamesSeries = cleanDf.iloc[:, 0]  # Will form node names
    if cleanDf.columns.shape[0] == 1:
        return df, cleanDf, pd.DataFrame(stockNamesSeries)
    return df, cleanDf.iloc[:, 1:], pd.DataFrame(stockNamesSeries)


def from_data_to_adjacencyMat(cleanDf, method, lag=0):
    N = cleanDf.shape[0]
    if method == 'spearman' or method == 'kendall':
        # Do not care about lagged auto-correlation
        adjMat = cleanDf.T.corr(method=method).to_numpy() - np.eye(N)
        return adjMat  # cleanDf.corrwith(cleanDf.shift(periods=lag), axis=0, method=method).to_numpy() - np.eye(N)
    elif method == 'distance':
        T = cleanDf.shape[1]
        adjMat = np.zeros(shape=(N, N))
        # TODO: EFFICIENCY/Parallelise
        for i in tqdm(range(N)):
            for j in range(i + 1, N):
                metric = dcor.distance_correlation(x=cleanDf.iloc[i, :T - lag].array, y=cleanDf.iloc[j, lag:].array)
                adjMat[i, j] = metric
                if lag == 0:
                    adjMat[j, i] = metric
                else:
                    adjMat[j, i] = dcor.distance_correlation(x=cleanDf.iloc[j, :T - lag], y=cleanDf.iloc[i, lag:])
        return adjMat


def threshold_adjMat(adjMat, method, alpha=0.01):
    # TODO: Threshold similarity metrics
    pass


def store_df(df, name, compression="gzip", isIndex=False):
    df.to_csv(name, compression=compression, index=isIndex)


def store_adjMatrix(adjMat, dataSetName, method, lag, columnNames=None):
    print(columnNames.shape, adjMat.shape)
    adjDf = pd.DataFrame(adjMat, columns=columnNames)
    name = "../data/" + "adjMat_" + dataSetName + "_" + method + "_lag_" + str(lag) + ".gzip"
    store_df(adjDf, name)
