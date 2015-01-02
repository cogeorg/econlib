#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = """Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

#-------------------------------------------------------------------------
#
#  conftools.py is a simple module to manage .xml configuration files
#
#-------------------------------------------------------------------------
if __name__ == '__main__':

#
# VARIABLES
#
    import sys

    from mappingtools import Mapping

    args = sys.argv

    # we have multiple tests here, the first argument specifies which test
    # to run
    test_number = args[1]

    #
    # TEST 1: standardize_string
    #
    if test_number == "1":
        input_string = args[2]
        redundant_strings_file_name = args[3]

        mapping = Mapping()

        standardized_string = mapping.standardize_string(input_string, redundant_strings_file_name)

        print "MappingTools version: " + str(mapping.__version__)
        print input_string + "  -->  " + standardized_string


    #
    # TEST 2: string frequency
    #
    if test_number == "2":
        input_file_name = args[2]

        mapping = Mapping()

        input_file = open(input_file_name, 'r')
        # for simplicity every line is a distinct string, but the string array
        # can really come from anywhere
        for line in input_file.readlines():
            mapping.from_strings.append(line.strip())

        mapping.reduced_from_strings = mapping.compute_string_frequency(mapping.from_strings)

        print "MappingTools version: " + str(mapping.__version__)
        print mapping.from_strings
        print mapping.reduced_from_strings


    #
    # TEST 3: find best match
    #
    if test_number == "3":
        input_file_name = args[2]

        mapping = Mapping()

        # first create a reduced string dictionary
        input_file = open(input_file_name, 'r')
        # for simplicity every line is a distinct string, but the string array
        # can really come from anywhere
        for line in input_file.readlines():
            mapping.from_strings.append(line.strip())

        mapping.reduced_from_strings = mapping.compute_string_frequency(mapping.from_strings)

        print "MappingTools version: " + str(mapping.__version__)

        print "<< RUN1: "
        number_of_fuzzy_options = 4
        threshold_fuzziness = 80
        print "number_of_fuzzy_options: " + str(number_of_fuzzy_options)
        print "threshold_fuzziness: " + str(threshold_fuzziness)

        for matching_string in mapping.reduced_from_strings:
            best_match = mapping.find_best_match(matching_string,
                                                 mapping.reduced_from_strings,
                                                 number_of_fuzzy_options,
                                                 threshold_fuzziness,
                                                 False
            )
            print matching_string + " --> " + best_match

        print "<< RUN2: "
        number_of_fuzzy_options = 4
        threshold_fuzziness = 70
        print "number_of_fuzzy_options: " + str(number_of_fuzzy_options)
        print "threshold_fuzziness: " + str(threshold_fuzziness)

        for matching_string in mapping.reduced_from_strings:
            best_match = mapping.find_best_match(matching_string,
                                                 mapping.reduced_from_strings,
                                                 number_of_fuzzy_options,
                                                 threshold_fuzziness,
                                                 False
            )
            print matching_string + " --> " + best_match


    #
    # TEST 4: find matching tuple
    #
    if test_number == "4":
        input_file_name = args[2]

        mapping = Mapping()

        # first create a reduced string dictionary
        input_file = open(input_file_name, 'r')
        # for simplicity every line is a distinct string, but the string array
        # can really come from anywhere
        for line in input_file.readlines():
            mapping.from_strings.append(tuple(line.strip().split(";")))  #  append tokens to string list

        mapping.reduced_from_strings = mapping.compute_string_frequency(mapping.from_strings)

        print "MappingTools version: " + str(mapping.__version__)

        print "<< RUN1: "
        threshold_fuzziness = 80.0
        matching_scaling_factor = 50.0
        print "threshold_fuzziness: " + str(threshold_fuzziness)
        print "matching_scaling_factor" + str(matching_scaling_factor)

        print "reduced tuples: ", mapping.reduced_from_strings
        for matching_tuple in mapping.reduced_from_strings:
            [best_match, best_distance] = mapping.find_best_match_tuple(
                matching_tuple,
                mapping.reduced_from_strings,  # TODO not a good name as it can also contain tuples
                threshold_fuzziness,
                matching_scaling_factor,
                True
            )

            print matching_tuple, " -->", best_match, "with best_distance:", best_distance
