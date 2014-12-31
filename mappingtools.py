#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = """Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

import sys
import logging
import re
from fuzzywuzzy import process
from fuzzywuzzy import fuzz


#-------------------------------------------------------------------------
#
#  class Mapping
#
#-------------------------------------------------------------------------
class Mapping(object):
    __version__ = 0.9


    #
    # VARIABLES
    #
    identifier = ""
    from_strings = []  # contains the raw from_strings
    reduced_from_strings = {}  # contains the reduced from_strings with unique entries and relative frequencies

    # NOTE: this variable is not always needed, e.g. when there is only one input file but with multiple
    #       occurences of certain strings. in this case the mapping is not between files, but from the various
    #       forms a given string is written to it's unique (correct) form
    to_string_array = []  # contains the raw to_strings
    to_string_dict = {}  # contains the reduced to_strings with unique entries and relative frequencies


    #
    #  METHODS
    #
    #-------------------------------------------------------------------------
    #  __init__
    #-------------------------------------------------------------------------
    def __init__(self):
        pass
    #-------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    # standardize_string(
    #   string,
    #   redundant_strings_file_name
    #   )
    #-------------------------------------------------------------------------
    def standardize_string(self,
                           original_string,
                           redundant_strings_file_name
    ):
        """
        Takes an original string and standardizes it by stripping special characters and redundant strings

        Args:
            original_string (str) -- string to be standardized
            redundant_strings_file_name (str) -- the file where redundant strings (one per line) are listed

        Returns:
            standardized_string (str) -- standardized string without special characters and redundant strings

        Note:
        - The redundant_strings_file contains strings that can be stripped from the strings that are being parsed.
          Examples: 'the', 'of'
        - Each string in the redundant_strings_file is in a single line
        - The uppercase version of each redundant string is also automatically removed

        """

        # all in upper case letters
        original_string = original_string.upper().strip()

        # special characters should be removed from all strings
        special_characters = [' ', '/', ',', '\'', '“', '”', '\?', '\.', '\"', '-']
        for special_character in special_characters:
            original_string = re.sub(special_character, '', original_string)

        # redundant strings are things like 'the', 'of', etc. that can be
        # stripped because they complicate the matching without carrying too
        # too much semantic meaning
        redundant_strings = []

        # read redundant strings from file.
        redundant_strings_file = open(redundant_strings_file_name, 'r')
        for line in redundant_strings_file.readlines():
            redundant_strings.append(line.strip())
            # we also remove the upper case version of each string
            redundant_strings.append(line.strip().upper())
        redundant_strings_file.close()

        # actually remove redundant strings
        for redundant_string in redundant_strings:
            original_string = re.sub(redundant_string, '', original_string)

        return original_string
    #-------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    # compute_string_frequency(
    #   string_array,
    #   )
    #-------------------------------------------------------------------------
    def compute_string_frequency(self,
                                 string_array
    ):
        """
        Computes the absolute frequency of every string in a string_array

        Args:
            string_array (list) -- array containing strings, possibly more than once

        Returns:
            reduced_string_dict (dict) -- dict containing unique string as key and frequency as value

        Note:
            Absolute frequency is the number of occurences of a unique string

        """

        reduced_string_dict = {}

        for entry in string_array:
            if entry in reduced_string_dict:
                reduced_string_dict[entry] += 1
            else:
                reduced_string_dict[entry] = 1

        return reduced_string_dict
    #-------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    # find_best_match(
    #   matching_string,
    #   original_strings,
    #   number_of_fuzzy_options,
    #   threshold_fuzziness
    #   )
    #-------------------------------------------------------------------------
    def find_best_match(self,
                        matching_string,
                        original_strings,
                        number_of_fuzzy_options,
                        threshold_fuzziness,
                        debug=None
    ):
        """
        Finds the best match of a string in an array of strings

        Args:
            matching_string (str) -- the string that is to be matched
            original_strings (list) -- the list of strings from which the best match is to be found
            number_of_fuzzy_options (int) -- the number of alternatives of the matching_string fuzzywuzzy should find in the original_strings
            threshold_fuzziness (int) -- the lower threshold for the precision of fuzzy matches

        Returns:
            best_match (str) -- the best match to matching_string in original_strings

        Note:


        """

        # the possible matches are the original_strings array reduced by the
        # string we are trying to match
        reduced_original_strings = list(original_strings)
        reduced_original_strings.remove(matching_string)

        # find fuzzy matches in the reduced list of all entries
        matching_options = process.extract(
            matching_string,
            reduced_original_strings,
            limit=number_of_fuzzy_options
        )

        # we start with the original string
        original_frequency = original_strings[matching_string]
        best_match_precision = 0.0  # original string is not in the reduced list of all entries
        best_match = matching_string

        # the best matching option is found by checking fuzziness and relative frequency of all matches
        for matching_option in matching_options:
            match_fuzziness = matching_option[1]
            match_frequency = original_strings[matching_option[0]]

            # we replace a name with a similar name only if the similar name
            # has a higher frequency; we also check that we only consider
            # reasonable matches, otherwise we might match with a fairly
            # different, but very prominent name
            matching_precision = match_fuzziness/100.0*match_frequency - original_frequency

            # finally, do the comparison by finding best match and checking that fuzziness is above some threshold
            if matching_precision > best_match_precision and match_fuzziness > threshold_fuzziness:
                best_match_precision = matching_precision
                best_match = matching_option[0]

            if debug:  # debug
                print matching_string + "[" + str(original_frequency) + "] vs.", matching_option, "-->", best_match, best_match_precision

        return best_match
    #-------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    # find_best_match_tuple(
    #   matching_string,
    #   original_strings,
    #   number_of_fuzzy_options,
    #   threshold_fuzziness
    #   )
    #-------------------------------------------------------------------------
    def find_best_match_tuple(self,
                        matching_tuple,
                        original_tuples,
                        number_of_fuzzy_options,
                        threshold_fuzziness,
                        debug=None
    ):
        """
        Finds the best match of a string tuple in an array of string tuples

        Args:
            matching_string (str) -- the string that is to be matched
            original_strings (list) -- the list of strings from which the best match is to be found
            number_of_fuzzy_options (int) -- the number of alternatives of the matching_string fuzzywuzzy should find in the original_strings
            threshold_fuzziness (int) -- the lower threshold for the precision of fuzzy matches

        Returns:
            best_match (str) -- the best match to matching_string in original_strings

        Note:


        """

        # the possible matches are the original_strings array reduced by the
        # string we are trying to match
        reduced_original_strings = list(original_strings)
        reduced_original_strings.remove(matching_string)

        # find fuzzy matches in the reduced list of all entries
        matching_options = process.extract(
            matching_string,
            reduced_original_strings,
            limit=number_of_fuzzy_options
        )

        # we start with the original string
        original_frequency = original_strings[matching_string]
        best_match_precision = 0.0  # original string is not in the reduced list of all entries
        best_match = matching_string

        # the best matching option is found by checking fuzziness and relative frequency of all matches
        for matching_option in matching_options:
            match_fuzziness = matching_option[1]
            match_frequency = original_strings[matching_option[0]]

            # we replace a name with a similar name only if the similar name
            # has a higher frequency; we also check that we only consider
            # reasonable matches, otherwise we might match with a fairly
            # different, but very prominent name
            matching_precision = match_fuzziness/100.0*match_frequency - original_frequency

            # finally, do the comparison by finding best match and checking that fuzziness is above some threshold
            if matching_precision > best_match_precision and match_fuzziness > threshold_fuzziness:
                best_match_precision = matching_precision
                best_match = matching_option[0]

            if debug:  # debug
                print matching_string, original_frequency, best_match, best_match_precision

        return best_match
    #-------------------------------------------------------------------------
