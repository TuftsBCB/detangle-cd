from __future__ import division
import argparse
import pandas as pd

def get_files(ft):
    fs = []
    with open(ft, 'r') as f:
        for line in f:
            if line.strip() == '': continue
            l = line.strip().split()
            fs.append((l[1], l[0]))
    return fs

def get_row(ft, cutoff, louvain=False):
    row = [None] * 6
    enriched_clusters, total_clusters, percent_enriched = 0, 0, 0.0
    with open(ft, 'r') as f:
        for line in f:
            if line.startswith('Enriched'):
                # louvain is a median over many runs, so these may be floats
                # other methods only admit ints
                if louvain:
                    enriched_clusters = float(line.split()[-1])
                else:
                    enriched_clusters = int(line.split()[-1])
            elif line.startswith('Valid'):
                if louvain:
                    total_clusters = float(line.split()[-1])
                else:
                    total_clusters = int(line.split()[-1])
            elif line.startswith('Nodes placed'):
                l = line.strip().split()
                n, t = map(float, l[-2].split('/'))
                r = 100 * (n / t)
                row[2] = n
                row[3] = ('{:.2f}%'.format(r))
            elif line.startswith('Nodes correctly'):
                l = line.strip().split()
                n, t = map(float, l[-2].split('/'))
                r = 100 * (n / t)
                row[4] = n
                row[5] = ('{:.2f}%'.format(r))
    row[0] = cutoff.replace('original', 'PPI')
    row[1] = '{}/{} ({:.2f}%)'.format(enriched_clusters, total_clusters,
                                  (enriched_clusters / total_clusters) * 100)
    return row

def main():
    p = argparse.ArgumentParser()
    p.add_argument('file_file')
    p.add_argument('-l', '--latex', action='store_true',
                   help='write to latex, if not included writes to csv')
    p.add_argument('-o', '--output_file', required=False, default='table.txt')
    opts = p.parse_args()

    files = get_files(opts.file_file)
    df = None
    cols = ['Method', 'Enriched Clusters', '# NEC', '% NEC', '# NEC S', '% NEC S']
    for (file, cutoff) in files:
        is_louvain = 'louvain' in file
        row = get_row(file, cutoff, louvain=is_louvain)
        if df is None:
            df = pd.DataFrame([row], columns=cols)
        else:
            df = pd.concat([df, pd.DataFrame([row], columns=cols)])
    if opts.latex:
        col_format = '|r|r|r|r|r|r|'
        output_buf = df.to_latex(None, index=False, column_format=col_format)
        output_buf = output_buf.replace('\\\\', '\\\\ \\hline').replace('\\toprule', '\\hline').replace('\\midrule', '').replace('\\bottomrule', '').replace('\n\n', '\n')
        with open(opts.output_file, 'w') as f:
            f.write(output_buf)
    else:
        df.to_csv(opts.output_file, index=False)

if __name__ == '__main__':
    main()
