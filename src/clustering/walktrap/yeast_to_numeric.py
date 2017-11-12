import sys
def main():
    f = open(sys.argv[1])
    node_map = {}
    node_index = 0
    for line in f.readlines():
        l = line.rstrip().split()
        if l[0] not in node_map:
            node_map[l[0]] = node_index
            node_index += 1
        if l[1] not in node_map:
            node_map[l[1]] = node_index
            node_index += 1
    node_map_file = open('node_map.txt', 'w')
    for (node, nix) in node_map.iteritems():
        node_map_file.write('{} {}\n'.format(node, nix))
    node_map_file.close()
    f.seek(0)
    for line in f.readlines():
        l = line.rstrip().split()
        n1, n2, weight = l[0], l[1], l[2]
        print('{} {} {}'.format(node_map[n1], node_map[n2], weight))

main()

