#!/bin/sh

# generate yeast network with integer node mapping
# python yeast_to_numeric.py /r/bcb/shalls/protein.links.yeast.experiment.txt > yeast_mapped.txt
# mv node_map.txt yeast_map.txt

# run walktrap on initial thing, and clean results
../walktrap yeast_mapped.txt -p800 -d1 > ../results/p800_no_recursion_raw.txt
python wt_output_to_csv.py ../results/p800_no_recursion_raw.txt > ../results/p800_no_recursion_clean.txt

# there aren't any singletons in this case, so skip that step
# TODO: build clusters from results
python simple_join.py ../results/p800_no_recursion_clean.txt yeast_map.txt > ../results/p800_no_recursion_final.txt
python /r/bcb/dream11/clustering/filter_clusters.py ../results/p800_no_recursion_final.txt > ../results/p800_no_recursion_final_filtered.txt

# run enrichment on non-recursive results
# python /r/bcb/shalls/eval_yeast.py ../results/p800_no_recursion_final_filtered.txt > ../results/p800_no_recursion_final_enrichment.txt
