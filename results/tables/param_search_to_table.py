from __future__ import division, print_function
import argparse
import pandas as pd


def parse_output_dir(output_dir, nec_s):
    import os, re
    import pandas as pd
    cols = ['200', '300', '500', '700']
    file_hashes = ['ppi', 'dsd_4_5', 'dsd_5', 'dsd_5_5', 'dsd_6', 'dsd_6_5']
    rows = {k: [-1 for _ in range(len(cols))] for k in file_hashes}
    p = re.compile('p[\d]+')

    for fname in os.listdir(output_dir):
        if fname.startswith('.') or fname.split('.')[-1] != 'txt': continue
        if fname == 'log.txt': continue
        full_fname = os.path.join(os.path.abspath(output_dir), fname)
        try:
            row_index = [ix for ix in file_hashes if ix in fname]
            row_index = sorted(row_index, key=lambda x: len(x))[-1]
            cutoff = p.search(fname).group().replace('p', '')
            enr_val = get_value(full_fname, nec_s=nec_s)
            rows[row_index][cols.index(cutoff)] = str(enr_val) + '%'
        except AttributeError: continue # no match found, ignore the file
        except IndexError: continue # no row index found
        except ValueError: continue # skip cols that we're not using in final tables
    df = pd.DataFrame.from_dict(rows, orient='index')
    df.columns = cols
    df = df.loc[file_hashes]
    return df

def get_value(fname, nec_s=False):
    import os
    with open(os.path.abspath(fname), 'r') as f:
        for line in f:
            if nec_s:
                if line.startswith('Nodes correctly clustered'):
                    return float(line.split(' ')[-1].replace('(', '').replace(')', '').replace('%', '')) * 100
            else:
                if line.startswith('Nodes placed'):
                    return float(line.split(' ')[-1].replace('(', '').replace(')', '').replace('%', '')) * 100

def main():
    p = argparse.ArgumentParser()
    p.add_argument('output_dir')
    p.add_argument('-l', '--latex', action='store_true',
                   help='write to latex, if not included writes to csv')
    p.add_argument('-o', '--output_file', required=False, default='table.txt')
    p.add_argument('-s', '--nec_s', action='store_true')
    args = p.parse_args()

    ps_table = parse_output_dir(args.output_dir, args.nec_s)
    ps_table.index.name = 'Dendrogram cut level'
    if args.latex:
        # col_format = '|r|r|r|r|r|r|r|r|'
        col_format = '|{}|'.format('|'.join(['r' for _ in range(len(ps_table.columns)+1)]))
        ps_table.reset_index(level=0, inplace=True)
        ps_table['Dendrogram cut level'] = ps_table['Dendrogram cut level'].map(lambda x: x.replace('dsd_', '').replace('_', '.'))
        output_buf = ps_table.to_latex(None, index=False, column_format=col_format)
        output_buf = output_buf.replace('\\\\', '\\\\ \\hline').replace('\\toprule', '\\hline').replace('\\midrule', '').replace('\\bottomrule', '').replace('\n\n', '\n')
        with open(args.output_file, 'w') as f:
            f.write(output_buf)
    else:
        ps_table.to_csv(args.output_file)

if __name__ == '__main__':
    main()
