#! /bin/bash

python3 1_vcf_filter.py
python3 2_fetch_dbSnp_terms.py
python3 3_fetch_SO_terms.py
python3 4_fetch_ExAc_API.py
