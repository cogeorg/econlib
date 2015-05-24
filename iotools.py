#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = """Michael E. Rose (Michael.Ernst.Rose@gmail.com)"""

#-------------------------------------------------------------------------
#
#  iotools.py is a collection of tools for input and outputting data
#
#-------------------------------------------------------------------------
if __name__ == '__main__':

#
# VARIABLES
#

    import csv

#-------------------------------------------------------------------------
#
#  class io
#
#-------------------------------------------------------------------------
class io(object):
    __version__ = 0.2

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
            csvDialect = csv.Sniffer().sniff(f.read(4096))
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
                csvDialect = csv.Sniffer().sniff(f.read(4096))
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
                csvDialect = csv.Sniffer().sniff(f.read(4096))
                f.seek(0)
                csvReader = csv.DictReader(f, dialect=csvDialect)
                for row in csvReader:
                    key = key_func(row)
                    aDict[key] = row

        return aDict
    #-------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    # nested_dict_to_csv(
    #    aNestedDict,
    #    FileName,
    #    FirstFieldName
    #    )
    #-------------------------------------------------------------------------
def nested_dict_to_csv(aNestedDict,
                       FileName,
                       FirstFieldName = "",
                       write_header = True):
        """
        Takes an dictionary of dictionaries and outputs it as csv with keys as rownames and subkeys as column names

        Args:
            aNestedDict (dict) -- a dictionary of dictionaries
            FileName (str) -- the name of target file
            FirstFieldName (str - optional) -- the name of the first column (ie the name for the keys - if none is given,
                                               the field is empty)
            write_header (boolean - optional) -- set to False if header should not be written

        """

        import csv

        # get unique names of all subkeys
        SubKeys = list({subkey for key in aNestedDict.values() for subkey in key})

        # create proper list of field names
        
        FieldNames = [FirstFieldName]
        FieldNames.extend(SubKeys)
        # output using csv
        with open(FileName, 'wb') as f:
            csvWriter = csv.DictWriter(f, fieldnames=FieldNames, lineterminator='\n')
            if write_header:
                csvWriter.writeheader()
            out_rows = []
            for key, data in aNestedDict.items():
                row = {FieldNames[0]: key}
                row.update(data)
                out_rows.append(row)
            csvWriter.writerows(out_rows)
    #-------------------------------------------------------------------------
