import sys

def main():
    f = open(sys.argv[1], 'r')
    for ix, line in enumerate(f.readlines()):
        if ix == 0: continue
        cluster = line.rstrip().split(' = ')[-1]
        cluster = cluster.replace('{', '').replace('}', '')
        print cluster

if __name__ == '__main__':
    main()
