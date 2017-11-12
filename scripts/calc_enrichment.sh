#!/bin/sh

mkdir -p ./data/enrichment

# spectral, no splitting large clusters
python ./src/eval_yeast_associations.py ./data/clusters/yeast/yeast_ppi_spectral_300_filtered.txt ./data/yeast_ppi.nodelist -a ./data/associations/fa_associations_070117_l5.txt -f 50 > ./data/enrichment/yeast_spectral_ppi_no_split.txt
python ./src/eval_yeast_associations.py ./data/clusters/yeast/yeast_dsd_4.5_spectral_300_filtered.txt ./data/dsd/yeast/yeast_network_0_filtered_4.5.nodelist -a ./data/associations/fa_associations_070117_l5.txt -f 50 > ./data/enrichment/yeast_spectral_4.5_no_split.txt
python ./src/eval_yeast_associations.py ./data/clusters/yeast/yeast_dsd_5_spectral_300_filtered.txt ./data/dsd/yeast/yeast_network_0_filtered_5.nodelist -a ./data/associations/fa_associations_070117_l5.txt -f 50 > ./data/enrichment/yeast_spectral_5_no_split.txt
python ./src/eval_yeast_associations.py ./data/clusters/yeast/yeast_dsd_5.5_spectral_300_filtered.txt ./data/dsd/yeast/yeast_network_0_filtered_5.5.nodelist -a ./data/associations/fa_associations_070117_l5.txt -f 50 > ./data/enrichment/yeast_spectral_5.5_no_split.txt
python ./src/eval_yeast_associations.py ./data/clusters/yeast/yeast_dsd_6_spectral_300_filtered.txt ./data/dsd/yeast/yeast_network_0_filtered_6.nodelist -a ./data/associations/fa_associations_070117_l5.txt -f 50 > ./data/enrichment/yeast_spectral_6_no_split.txt
python ./src/eval_yeast_associations.py ./data/clusters/yeast/yeast_dsd_6.5_spectral_300_filtered.txt ./data/dsd/yeast/yeast_network_0_filtered_6.5.nodelist -a ./data/associations/fa_associations_070117_l5.txt -f 50 > ./data/enrichment/yeast_spectral_6.5_no_split.txt

# spectral, splitting large clusters
python ./src/eval_yeast_associations.py ./data/clusters/yeast/yeast_ppi_spectral_300_split_filtered.txt ./data/yeast_ppi.nodelist -a ./data/associations/fa_associations_070117_l5.txt -f 50 > ./data/enrichment/yeast_spectral_ppi_split.txt
python ./src/eval_yeast_associations.py ./data/clusters/yeast/yeast_dsd_4.5_spectral_300_split_filtered.txt ./data/dsd/yeast/yeast_network_0_filtered_4.5.nodelist -a ./data/associations/fa_associations_070117_l5.txt -f 50 > ./data/enrichment/yeast_spectral_4.5_split.txt
python ./src/eval_yeast_associations.py ./data/clusters/yeast/yeast_dsd_5_spectral_300_split_filtered.txt ./data/dsd/yeast/yeast_network_0_filtered_5.nodelist -a ./data/associations/fa_associations_070117_l5.txt -f 50 > ./data/enrichment/yeast_spectral_5_split.txt
python ./src/eval_yeast_associations.py ./data/clusters/yeast/yeast_dsd_5.5_spectral_300_split_filtered.txt ./data/dsd/yeast/yeast_network_0_filtered_5.5.nodelist -a ./data/associations/fa_associations_070117_l5.txt -f 50 > ./data/enrichment/yeast_spectral_5.5_split.txt
python ./src/eval_yeast_associations.py ./data/clusters/yeast/yeast_dsd_6_spectral_300_split_filtered.txt ./data/dsd/yeast/yeast_network_0_filtered_6.nodelist -a ./data/associations/fa_associations_070117_l5.txt -f 50 > ./data/enrichment/yeast_spectral_6_split.txt
python ./src/eval_yeast_associations.py ./data/clusters/yeast/yeast_dsd_6.5_spectral_300_split_filtered.txt ./data/dsd/yeast/yeast_network_0_filtered_6.5.nodelist -a ./data/associations/fa_associations_070117_l5.txt -f 50 > ./data/enrichment/yeast_spectral_6.5_split.txt

# original walktrap
python ./src/eval_yeast_associations.py ./data/clusters/yeast_ppi_wt.txt ./data/yeast_ppi.nodelist -a ./data/associations/fa_associations_070117_l5.txt -f 50 > ./data/enrichment/yeast_wt_ppi.txt
python ./src/eval_yeast_associations.py ./data/clusters/yeast_dsd_4_wt.txt ./data/dsd/yeast/yeast_network_0_filtered_4.nodelist -a ./data/associations/fa_associations_070117_l5.txt -f 50 > ./data/enrichment/yeast_wt_4.txt
python ./src/eval_yeast_associations.py ./data/clusters/yeast_dsd_4.5_wt.txt ./data/dsd/yeast/yeast_network_0_filtered_4.5.nodelist -a ./data/associations/fa_associations_070117_l5.txt -f 50 > ./data/enrichment/yeast_wt_4.5.txt
python ./src/eval_yeast_associations.py ./data/clusters/yeast_dsd_5_wt.txt ./data/dsd/yeast/yeast_network_0_filtered_5.nodelist -a ./data/associations/fa_associations_070117_l5.txt -f 50 > ./data/enrichment/yeast_wt_5.txt
python ./src/eval_yeast_associations.py ./data/clusters/yeast_dsd_5.5_wt.txt ./data/dsd/yeast/yeast_network_0_filtered_5.5.nodelist -a ./data/associations/fa_associations_070117_l5.txt -f 50 > ./data/enrichment/yeast_wt_5.5.txt
python ./src/eval_yeast_associations.py ./data/clusters/yeast_dsd_6_wt.txt ./data/dsd/yeast/yeast_network_0_filtered_6.nodelist -a ./data/associations/fa_associations_070117_l5.txt -f 50 > ./data/enrichment/yeast_wt_6.txt

# modified walktrap
python ./src/eval_yeast_associations.py ./data/walktrap/p200_no_recursion_final_filtered.txt ./data/yeast_ppi.nodelist -a ./data/associations/fa_associations_070117_l5.txt -f 50 > ./data/enrichment/yeast_mod_wt_p200_ppi.txt
python ./src/eval_yeast_associations.py ./data/walktrap/dsd_4_p200_final_filtered.txt ./data/dsd/yeast/yeast_network_0_filtered_4.nodelist -a ./data/associations/fa_associations_070117_l5.txt -f 50 > ./data/enrichment/yeast_mod_wt_p200_4.txt
python ./src/eval_yeast_associations.py ./data/walktrap/dsd_4_5_p200_final_filtered.txt ./data/dsd/yeast/yeast_network_0_filtered_4.5.nodelist -a ./data/associations/fa_associations_070117_l5.txt -f 50 > ./data/enrichment/yeast_mod_wt_p200_4.5.txt
python ./src/eval_yeast_associations.py ./data/walktrap/dsd_5_p200_final_filtered.txt ./data/dsd/yeast/yeast_network_0_filtered_5.nodelist -a ./data/associations/fa_associations_070117_l5.txt -f 50 > ./data/enrichment/yeast_mod_wt_p200_5.txt
python ./src/eval_yeast_associations.py ./data/walktrap/dsd_5_5_p200_final_filtered.txt ./data/dsd/yeast/yeast_network_0_filtered_5.5.nodelist -a ./data/associations/fa_associations_070117_l5.txt -f 50 > ./data/enrichment/yeast_mod_wt_p200_5.5.txt
python ./src/eval_yeast_associations.py ./data/walktrap/dsd_6_p200_final_filtered.txt ./data/dsd/yeast/yeast_network_0_filtered_6.nodelist -a ./data/associations/fa_associations_070117_l5.txt -f 50 > ./data/enrichment/yeast_mod_wt_p200_6.txt
python ./src/eval_yeast_associations.py ./data/walktrap/p300_no_recursion_final_filtered.txt ./data/yeast_ppi.nodelist -a ./data/associations/fa_associations_070117_l5.txt -f 50 > ./data/enrichment/yeast_mod_wt_p300_ppi.txt
python ./src/eval_yeast_associations.py ./data/walktrap/dsd_4_p300_final_filtered.txt ./data/dsd/yeast/yeast_network_0_filtered_4.nodelist -a ./data/associations/fa_associations_070117_l5.txt -f 50 > ./data/enrichment/yeast_mod_wt_p300_4.txt
python ./src/eval_yeast_associations.py ./data/walktrap/dsd_4_5_p300_final_filtered.txt ./data/dsd/yeast/yeast_network_0_filtered_4.5.nodelist -a ./data/associations/fa_associations_070117_l5.txt -f 50 > ./data/enrichment/yeast_mod_wt_p300_4.5.txt
python ./src/eval_yeast_associations.py ./data/walktrap/dsd_5_p300_final_filtered.txt ./data/dsd/yeast/yeast_network_0_filtered_5.nodelist -a ./data/associations/fa_associations_070117_l5.txt -f 50 > ./data/enrichment/yeast_mod_wt_p300_5.txt
python ./src/eval_yeast_associations.py ./data/walktrap/dsd_5_5_p300_final_filtered.txt ./data/dsd/yeast/yeast_network_0_filtered_5.5.nodelist -a ./data/associations/fa_associations_070117_l5.txt -f 50 > ./data/enrichment/yeast_mod_wt_p300_5.5.txt
python ./src/eval_yeast_associations.py ./data/walktrap/dsd_6_p300_final_filtered.txt ./data/dsd/yeast/yeast_network_0_filtered_6.nodelist -a ./data/associations/fa_associations_070117_l5.txt -f 50 > ./data/enrichment/yeast_mod_wt_p300_6.txt

