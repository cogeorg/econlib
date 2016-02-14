__author__ = """Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""
from math import ceil

#-------------------------------------------------------------------------
#
#  class File
#
#-------------------------------------------------------------------------
class File(object):
    __version__ = 0.91

#
#  METHODS
#
    def __init__(self):
        pass

    def split_file(self, input_file_name, _num_lines, _num_files):
        """
        Read in a large file with a predetermined number of lines and split it
        into several smaller files.
        """
        num_lines = int(_num_lines)
        num_files = int(_num_files)
        if input_file_name.count('.')>1:
            raise AssertionError("File name must contain only a single . as separator between identifier and extension.")
            exit

        file_identifier, file_extension = input_file_name.split('.') # used for input and output file name

        lines_to_read = ceil(num_lines/num_files)
        print lines_to_read

        #
        # read all lines in the input file, every so often, write them into a new output file
        #
        i = 0
        num_file = 0

        out_text = ""
        with open(input_file_name,'r') as input_file:
            for line in input_file.readlines():
                if i < lines_to_read:
                    out_text += line
                    i += 1
                else: # Write out and reset
                    out_file_name = "{}-{}.{}".format(file_identifier, num_file, file_extension)
                    with open(out_file_name,'w') as f:
                        f.write(out_text)
                    print out_file_name, "saved"
                    out_text = ""
                    num_file += 1
                    i = 0
