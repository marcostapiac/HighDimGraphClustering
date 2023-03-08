from utils.math_functions import np


class DSBM:
    def __init__(self, k, n, p, q, F=None):
        self.clusterNum = k
        self.pcNodes = n
        self.interClusterEdgeProb = p
        self.intraClusterEdgeProb = q
        if F is None:
            self.metaMatrix = self.generate_meta_graph()
        else:
            self.metaMatrix = F

    def generate_meta_graph(self):
        # TODO: Faster generation of meta graph
        k = self.clusterNum
        F = np.zeros(shape=(k, k))
        for i in range(k):
            F[i, i:] = np.random.uniform(0., 1., size=k - i)
            F[i:, i] = 1. - F[i, i:]
            F[i, i] = 0.5
        return F

    def get_clustered_nodes(self):
        dps = np.reshape(
            np.array([["N" + str(i * self.pcNodes + j) for j in range(self.pcNodes)] for i in range(self.clusterNum)]),
            (self.clusterNum, self.pcNodes))  # k clusters, each with n nodes
        assert (dps.shape == (self.clusterNum, self.pcNodes))
        return dps

    def generate_edges(self):
        """ We assume for DSBM models that the clusters are alog the diagonal"""
        N = self.clusterNum * self.pcNodes
        edges = np.zeros(shape=(N, N))
        s = 0
        for i in range(N):
            if i % self.pcNodes == 0: s += 1
            for j in range(i, N):
                # Inter-cluster
                if j < self.pcNodes * s:
                    p = self.interClusterEdgeProb
                    isEdge = np.random.choice([1, 0], p=[p, 1. - p])
                    if i == j:
                        edges[i, j] = isEdge
                    else:
                        edges[i, j] = isEdge * np.random.choice([1, 0], p=[0.5, 0.5])
                        edges[j, i] = isEdge * (1 - edges[i, j])
                # Intra-cluster
                else:
                    p = self.intraClusterEdgeProb
                    isEdge = np.random.choice([1, 0], p=[p, 1. - p])
                    p = self.metaMatrix[i % self.clusterNum, j % self.clusterNum]
                    edges[i, j] = isEdge * (np.random.choice([1, 0], p=[p, 1. - p]))
                    edges[j, i] = isEdge * (1 - edges[i, j])
        return edges

    def simulate(self):
        cdNodes = self.get_clustered_nodes()
        edgeMatrix = self.generate_edges()
        return cdNodes, edgeMatrix
