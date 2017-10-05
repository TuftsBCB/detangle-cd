import numpy as np

def parsePPIP(filename, adjacency, names, pathways, count, i_map, next_map, addUnsupportedEdges = True, mode = 3):
    """
    filename - the name of the input file to be parsed, which should
        be a tab-delimited file with col1 as the source and col2
        as the destination of each edge.

    adjacency - the nxn adjacency matrix from reading the PPI

    names - the mapping of protein names to array indices

    pathways - a i x n x n array, where i is the number of existing pathways
        and n is the size of the adjacency matrix.  pathway[k][i][j] = 1 indicates
        that the edge at i,j is part of pathway k

    count - load this pathway into pathway[count]

    i_map - used later, when building the transition matrix.  Maps (original node, path)
        to the index of the new node

    next_map - next available index for i_map

    addUnsupportedEdges - toggle whether or not to toggle adjacency[i,j] to 1
        upon adding a pathway
        
    mode - 1 if all edges are treated as directed.  2 if all edges are treated as undirected.  3 if only edges
        listed in dtypes are treated as directed.  Mode = 3 gives the sane results.
    """

    f = open(filename, 'r')
    dtypes = ["activation", "inhibition", "phosphorylation", "dephosphorylation", "ubiquitination"]

    for line in f:
        line = line.rstrip().split()
        type = line[2:]
        isdir = (mode == 1) or (mode == 3)
        if isdir and mode == 3:
            for t in type:
                if t not in dtypes: isdir = False
        try:
            i, j = names[line[0]], names[line[1]]
            pathways[count][i][j] = 1
            if not isdir: pathways[count][j][i] = 1
            for key in [(i, count), (j, count)]:
                if key not in i_map:
                    i_map[key] = next_map
                    next_map+=1
            if addUnsupportedEdges: # and not adjacency[i][j]:
                adjacency[i][j] = 1
                if not isdir: adjacency[j][i] = 1
        except:
            pass
    return (i_map, next_map) # i_map maps (original node number,  path num) to path node number
