#!/usr/bin/env python
# -*- coding: utf-8

__author__ = """Michael E. Rose (Michael.Ernst.Rose@gmail.com)"""


#-------------------------------------------------------------------------
#
#  stringtools.py is a collection of tools to manipulate strings
#
#-------------------------------------------------------------------------

if __name__ == '__main__':

#-------------------------------------------------------------------------
#
#  class DirtyString
#
#-------------------------------------------------------------------------
    class DirtyString(object):
        __version__ = 0.1

    #
    #  METHODS
    #

    #-------------------------------------------------------------------------
    # standardize(aDirtyString)
    #-------------------------------------------------------------------------
def standardize(aDirtyString):
        """
        Removes interpunctuation and blanks from a string

        Args:
            aDirtyString (str) -- the string to be cleaned

        Returns:
            aCleanString (str) -- the string without interpunctuation

        Note:
            The use of normalize() is encouraged, as standardize() only removes
            unicode characters until ordinal number 128
        """

        # Remove ASCII Punctuation & Symbols
        aCleanerString = "".join(i for i in aDirtyString if not 32<=ord(i)<=47)

        # Remove ASCII Punctuation & Symbols, part I
        aCleanerString = "".join(i for i in aCleanerString if not 58<=ord(i)<=64)

        # Remove ASCII Punctuation & Symbols, part II
        aCleanerString = "".join(i for i in aCleanerString if not 91<=ord(i)<=96)

        # Remove ASCII Punctuation & Symbols, part III
        aCleanString = "".join(i for i in aCleanerString if not 123<=ord(i)<=126)

        return aCleanString
    #-------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    # normalize(aDirtyString)
    #-------------------------------------------------------------------------
def normalize(aDirtyString):
        """
        Returns the normal form of a Unicode string (transliteration). Removes
        characters in case transliteration is not possible.

        Args:
            aDirtyString (str) -- the string to be cleaned

        Returns:
            aCleanString (str) -- the string without interpunctuation
        """

        import unicodedata

        # Replace by ASCII equivalent
        try:
            aCleanString = ''.join(c for c in unicodedata.normalize('NFKD', unicode(aDirtyString))
                            if unicodedata.category(c) != 'Mn')

        # Remove if not possible
        except UnicodeDecodeError:
            aCleanString = "".join(i for i in aDirtyString if ord(i)<128)

        return aCleanString
    #-------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    # translit_nordic(aDirtyString)
    #-------------------------------------------------------------------------
def translit_nordic(aDirtyString):
        """
        Replaces characters used in nordic languages not covered by normalize()

        Args:
            aDirtyString (str) -- the string to be cleaned

        Returns:
            aCleanString (str) -- the string without interpunctuation
        """
        # Some characters are out of range
        aCleanerString = aDirtyString.replace("Ø","O").replace("ø", "o")
        aCleanerString = aCleanerString.replace("Æ","AE").replace("æ", "ae")
        aCleanerString = aCleanerString.replace("Ð","D").replace("ð", "d")
        aCleanerString = aCleanerString.replace("Þ","TH").replace("þ", "th")
        aCleanerString = aCleanerString.replace("Œ","OE").replace("œ", "oe")
        aCleanString = aCleanerString.replace("ß","sz").replace("ƒ", "f")

        return aCleanString
    #-------------------------------------------------------------------------