"""
=======
iotools
=======

A collection of methods for input and outputting data
"""
import csv
__author__ = """Michael E. Rose (Michael.Ernst.Rose@gmail.com)"""
__all__ = ['csv_to_dict', 'csv_to_nested_dict', 'nested_dict_to_csv']
__version__ = 0.3

def csv_to_dict(filename,key_func,value_func,skip_header=True):
    """
    Reads a csv as a dictionary, where values and keys are set
    in a flexible manner. Delimiters are determined automatically.

    Parameters
    ----------
    filename: the name of the source file (str)
    key_func: a function specifying which row(s) to use as dictionary key (func)
    value_func: a function specifiying which row(s) to use as dictionary values (func)
    skip_header: whether the header should be skpped (boolean - p)

    Returns
    -------
    dictionary object
    """
    aDict = {}
    with open(filename, 'r') as f:
        dialect = csv.Sniffer().sniff(f.readline())
        f.seek(0)
        csvReader = csv.reader(f, dialect=dialect)
        if skip_header: next(csvReader, None)
        for row in csvReader:
            key = key_func(row)
            aDict[key] = value_func(row)
    return aDict


def csv_to_nested_dict(filename,key_func,ordered=False):
    """
    Reads a csv as a dictionary of dictionaries, where keys are set
    in a flexible manner. Delimiters are determined automatically.

    Parameters
    ----------
    filename: the name of the source file (str)
    key_func: a function specifying which row(s) to use as dictionary key (func)
    ordered: whether to return a nested dict instead of an ordinary dict (boolean -o)

    Returns
    -------
    dictionary object or ordered dictionary object
    """
    with open(filename,'r') as f:
        dialect = csv.Sniffer().sniff(f.readline())
        f.seek(0)
        if ordered:
            csvReader = csv.reader(f, dialect=dialect)
            from collections import OrderedDict
            aDict = OrderedDict()
            fields = next(csvReader)
            for row in csvReader:
                temp = OrderedDict(zip(fields, row))
                key = key_func(temp)
                aDict[key] = temp
        else:
            csvReader = csv.DictReader(f, dialect=dialect)
            aDict = {}
            for row in csvReader:
                key = key_func(row)
                aDict[key] = row
    return aDict


def nested_dict_to_csv(nested_dict,file_name,fields='',header=True):
    """
    Prints a nested dictionary to csv.

    Parameters
    ----------
    nested_dict: a dictionary of dictionaries (dictionary object)
    file_name: the name of output file (str)
    fields: the ordering of subkeys with the first entry being the main key (list of str)
    header: set to False if header should not be written (boolean - o)
    """
    with open(file_name,'w') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        if header:
            w.writeheader()
        for k in nested_dict:
            w.writerow({field: nested_dict[k].get(field) or k for field in fields})
