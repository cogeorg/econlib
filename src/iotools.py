#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = """Michael E. Rose (Michael.Ernst.Rose@gmail.com)"""


#-------------------------------------------------------------------------
#
#  iotools.py is a collection of tools for input and outputting data
#
#-------------------------------------------------------------------------


#-------------------------------------------------------------------------
# getDialect(aFile)
#-------------------------------------------------------------------------
def getDialect(aFile):

    return csv.Sniffer().sniff(aFile.readline())
#-------------------------------------------------------------------------

#
#  METHODS
#

#-------------------------------------------------------------------------
# csv_to_dict(
#    filename,
#    key_func,
#    value_func,
#    skip_header
#    )
#-------------------------------------------------------------------------
def csv_to_dict(filename,
                key_func,
                value_func,
                skip_header = True):
        """
        Reads a csv as a dictionary, where values and keys are set in a flexible manner. Delimiters are determined automatically.

        Args:
            filename (str) -- the name of the source file
            key_func (func) -- a function specifying which row(s) of the csv file should be the keys of the dictionary
            value_func (func) -- a function specifiying which row(s) of the csv file should be the values of the dictionary
            skip_header (boolean - optional) -- set to False if header should not be skipped

        Returns:
            aDict (dict) -- the dictionary compiled from the csv file

        """

        import csv

        aDict = {}
        with open(filename, 'r') as f:
            csvDialect = getDialect(f)
            f.seek(0)
            csvReader = csv.reader(f, dialect=csvDialect)
            if skip_header:
                next(csvReader, None)
            for row in csvReader:
                key = key_func(row)
                aDict[key] = value_func(row)

        return aDict
#-------------------------------------------------------------------------


#-------------------------------------------------------------------------
# csv_to_nested_dict(
#    filename,
#    key_func,
#    skip_header
#    )
#-------------------------------------------------------------------------
def csv_to_nested_dict(filename,
                       key_func,
                       ordered = False):
        """
        Reads a csv as a dictionary of dictionaries, where keys are set in a flexible manner. Delimiters are determined automatically.

        Args:
            filename (str) -- the name of the source file
            key_func (func) -- a function specifying which row(s) of the csv file should be the keys of the dictionary
            ordered (boolean - optional) -- set to True if entire dictionary shall be ordered

        Returns:
            aDict (dict) -- the nested dictionary compiled from the csv file

        """

        import csv

        if ordered:
            from collections import OrderedDict
            aDict = OrderedDict()
            with open(filename, 'rb') as f:
                csvDialect = getDialect(f)
                f.seek(0)
                csvReader = csv.reader(f, dialect=csvDialect)
                fields = next(csvReader)
                for row in csvReader:
                    temp = OrderedDict(zip(fields, row))
                    key = key_func(temp)
                    aDict[key] = temp

        else:
            aDict = {}
            with open(filename, 'rb') as f:
                csvDialect = getDialect(f)
                f.seek(0)
                csvReader = csv.DictReader(f, dialect=csvDialect)
                for row in csvReader:
                    key = key_func(row)
                    aDict[key] = row

        return aDict
#-------------------------------------------------------------------------


#-------------------------------------------------------------------------
# nested_dict_to_csv(
#    nested_dict,
#    file_name,
#    fields
#    )
#-------------------------------------------------------------------------
def nested_dict_to_csv(nested_dict,file_name,fields='',header=True):
        """
        Printes a nested dictionary to csv.

        Args:
            nested_dict (dict) -- a dictionary of dictionaries
            file_name (str) -- the name of output file
            fields (list of str) -- the ordering of subkeys with the first entry being the main key
            header (boolean - optional) -- set to False if header should not be written
        """
        import csv
        with open(file_name,'w') as f:
            w = csv.DictWriter(f, fieldnames=fields)
            if header:
                w.writeheader()
            for k in nested_dict:
                w.csvWriter({field: out_dict[k].get(field) or k for field in fields})
#-------------------------------------------------------------------------
