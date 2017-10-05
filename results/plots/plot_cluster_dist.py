import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from ast import literal_eval

light_blue = sns.color_palette("Blues")[2]
dark_blue = sns.color_palette("Blues")[4]
light_green = sns.color_palette("Greens")[2]
dark_green = sns.color_palette("Greens")[4]

label_map = {
    4: '3-4',
    8: '5-8',
    16: '9-16',
    32: '17-32',
    64: '33-64',
    128: '65-100'
    # 128: '65-128',
    # 256: '129-256',
    # 512: '257-512',
    # 1024: '513-1024',
    # 2048: '1025-2048'
}

p = argparse.ArgumentParser()
p.add_argument('cluster_file_1')
p.add_argument('cluster_file_2')
p.add_argument('-o', '--output_file', required=False, default='figure.png')
p.add_argument('-n', '--method_name', required=False, default='spectral')
opts = p.parse_args()

ALL_L1 = 'not significantly enriched - {}'.format(opts.method_name)
ALL_L2 = 'not significantly enriched - DSD+{}'.format(opts.method_name)
SIG_L1 = 'enriched - {}'.format(opts.method_name)
SIG_L2 = 'enriched - DSD+{}'.format(opts.method_name)

def get_bins_cls(cluster_file):
    bins_cls = []
    cls_count = 0
    with open(cluster_file, 'r') as f:
        for line in f:
            if line[0] == '[' and line[1] != ']' and cls_count < 2:
                bins_cls.append(literal_eval(line.strip()))
                cls_count += 1
    bins_cls = [sorted(l, key=lambda x: x[0]) for l in bins_cls]
    return bins_cls

bins1, cls1 = get_bins_cls(opts.cluster_file_1)
bins2, cls2 = get_bins_cls(opts.cluster_file_2)

all_list, enriched_list = [], []

for bin in bins1:
    all_list.append((label_map[bin[0]], bin[1], 'cl1'))

for bin in bins2:
    all_list.append((label_map[bin[0]], bin[1], 'cl2'))

for cl in cls1:
    enriched_list.append((label_map[cl[0]], cl[1], 'cl1'))

for cl in cls2:
    enriched_list.append((label_map[cl[0]], cl[1], 'cl2'))

df_all = pd.DataFrame(all_list)
df_enriched = pd.DataFrame(enriched_list)

sns.barplot(x=0, y=1, hue=2, data=df_all, palette=[light_blue, light_green])
sns.barplot(x=0, y=1, hue=2, data=df_enriched, palette=[dark_blue, dark_green])
plt.xlabel("Cluster size range")
plt.ylabel("Number of clusters")
lgd = plt.legend(loc='center right', bbox_to_anchor=(1.55, 0.5))
texts = lgd.get_texts()
texts[0].set_text(ALL_L1)
texts[1].set_text(ALL_L2)
texts[2].set_text(SIG_L1)
texts[3].set_text(SIG_L2)
plt.savefig(opts.output_file, bbox_extra_artists=(lgd,), bbox_inches='tight')

