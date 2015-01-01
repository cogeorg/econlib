#!/bin/bash

# standardize string
./test_mappingtools.py 1 footeststringbar samples/mappingtools/redundant_strings.csv

# best matches
./test_mappingtools.py 3 samples/mappingtools/best_match_sample_file.csv
./test_mappingtools.py 4 samples/mappingtools/best_tuple_match_sample_file.csv
