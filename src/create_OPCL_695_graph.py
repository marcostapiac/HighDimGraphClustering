from utils.math_functions import pd
from utils.plotting_functions import plt, visualise_digraph

dataSetName = "OPCL_20000103_20201231"
methods = ["pearson", "kendall"]
for method in methods:
    csvPath = "../data/adjMat_"+dataSetName+"_" + method + ".gzip"
    df = pd.read_csv(csvPath, compression="gzip")
    visualise_digraph(df.columns.array, df.to_numpy(), plottitle="Graph for " + method + " correlation metric")
    plt.savefig("../pngs/" + dataSetName + "_" + method +  ".png", bbox_inches="tight", transparent=False)
    plt.show()
    plt.close()