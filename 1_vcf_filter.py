#!/usr/bin/env python3
# -*- coding: utf-8 -*-

######################################################################################################################
#
# Variant Annotation Tool: 1_vcf_filter.py
# Shuang (Amber) Guo, 10-24-2021
#
# Functions of this script include:
# 1. Filter the input vcf file based on quality, variant frequency in samples and read depth.
# 2. Format the input vcf file to only include terms needed.
# 3. Record numbers of variants pre filtering and post filtering in log file.
#
######################################################################################################################

import time
import re

time_start = time.time()
print('vcf filtering...')

with open('data.vcf', 'r') as file2in:
    newlines = []
    total = total_pass = total_variants = 0
    for linein in file2in:
        if not linein.startswith('#'):
            total += 1
            linein = linein.rstrip('\n')
            eles = re.split(r'\t', linein)
            chrom = eles[0]
            loci = eles[1]
            ref = eles[3]
            alt = eles[4]
            qual = eles[5]
            infos = eles[7]
            info_eles = re.split(r';', infos)
            
            # only saving terms of interests in output file
            # terms of interests include: sample number, alteration allele count,
            # read depth, read count of alteration, read count of reference,
            # allele frequency, CIGAR (optional), alteration type
            
            for info_ele in info_eles:
                if 'NS=' in info_ele:
                    sample_number = info_ele.replace('NS=', '')
                elif 'AC=' in info_ele:
                    alt_allele_count = info_ele.replace('AC=', '')
                elif 'DP=' in info_ele:
                    read_depth = info_ele.replace('DP=', '')
                elif 'AO=' in info_ele and 'PAO=' not in info_ele:
                    read_count_alt = info_ele.replace('AO=', '')
                elif 'RO=' in info_ele and 'PRO=' not in info_ele:
                    read_count_ref = info_ele.replace('RO=', '')
                elif 'AF=' in info_ele and 'SAF=' not in info_ele:
                    allele_freq = info_ele.replace('AF=', '')
                elif 'CIGAR=' in info_ele:
                    cigar = info_ele.replace('CIGAR=', '')                
                elif 'TYPE=' in info_ele:
                    alt_type = info_ele.replace('TYPE=','')
            
            # filter out records with quality value less than 10, 
            # filter out records with variant identified in more than 1 sample,
            # filter out records with total read depth less than 3.
            # filter out records with alteration allele count less than 3.
            
            if float(qual) > 10 and int(sample_number) > 1 and int(read_depth) > 3:
                if ',' in alt:    # if multiple variants are called for one reference
                    mark = 'multiple_variant'
                    alt_eles = re.split(r',', alt)
                    alt_allele_count_eles = re.split(r',', alt_allele_count)
                    read_count_alt_eles = re.split(r',', read_count_alt)
                    allele_freq_eles = re.split(r',', allele_freq)
                    cigar_eles = re.split(r',', cigar)
                    alt_type_eles = re.split(r',', alt_type)
                    for i in range(len(alt_eles)):    # loop through each variant
                        if int(alt_allele_count_eles[i]) > 3:
                            read_count_alt_ratio = '{:.2f}'.format((int(read_count_alt_eles[i])/int(read_depth))*100)
                            read_count_ref_ratio = '{:.2f}'.format((int(read_count_ref)/int(read_depth))*100)
                            newline = chrom+'\t'+loci+'\t'+ref+'\t'+alt_eles[i]+'\t'+alt_type_eles[i]+'\t'+read_depth+'\t'+read_count_alt_eles[i]+'\t'+read_count_ref+'\t'+read_count_alt_ratio+'\t'+read_count_ref_ratio+'\t'+allele_freq_eles[i]+'\t'+cigar_eles[i]+'\t'+mark
                            newlines.append(newline)
                            total_variants += 1
                            if i == 0:
                                total_pass += 1
                else:    # if single variant is called for one reference
                    mark = 'single_variant'
                    if int(alt_allele_count) > 3:
                        read_count_alt_ratio = '{:.2f}'.format((int(read_count_alt)/int(read_depth))*100)
                        read_count_ref_ratio = '{:.2f}'.format((int(read_count_ref)/int(read_depth))*100)
                        newline = chrom+'\t'+loci+'\t'+ref+'\t'+alt+'\t'+alt_type+'\t'+read_depth+'\t'+read_count_alt+'\t'+read_count_ref+'\t'+read_count_alt_ratio+'\t'+read_count_ref_ratio+'\t'+allele_freq+'\t'+cigar+'\t'+mark
                        newlines.append(newline)
                        total_variants += 1
                        total_pass += 1

with open('data_vcf_filtered.txt', 'w') as file2out:
    file2out.write('chr\tposition\treference\tvariant\tvariant_type\ttotal_read_depth\tvariant_read_count\treference_read_count\tvariant_read_count_percentage\treference_read_count_percentage\tallele_frequency\tCIGAR\n')
    for newline in newlines:
        file2out.write(newline + '\n')
      
time_end = time.time()
run_time = '{:.2f}'.format(time_end - time_start)
print('vcf filtering completed!\n')

with open('log.txt', 'a') as file2log:
    file2log.write('pre vcf filter without listing multiple variants: {}\n'.format(total))
    file2log.write('post vcf filter without listing multiple variants: {}\n'.format(total_pass))
    file2log.write('post vcf filter with listing multiple variants: {}\n'.format(total_variants))
    file2log.write('vcf filtering run time: {}s ... Done\n\n'.format(run_time))
