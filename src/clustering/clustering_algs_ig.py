"""
Implementations of some graph clustering algorithms

TODO: thresholding, SPICi, spectral clustering
      (with documentation)

"""
import igraph as ig
import numpy as np
import sklearn.cluster as sc

def threshold_clustering(G, threshold, node_map=[], objects=False):
    """ Calculate threshold clusters for the given similarity scores.

    Args:
        G (ig.Graph)      - the input network
        threshold (float) - the weight above which to remove edges

    Returns:
        clusters (list) - a list of lists of nodes, each sublist represents
                          a cluster
    """
    edges = []
    for edge in G.es:
        edges.append((edge.tuple[0], edge.tuple[1], edge['weight']))
    edges_to_remove = [(n1, n2) for n1, n2, w in edges if w > threshold]
    G.delete_edges(edges_to_remove)

    # hopefully the graph is disconnected now, so filter nodes into bins
    if objects: return G.clusters().subgraphs()
    else:
        clusters = [c for c in G.clusters()]
        if node_map:
            return [[node_map[n] for n in cl] for cl in clusters]
        else: return clusters

def spectral_clustering(G, n_clusters=8, node_map=[], no_conversion=False,
                        simple_conversion=False):
    """ Cluster the given similarity matrix using spectral clustering.

    Assumes the given similarity network is connected.

    Args:
        G (ig.Graph)     - the input network
        n_clusters (int) - number of clusters to look for

    Returns:
        clusters (list) - a list of lists of nodes, each sublist represents
                          a cluster
    """
    # generate a numpy distance matrix from the given graph
    mat = G.get_adjacency(attribute='weight')
    dist_matrix = np.array(mat.data)

    if no_conversion:
        sim_matrix = dist_matrix
    elif simple_conversion:
        # take simple inverse to get similarity from distance
        sim_fn = np.vectorize(lambda x: 0 if x == 0 else 1 / float(x),
                              otypes=[np.float])
        sim_matrix = sim_fn(dist_matrix)
    else:
        # apply RBF kernel to generate similarity matrix from distance
        # matrix (i.e. lower DSD => higher similarity)
        std_dev = dist_matrix.std()
        sim_fn = np.vectorize(lambda x: 0 if x == 0
                                          else np.exp(-(x) / (2 * (std_dev) ** 2)),
                              otypes=[np.float])
        sim_matrix = sim_fn(dist_matrix)

    # now do the clustering, scikit-learn implements this
    # return a list of lists representing the clusters
    node_assignments = list(sc.spectral_clustering(sim_matrix, n_clusters))
    clusters = []
    for n in xrange(n_clusters):
        clusters.append([i for i, m in enumerate(node_assignments) if m == n])
    if node_map:
        return [[node_map[n] for n in cl] for cl in clusters]
    else: return clusters

def hierarchical_clustering(G, threshold=1.0):
    """ Hierarchical clustering using shortest path distances.

    For use as a baseline comparison against our DSD-based methods.
    """
    # TODO: not yet implemented using igraph
    pass

