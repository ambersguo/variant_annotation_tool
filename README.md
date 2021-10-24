# Variant Annotation Tool

Shuang (Amber) Guo, 10-24-2021
Contact: shuangguo831@gmail.com

This tool include following files in same folder:
- README
- shell script: 0_variant_annotation_tool.sh
- python script 1: 1_vcf_filter.py
- python script 2: 2_fetch_dbSnp_terms.py
- python script 3: 3_fetch_SO_terms.py
- python script 4: 4_fetch_ExAc_API.py
- reference file 1: dbSnp153Common.bed (not included in this repository)
- reference file 2: so.obo (not included in this repository)
- input file: Challenge_data.vcf (not included in this repository)

System Dependencies:
- python version 3.6 or higher
- python packages: time, re, string, pandas, json, requests

To run this tool, please following steps as below:
Step 1: make sure the input vcf file is in the same folder with the rest of the scripts and references.
Step 2: make sure the internet connection is stable, which is required for vising REST APIs.
Step 2: open a terminal window, set up the folder as present working directory.
Step 3: type this command: bash 0_variant_annotation_tool.sh
