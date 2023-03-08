from src.ClassDSBM import DSBM
from utils.math_functions import np
from utils.plotting_functions import visualise_digraph, plt

k, n, p, q = 3, 3, 1., 0.
g = DSBM(k=k, n=n, p=p, q=q, F=None)

nodes, edges = g.simulate()
visualise_digraph(nodes, edges, plottitle="$p = q$ Dense DSBM Network")
plt.savefig("../pngs/IsolatedDSBMNetwork.png", bbox_inches="tight", transparent=False)
plt.show()
