#!/usr/bin/env python3
# -*- coding: utf-8 -*-

######################################################################################################################
#
# Variant Annotation Tool: 3_fetch_SO_terms.py
# Shuang (Amber) Guo, 10-24-2021
#
# Functions of this script include:
# 1. Fetch terms of interests in SO (Sequence Ontology) database based on SO id.
#    Terms of interests include: name of max impact function, description of max impact function.
#    SO database used in this script is: so.obo
#    SO database was downloaded from: https://github.com/The-Sequence-Ontology/SO-Ontologies/tree/master/Ontology_Files
#    Alternative references for SO databases can be used instead of so.obo if needed.
# 2. Append terms of interested fetched from so.obo to file.
#
######################################################################################################################

import time
import re
import string

time_start = time.time()
print('SO indexing...')

# make a dictionary with key as SO id, and value as SO name and SO description
with open('so.obo', 'r') as ref:
    id2info = {}
    line_count = 0
    for linein in ref:
        linein = linein.rstrip('\n')
        if linein.startswith('id: SO:'):
            SO_id = int(linein.replace('id: SO:',''))
            line_count = 1
        elif linein.startswith('name: ') and line_count == 1:    # make sure SO name is in the same block as id
            SO_name = (linein.replace('name: ',''))
            SO_info = SO_name + '\tnone'
            id2info[SO_id] = SO_info
            line_count += 1
        elif linein.startswith('def: ') and line_count == 2:    # make sure SO def is in the same block as id
            SO_def = (linein.replace('def: ',''))
            SO_info = SO_name + '\t' + SO_def
            id2info[SO_id] = SO_info
            line_count += 1
        elif linein.startswith('[Term]'):
            line_count += 1

print('fetching SO terms...')
with open('data_vcf_filtered_dbSnp153Common.txt', 'r') as file2in:
    newlines = []
    header = file2in.readline()
    header = header.rstrip('\n')
    for linein in file2in:
        linein = linein.rstrip('\n')
        eles = re.split(r'\t', linein)
        SO_id = eles[-1]
        if SO_id.isdigit():    # if SO id is available for the variant
            SO_id = int(SO_id)
            SO_info = id2info[SO_id]
        else:
            SO_info = 'n/a\tn/a'    # if SO id is not available for the variant
        newline = linein + '\t' + SO_info
        newlines.append(newline)

print('appending SO terms...')
with open('data_vcf_filtered_dbSnp153Common_SOterms.txt', 'w') as file2out:
    file2out.write(header + '\tmax_impact_function_SO_name\tmax_impact_function_SO_description\n')
    for newline in newlines:
        file2out.write(newline + '\n')
        
time_end = time.time()
run_time = '{:.2f}'.format(time_end - time_start)
print('SO terms appending completed!\n')

with open('log.txt', 'a') as file2log:
    file2log.write('Sequence Ontology terms appending run time: {}s ... Done\n\n'.format(run_time))
