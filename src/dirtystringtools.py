#-*- coding: utf-8 -*-
"""
================
dirtystringtools
================

A collection of methods for cleaning strings
"""
import unicodedata
__author__  =  """Michael E. Rose (Michael.Ernst.Rose@gmail.com)"""
__all__ = ['standardize', 'normalize', 'translit_nordic']
__version__ = 0.13


def standardize(ds):
    """
    Removes interpunctuation and blanks from a string.

    Parameters
    ----------
    ds: the string to be cleaned

    Returns
    -------
    a string without interpunctuation

    Note
    ----
    The use of normalize() is encouraged, as standardize() only removes
    characters until ordinal number 128.
    """
    while "  " in ds:
        ds = ds.replace("  ", " ")
    ds = "".join(i for i in ds if not 32<=ord(i)<=47)
    ds = "".join(i for i in ds if not 58<=ord(i)<=64)
    ds = "".join(i for i in ds if not 91<=ord(i)<=96)
    return "".join(i for i in ds if not 123<=ord(i)<=126)

def normalize(a_dirty_string):
    """
    Returns the normal form of a Unicode string (transliteration). Removes
    characters in case transliteration is not possible.

    Args:
        a_dirty_string (str) -- the string to be cleaned

    Returns:
        a_clean_string (str) -- the string without interpunctuation
    """
    try: # Replace by ASCII equivalent
        a_clean_string = ''.join(c for c in unicodedata.normalize('NFKD', unicode(a_dirty_string))
                                 if unicodedata.category(c) != 'Mn')
    except UnicodeDecodeError: # Remove if not possible
        a_clean_string = "".join(i for i in a_dirty_string if ord(i)<128)
    return a_clean_string


def translit_nordic(ascii_string):
    """
    Replaces characters used in nordic languages. These characters are not
    in UTF-8 and will get lost when decoding. This is only meaningfull
    in python 2.

    Parameters
    ascii_string: the string to be cleaned, ascii formatted (str)

    Returns
    -------
    a_clean_string: the string without replaced characters (str)
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
