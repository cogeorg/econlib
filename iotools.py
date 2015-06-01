#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = """Michael Rose (michael.q.rose@gmail.com)"""

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
    __version__ = 0.1

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
                skip_header = True
    ):
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
            dialect = csv.Sniffer().sniff(f.read(1024), delimiters=";,")
            f.seek(0)
            csvReader = csv.reader(f, dialect)
            if skip_header:
                next(csvReader, None)
            for row in csvReader:
                key = key_func(row)
                aDict[key] = value_func(row)

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
                       FirstFieldName = ""
    ):
        """
        Takes an dictionary of dictionatires and outputs it as csv with keys as rownames and subkeys as column names

        Args:
            aNestedDict (dict) -- a dictionary of dictionaries
            FileName (str) -- the name of target file
            FirstFieldName (str - optional) -- the name of the first column (ie the name for the keys - if none is given,
                                               the field is empty)

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
            csvWriter.writeheader()
            out_rows = []
            for key, data in aNestedDict.items():
                row = {FieldNames[0]: key}
                row.update(data)
                out_rows.append(row)
            csvWriter.writerows(out_rows)
    #-------------------------------------------------------------------------
