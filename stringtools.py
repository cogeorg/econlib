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
    __version__ = 0.11

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

        # Remove ASCII Punctuation & Symbols
        a_cleaner_string = "".join(i for i in a_dirty_string if not 32<=ord(i)<=47)

        # Remove ASCII Punctuation & Symbols, part I
        a_cleaner_string = "".join(i for i in a_cleaner_string if not 58<=ord(i)<=64)

        # Remove ASCII Punctuation & Symbols, part II
        a_cleaner_string = "".join(i for i in a_cleaner_string if not 91<=ord(i)<=96)

        # Remove ASCII Punctuation & Symbols, part III
        a_clean_string = "".join(i for i in a_cleaner_string if not 123<=ord(i)<=126)

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
<<<<<<< HEAD
            a_clean_string = "".join(i for i in a_dirty_string if ord(i)<128)
=======
            aCleanString = "".join(i if ord(i)<128 else ' ' for i in aDirtyString)

        return aCleanString
    #-------------------------------------------------------------------------
>>>>>>> a5db3672665dcb7f75625102f3c67470052f2866

        return a_clean_string
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # translit_nordic(a_dirty_string)
    # -------------------------------------------------------------------------
    def translit_nordic(self, a_dirty_string):
        """
        Replaces characters used in nordic languages not covered by normalize()

        Args:
            a_dirty_string (str) -- the string to be cleaned

        Returns:
            a_clean_string (str) -- the string without interpunctuation
        """
        # Some characters are out of range
<<<<<<< HEAD
        a_cleaner_string = a_dirty_string.replace("Ø","O").replace("ø", "o")
        a_cleaner_string = a_cleaner_string.replace("Æ","AE").replace("æ", "ae")
        a_cleaner_string = a_cleaner_string.replace("Ð","D").replace("ð", "d")
        a_cleaner_string = a_cleaner_string.replace("Þ","TH").replace("þ", "th")
        a_cleaner_string = a_cleaner_string.replace("Œ","OE").replace("œ", "oe")
        a_clean_string = a_cleaner_string.replace("ß","sz").replace("ƒ", "f")

        return a_clean_string
    # -------------------------------------------------------------------------
=======
        aCleanerString = aDirtyString.replace("Ø","O").replace("ø", "o")
        aCleanerString = aCleanerString.replace("Æ","AE").replace("æ", "ae")
        aCleanerString = aCleanerString.replace("Ð","D").replace("ð", "d")
        aCleanerString = aCleanerString.replace("Þ","TH").replace("þ", "th")
        aCleanerString = aCleanerString.replace("Œ","OE").replace("œ", "oe")
        aCleanString = aCleanerString.replace("ß","sz").replace("ƒ", "f")

        return aCleanString
    #-------------------------------------------------------------------------
>>>>>>> a5db3672665dcb7f75625102f3c67470052f2866
