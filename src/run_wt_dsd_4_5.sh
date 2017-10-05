#!/bin/sh

# generate edge list/mapping from filtered DSD matrix
python dsd_to_numeric.py /r/bcb/clustering_paper/yeast_network_0_filtered_4_5.dsd /r/bcb/shalls/networks/yeast_network_0.nodelist > yeast_dsd_4_5.txt
mv dsd_node_map.txt yeast_dsd_4_5_map.txt

# run walktrap on initial thing, and clean results
../walktrap yeast_dsd_4_5.txt -p800 -d1 > ../results/dsd_4_5_p800_raw.txt
python wt_output_to_csv.py ../results/dsd_4_5_p800_raw.txt > ../results/dsd_4_5_p800_clean.txt

# there aren't any singletons in this case, so skip that step
python simple_join.py ../results/dsd_4_5_p800_clean.txt yeast_dsd_4_5_map.txt > ../results/dsd_4_5_p800_final.txt
python /r/bcb/dream11/clustering/filter_clusters.py ../results/dsd_4_5_p800_final.txt > ../results/dsd_4_5_p800_final_filtered.txt

# run enrichment on non-recursive results
# python /r/bcb/shalls/eval_yeast.py ../results/dsd_4_5_p800_final_filtered.txt > ../results/dsd_4_5_p800_final_enrichment.txt
