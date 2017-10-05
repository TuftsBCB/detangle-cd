#!/usr/bin/env python
import sys
import numpy as np
import igraph as ig

def get_node_list(node_file):
    node_list = []
    try:
        fp = open(node_file, 'r')
    except IOError:
        sys.exit('Could not open file: {}'.format(node_file))

    # read the first (i.e. largest) connected component
    cur_line = fp.readline()
    while cur_line and not cur_line.isspace():
        if cur_line and not cur_line.startswith('Component'):
            node_list.append(cur_line.rstrip())
        cur_line = fp.readline()

    fp.close()
    return node_list

def main():
    matrix = np.loadtxt(sys.argv[1])
    node_list = get_node_list(sys.argv[2])
    G = ig.Graph.Weighted_Adjacency(matrix.tolist(), mode=ig.ADJ_UNDIRECTED)
    G.vs['name'] = node_list

    # write node list to file
    '''
    f = open('dsd_node_map.txt', 'w')
    for v in G.vs:
        f.write('{} {}\n'.format(v['name'], v.index))
    f.close()
    '''

    # write edges to stdout
    node_map = {}
    cur_index = 0
    for e in G.es:
        name1, name2 = G.vs[e.source]['name'], G.vs[e.target]['name']
        if name1 not in node_map:
            node_map[name1] = cur_index
            cur_index += 1
        if name2 not in node_map:
            node_map[name2] = cur_index
            cur_index += 1
        sim_score = 1 / float(e['weight'])
        print('{} {} {}'.format(node_map[name1], node_map[name2], sim_score))
        # print('{} {} {}'.format(node_map[name1], node_map[name2], e['weight']))

    f = open('dsd_node_map.txt', 'w')
    for name, ix in node_map.iteritems():
        f.write('{} {}\n'.format(name, ix))
    f.close()


if __name__ == '__main__':
    main()
