#!/usr/bin/env python
# -*- coding: utf-8

__author__ = """Michael E. Rose (Michael.Ernst.Rose@gmail.com)"""

import unicodedata


# -------------------------------------------------------------------------
#
#  class DirtyString
#
# -------------------------------------------------------------------------
class DirtyString(object):
    __version__ = 0.12

    #
    #  METHODS
    #
    # -------------------------------------------------------------------------
    # standardize(aDirtyString)
    # -------------------------------------------------------------------------
    def standardize(self, a_dirty_string):
        """
        Removes interpunctuation and blanks from a string

        Args:
            a_dirty_string (str) -- the string to be cleaned

        Returns:
            a_clean_string (str) -- the string without interpunctuation

        Note:
            The use of normalize() is encouraged, as standardize() only removes
            unicode characters until ordinal number 128
        """

        # Remove extra whitespaces
        while "  " in a_dirty_string:
            a_dirty_string = a_dirty_string.replace("  ", " ")
        # replace _ with whitespace to keep syntactic structure of string
        a_dirty_string = a_dirty_string.replace("_", " ")

        # Remove ASCII Punctuation & Symbols
        # Note: we keep whitespaces because we want to keep the syntactic structure of the string
        a_cleaner_string = "".join(i for i in a_dirty_string if not 33 <= ord(i) <= 47)

        # Remove ASCII Punctuation & Symbols, part I
        a_cleaner_string = "".join(i for i in a_cleaner_string if not 58<=ord(i)<=64)

        # Remove ASCII Punctuation & Symbols, part II
        a_cleaner_string = "".join(i for i in a_cleaner_string if not 91<=ord(i)<=96)

        # Remove ASCII Punctuation & Symbols, part III
        a_clean_string = "".join(i for i in a_cleaner_string if not 123<=ord(i)<=126)

        # Change whitespace to underscore
        a_clean_string = a_clean_string.replace(" ", "_")

        return a_clean_string
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # normalize(a_dirty_string)
    # -------------------------------------------------------------------------
    def normalize(self, a_dirty_string):
        """
        Returns the normal form of a Unicode string (transliteration). Removes
        characters in case transliteration is not possible.

        Args:
            a_dirty_string (str) -- the string to be cleaned

        Returns:
            a_clean_string (str) -- the string without interpunctuation
        """
        # Replace by ASCII equivalent
        try:
            a_clean_string = ''.join(c for c in unicodedata.normalize('NFKD', unicode(a_dirty_string))
                                     if unicodedata.category(c) != 'Mn')

        # Remove if not possible
        except UnicodeDecodeError:
            a_clean_string = "".join(i for i in a_dirty_string if ord(i)<128)

        return a_clean_string
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # translit_nordic(ascii_string)
    # -------------------------------------------------------------------------
    def translit_nordic(self, ascii_string):
        """
        Replaces characters used in nordic languages. These characters are not
        in UTF-8 and will get lost when decoding. This is only meaningfull
        in python 2.

        Args:
            ascii_string (str) -- the string to be cleaned, ascii formatted

        Returns:
            a_clean_string (str) -- the string without replaced characters
        """
        
        if not isinstance(ascii_string, str):
            raise ValueError('Expects an ascii encoded string')

        a_cleaner_string = ascii_string.replace('\xc3\x98','O').replace('ø', 'o')
        a_cleaner_string = a_cleaner_string.replace('\xc3\x86','AE').replace('\xc3\xa6', 'ae')
        a_cleaner_string = a_cleaner_string.replace('\xc3\x90','D').replace('\xc3\xb0', 'd')
        a_cleaner_string = a_cleaner_string.replace('\xc3\x9e','TH').replace('\xc3\xbe', 'th')
        a_cleaner_string = a_cleaner_string.replace('\xc5\x92','OE').replace('\xc5\x93', 'oe')
        a_clean_string = a_cleaner_string.replace('\xc3\x9f','sz').replace('\xc6\x92', 'f')

        return a_clean_string
    # -------------------------------------------------------------------------
