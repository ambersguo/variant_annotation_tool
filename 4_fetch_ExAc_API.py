#!/usr/bin/env python3
# -*- coding: utf-8 -*-

######################################################################################################################
#
# Variant Annotation Tool: 4_fetch_ExAc_API.py
# Shuang (Amber) Guo, 10-24-2021
#
# Functions of this script include:
# 1. Prepare ExAc API bulk query in correct format according to: http://exac.hms.harvard.edu/
# 2. Fetch ExAC API metadata according to: https://github.com/hms-dbmi/exac_browser
#    API url used to combine with bulk query in json: 'http://exac.hms.harvard.edu/rest/bulk/variant/variant'
#    Alternative url can be used instead of ...variant/variant if needed.
# 3. Fetch allele frequency from ExAc API metadata and append to file.
# 4. Generate final reports in both txt and csv formats.
#
######################################################################################################################

import time
import json
import requests
import re
import string
import pandas as pd

time_start = time.time()
print('preparing ExAc API bulk query...')

# prepare ExAc API bulk query
with open('Challenge_data_vcf_filtered_dbSnp153Common_SOterms.txt', 'r') as file2in:
    lines = []
    api_input = []
    alt2line = {}
    header = file2in.readline()
    header = header.rstrip('\n')
    for linein in file2in:
        linein = linein.rstrip('\n')
        lines.append(linein)
        eles = re.split(r'\t', linein)
        alt = eles[0] + '-' + eles[1] + '-' + eles[2] + '-' + eles[3]
        if eles[0].isdigit():
            api_input.append(alt)

# fetch ExAc metainfo using query in json format
# make a dictionary with key as variant and value as ExAc allele frequency
print('fetching ExAc allele frequency from REST API...')
api_json = json.dumps(api_input)
api_url = 'http://exac.hms.harvard.edu/rest/bulk/variant/variant'
api_req = requests.post(api_url, data = api_json)
api_output = api_req.text
api_dict = json.loads(api_output)
alt2freq = {}
for alt, alt_info in api_dict.items():
    for info_name, info_detail in alt_info.items():
        if info_name == 'allele_freq':
            alt2freq[alt] = '{:.2f}'.format(info_detail)
            next

print('appending ExAc allele frequency...')
newlines = []
with open('Challenge_data_vcf_filtered_dbSnp153Common_SOterms_ExACfreq.txt', 'w') as file2out:
    header = header + '\tExAC_allele_frequency'
    file2out.write(header + '\n')
    header = header.replace('\t',',')
    newlines.append(header)
    for linein in lines:
        eles = re.split(r'\t', linein)
        alt = eles[0] + '-' + eles[1] + '-' + eles[2] + '-' + eles[3]
        if alt in alt2freq:
            freq = str(alt2freq[alt])
        else:
            freq = 'n/a'
        newline = linein + '\t' + freq
        file2out.write(newline + '\n')
        newline = newline.replace(',',';')
        newline = newline.replace('\t',',')
        newlines.append(newline)

with open('Challenge_data_vcf_filtered_dbSnp153Common_SOterms_ExACfreq.csv', 'w') as csv2out:
    df = pd.DataFrame([newline.split(',') for newline in newlines])
    df.to_csv(csv2out, header=False, index=False, sep=',')

time_end = time.time()
run_time = '{:.2f}'.format(time_end - time_start)
print('final report generating completed!\n')

with open('log.txt', 'a') as file2log:
    file2log.write('ExAC appending and final report generating run time: {}s ... Done\n\n'.format(run_time))
