#!/bin/sh

# generate walktrap clusters
python ./src/clustering/walktrap_clustering.py ./data/protein.links.yeast.experiment.txt -p > ./data/clusters/yeast_ppi_wt.txt
python ./src/clustering/walktrap_clustering.py ./data/dsd/yeast/yeast_network_0_filtered_4.dsd -n ./data/dsd/yeast/yeast_network_0_filtered_4.nodelist > ./data/clusters/yeast_dsd_4_spectral.txt
python ./src/clustering/walktrap_clustering.py ./data/dsd/yeast/yeast_network_0_filtered_4.5.dsd -n ./data/dsd/yeast/yeast_network_0_filtered_4.5.nodelist > ./data/clusters/yeast_dsd_4.5_spectral.txt
python ./src/clustering/walktrap_clustering.py ./data/dsd/yeast/yeast_network_0_filtered_5.dsd -n ./data/dsd/yeast/yeast_network_0_filtered_5.nodelist > ./data/clusters/yeast_dsd_5_spectral.txt
python ./src/clustering/walktrap_clustering.py ./data/dsd/yeast/yeast_network_0_filtered_5.5.dsd -n ./data/dsd/yeast/yeast_network_0_filtered_5.5.nodelist > ./data/clusters/yeast_dsd_5.5_spectral.txt
python ./src/clustering/walktrap_clustering.py ./data/dsd/yeast/yeast_network_0_filtered_6.dsd -n ./data/dsd/yeast/yeast_network_0_filtered_6.nodelist > ./data/clusters/yeast_dsd_6_spectral.txt

# generate modified walktrap clusters
# because we're working directly from c++ source, this has a lot of steps

# generate yeast network with integer node mapping
mkdir -p data/walktrap
python ./src/clustering/walktrap/yeast_to_numeric.py ./data/protein.links.yeast.experiment.txt > ./data/walktrap/yeast_mapped.txt
mv node_map.txt ./data/walktrap/yeast_map.txt

# run walktrap and clean results
./src/clustering/walktrap/walktrap ./data/walktrap/yeast_mapped.txt -p200 -d1 > ./data/walktrap/p200_no_recursion_raw.txt
python ./src/clustering/walktrap/wt_output_to_csv.py ./data/walktrap/p200_no_recursion_raw.txt > ./data/walktrap/p200_no_recursion_clean.txt
python ./src/clustering/walktrap/simple_join.py ./data/walktrap/p200_no_recursion_clean.txt ./data/walktrap/yeast_map.txt > ./data/walktrap/p200_no_recursion_final.txt
python ./src/clustering/filter_clusters.py ./data/walktrap/p200_no_recursion_final.txt > ./data/walktrap/p200_no_recursion_final_filtered.txt

./src/clustering/walktrap/walktrap ./data/walktrap/yeast_mapped.txt -p300 -d1 > ./data/walktrap/p300_no_recursion_raw.txt
python ./src/clustering/walktrap/wt_output_to_csv.py ./data/walktrap/p300_no_recursion_raw.txt > ./data/walktrap/p300_no_recursion_clean.txt
python ./src/clustering/walktrap/simple_join.py ./data/walktrap/p300_no_recursion_clean.txt ./data/walktrap/yeast_map.txt > ./data/walktrap/p300_no_recursion_final.txt
python ./src/clustering/filter_clusters.py ./data/walktrap/p300_no_recursion_final.txt > ./data/walktrap/p300_no_recursion_final_filtered.txt

# generate edge list/mapping from filtered DSD matrix
python ./src/clustering/walktrap/dsd_to_numeric.py /r/bcb/clustering_paper/yeast_network_0_filtered_4_5.dsd /r/bcb/shalls/networks/yeast_network_0.nodelist > ./data/walktrap/yeast_dsd_4_5.txt
mv dsd_node_map.txt ./data/walktrap/yeast_dsd_4_5_map.txt
python ./src/clustering/walktrap/dsd_to_numeric.py /r/bcb/clustering_paper/yeast_network_0_filtered_5.dsd /r/bcb/shalls/networks/yeast_network_0.nodelist > ./data/walktrap/yeast_dsd_5.txt
mv dsd_node_map.txt ./data/walktrap/yeast_dsd_5_map.txt
python ./src/clustering/walktrap/dsd_to_numeric.py /r/bcb/clustering_paper/yeast_network_0_filtered_5_5.dsd /r/bcb/shalls/networks/yeast_network_0.nodelist > ./data/walktrap/yeast_dsd_5_5.txt
mv dsd_node_map.txt ./data/walktrap/yeast_dsd_5_5_map.txt
python ./src/clustering/walktrap/dsd_to_numeric.py /r/bcb/clustering_paper/yeast_network_0_filtered_6.dsd /r/bcb/shalls/networks/yeast_network_0.nodelist > ./data/walktrap/yeast_dsd_6.txt
mv dsd_node_map.txt ./data/walktrap/yeast_dsd_6_map.txt
python ./src/clustering/walktrap/dsd_to_numeric.py /r/bcb/clustering_paper/yeast_network_0_filtered_6_5.dsd /r/bcb/shalls/networks/yeast_network_0.nodelist > ./data/walktrap/yeast_dsd_6_5.txt
mv dsd_node_map.txt ./data/walktrap/yeast_dsd_6_5_map.txt

# run walktrap on initial thing, and clean results
./src/clustering/walktrap/walktrap ./data/walktrap/yeast_dsd_4_5.txt -p200 -d1 > ./data/walktrap/dsd_4_5_p200_raw.txt
python ./src/clustering/walktrap/wt_output_to_csv.py ./data/walktrap/dsd_4_5_p200_raw.txt > ./data/walktrap/dsd_4_5_p200_clean.txt
python ./src/clustering/walktrap/simple_join.py ./data/walktrap/dsd_4_5_p200_clean.txt ./data/walktrap/yeast_dsd_4_5_map.txt > ./data/walktrap/dsd_4_5_p200_final.txt
python ./src/clustering/filter_clusters.py ./data/walktrap/dsd_4_5_p200_final.txt > ./data/walktrap/dsd_4_5_p200_final_filtered.txt

./src/clustering/walktrap/walktrap ./data/walktrap/yeast_dsd_5.txt -p200 -d1 > ./data/walktrap/dsd_5_p200_raw.txt
python ./src/clustering/walktrap/wt_output_to_csv.py ./data/walktrap/dsd_5_p200_raw.txt > ./data/walktrap/dsd_5_p200_clean.txt
python ./src/clustering/walktrap/simple_join.py ./data/walktrap/dsd_5_p200_clean.txt ./data/walktrap/yeast_dsd_5_map.txt > ./data/walktrap/dsd_5_p200_final.txt
python ./src/clustering/filter_clusters.py ./data/walktrap/dsd_5_p200_final.txt > ./data/walktrap/dsd_5_p200_final_filtered.txt

./src/clustering/walktrap/walktrap ./data/walktrap/yeast_dsd_5_5.txt -p200 -d1 > ./data/walktrap/dsd_5_5_p200_raw.txt
python ./src/clustering/walktrap/wt_output_to_csv.py ./data/walktrap/dsd_5_5_p200_raw.txt > ./data/walktrap/dsd_5_5_p200_clean.txt
python ./src/clustering/walktrap/simple_join.py ./data/walktrap/dsd_5_5_p200_clean.txt ./data/walktrap/yeast_dsd_5_5_map.txt > ./data/walktrap/dsd_5_5_p200_final.txt
python ./src/clustering/filter_clusters.py ./data/walktrap/dsd_5_5_p200_final.txt > ./data/walktrap/dsd_5_5_p200_final_filtered.txt

./src/clustering/walktrap/walktrap ./data/walktrap/yeast_dsd_6.txt -p200 -d1 > ./data/walktrap/dsd_6_p200_raw.txt
python ./src/clustering/walktrap/wt_output_to_csv.py ./data/walktrap/dsd_6_p200_raw.txt > ./data/walktrap/dsd_6_p200_clean.txt
python ./src/clustering/walktrap/simple_join.py ./data/walktrap/dsd_6_p200_clean.txt ./data/walktrap/yeast_dsd_6_map.txt > ./data/walktrap/dsd_6_p200_final.txt
python ./src/clustering/filter_clusters.py ./data/walktrap/dsd_6_p200_final.txt > ./data/walktrap/dsd_6_p200_final_filtered.txt

./src/clustering/walktrap/walktrap ./data/walktrap/yeast_dsd_6_5.txt -p200 -d1 > ./data/walktrap/dsd_6_5_p200_raw.txt
python ./src/clustering/walktrap/wt_output_to_csv.py ./data/walktrap/dsd_6_5_p200_raw.txt > ./data/walktrap/dsd_6_5_p200_clean.txt
python ./src/clustering/walktrap/simple_join.py ./data/walktrap/dsd_6_5_p200_clean.txt ./data/walktrap/yeast_dsd_6_5_map.txt > ./data/walktrap/dsd_6_5_p200_final.txt
python ./src/clustering/filter_clusters.py ./data/walktrap/dsd_6_5_p200_final.txt > ./data/walktrap/dsd_6_5_p200_final_filtered.txt

./src/clustering/walktrap/walktrap ./data/walktrap/yeast_dsd_4_5.txt -p300 -d1 > ./data/walktrap/dsd_4_5_p300_raw.txt
python ./src/clustering/walktrap/wt_output_to_csv.py ./data/walktrap/dsd_4_5_p300_raw.txt > ./data/walktrap/dsd_4_5_p300_clean.txt
python ./src/clustering/walktrap/simple_join.py ./data/walktrap/dsd_4_5_p300_clean.txt ./data/walktrap/yeast_dsd_4_5_map.txt > ./data/walktrap/dsd_4_5_p300_final.txt
python ./src/clustering/filter_clusters.py ./data/walktrap/dsd_4_5_p300_final.txt > ./data/walktrap/dsd_4_5_p300_final_filtered.txt

./src/clustering/walktrap/walktrap ./data/walktrap/yeast_dsd_5.txt -p300 -d1 > ./data/walktrap/dsd_5_p300_raw.txt
python ./src/clustering/walktrap/wt_output_to_csv.py ./data/walktrap/dsd_5_p300_raw.txt > ./data/walktrap/dsd_5_p300_clean.txt
python ./src/clustering/walktrap/simple_join.py ./data/walktrap/dsd_5_p300_clean.txt ./data/walktrap/yeast_dsd_5_map.txt > ./data/walktrap/dsd_5_p300_final.txt
python ./src/clustering/filter_clusters.py ./data/walktrap/dsd_5_p300_final.txt > ./data/walktrap/dsd_5_p300_final_filtered.txt

./src/clustering/walktrap/walktrap ./data/walktrap/yeast_dsd_5_5.txt -p300 -d1 > ./data/walktrap/dsd_5_5_p300_raw.txt
python ./src/clustering/walktrap/wt_output_to_csv.py ./data/walktrap/dsd_5_5_p300_raw.txt > ./data/walktrap/dsd_5_5_p300_clean.txt
python ./src/clustering/walktrap/simple_join.py ./data/walktrap/dsd_5_5_p300_clean.txt ./data/walktrap/yeast_dsd_5_5_map.txt > ./data/walktrap/dsd_5_5_p300_final.txt
python ./src/clustering/filter_clusters.py ./data/walktrap/dsd_5_5_p300_final.txt > ./data/walktrap/dsd_5_5_p300_final_filtered.txt

./src/clustering/walktrap/walktrap ./data/walktrap/yeast_dsd_6.txt -p300 -d1 > ./data/walktrap/dsd_6_p300_raw.txt
python ./src/clustering/walktrap/wt_output_to_csv.py ./data/walktrap/dsd_6_p300_raw.txt > ./data/walktrap/dsd_6_p300_clean.txt
python ./src/clustering/walktrap/simple_join.py ./data/walktrap/dsd_6_p300_clean.txt ./data/walktrap/yeast_dsd_6_map.txt > ./data/walktrap/dsd_6_p300_final.txt
python ./src/clustering/filter_clusters.py ./data/walktrap/dsd_6_p300_final.txt > ./data/walktrap/dsd_6_p300_final_filtered.txt

./src/clustering/walktrap/walktrap ./data/walktrap/yeast_dsd_6_5.txt -p300 -d1 > ./data/walktrap/dsd_6_5_p300_raw.txt
python ./src/clustering/walktrap/wt_output_to_csv.py ./data/walktrap/dsd_6_5_p300_raw.txt > ./data/walktrap/dsd_6_5_p300_clean.txt
python ./src/clustering/walktrap/simple_join.py ./data/walktrap/dsd_6_5_p300_clean.txt ./data/walktrap/yeast_dsd_6_5_map.txt > ./data/walktrap/dsd_6_5_p300_final.txt
python ./src/clustering/filter_clusters.py ./data/walktrap/dsd_6_5_p300_final.txt > ./data/walktrap/dsd_6_5_p300_final_filtered.txt
