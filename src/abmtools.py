"""
Robustness check for Agent-Based Models (conceivably other models as well) across the whole of the multidimensional
parameter space.

Date of last update: 04-09-2015 (Cape Town)
"""
__author__ = '\n'.join(["Pawel Fiedor (pawel@fiedor.eu)",
                        "Co-Pierre Georg (cogeorg@gmail.com)"])
__version__ = 0.1

# Libraries
import sys
import random
import subprocess
import importlib
import operator
import math
import csv
import time
import glob

# ---------------------------------------------------------------------------
#
# CLASS ABMTools
#
# ---------------------------------------------------------------------------
class ABMTools(object):
    __version__ = 0.1

    """
    Parameters
    """
    # Lists for input and output model parameter range and type (int/float), as well as the target for the hypothesis
    # test (H_0: out_target = result of the simulation)
    par_type = []
    par_low = []
    par_high = []
    out_type = []
    out_low = []
    out_high = []
    out_target = []
    # Distance type to be used - either Euclidean ('euclid') or squared Euclidean [not technically a metric]
    # ('squared'): https://en.wikipedia.org/wiki/Euclidean_distance
    dist_type = ""
    # Number of random parameter samples used to test the hypothesis
    sweep_num = 0
    # Random parameter sample (drawn every sweep)
    par_sample = []
    # Script name, contains name of the script to be called (without file extension as we expect .py, and the name of
    # the function within the script which returns the tested parameter)
    script_name = ""
    funct_name = ""
    # Outputs (whatever we get from running the scripts with the drawn parameters)
    out_gotten = []
    # Operational parameters (internal, for looping)
    adding_par = True
    adding_out = True
    par_test = ""
    # Passed arguments (config filename)
    args = sys.argv

    # collated results from files [csv columns as elements in lists]
    all_read = []
    int_good = 0
    int_sample = 0
    goodness = 0

    """
    Functions
    """

    def __init__(self):
        self.num_runs = 0  # how many runs we do
        self.model_parameters = {}  # the parameters of the model
        self.run_parameters = []  # this is an array of model_parameters with length self.num_runs


#
# HELPER METHODS
#
    # Not used, created for testing [adds more details than the standard one below]
    def write_output_one_full(self, FileName, out_got, max_d):
        with open(FileName, 'w', newline='') as f:
            csvWriter = csv.writer(f, lineterminator='\n')
            csvWriter.writerow(['Difference', "Max difference"])
            out_rows = []
            for key in range(0, len(out_got)):
                int_row = []
                int_row.append(abs(out_got[key][0]-out_target[0]))
                int_row.append(max_d)
                out_rows.append(int_row)
            csvWriter.writerows(out_rows)


    # Not used, created for testing [adds more details than the standard one below]
    def write_output_mult_full(self, FileName, out_got, max_d):
        with open(FileName, 'w', newline='') as f:
            csvWriter = csv.writer(f, lineterminator='\n')
            tempheader = []
            for key in range(0, len(out_got)):
                for kkey in range(0, len(out_got[key])):
                    tempheader.append("Difference")
                    tempheader.append("Max difference")
            csvWriter.writerow(tempheader)
            out_rows = []
            for key in range(0, len(out_got)):
                int_row = []
                for kkey in range(0, len(out_got[key])):
                    int_row.append(abs(out_got[key][kkey][0]-out_target[kkey]))
                    int_row.append(max_d[y])
                out_rows.append(int_row)
            csvWriter.writerows(out_rows)


    # Writes CSV file with the data needed to collate results from parallel runs [case for single output]
    def write_output_one(self, FileName, inter, leng):
        with open(FileName, 'w', newline='') as f:
            csvWriter = csv.writer(f, lineterminator='\n')
            csvWriter.writerow(['Aggregate sample difference', "Sample size"])
            out_row = [inter, leng]
            csvWriter.writerow(out_row)


    # Writes CSV file with the data needed to collate results from parallel runs [case for multiple outputs]
    def write_output_mult(self, FileName, inter, max_e, leng):
        with open(FileName, 'w', newline='') as f:
            csvWriter = csv.writer(f, lineterminator='\n')
            csvWriter.writerow(['Aggregate sample difference', 'Max Euclidean difference', "Sample size"])
            out_row = [inter, max_e, leng]
            csvWriter.writerow(out_row)


    # Writes CSV file with all the results obtained from running the script so the distibution of the results can be analysed externally (R+ggplot2 presumably)
    def write_output_all_one(self, FileName, reslts):
        with open(FileName, 'w', newline='') as f:
            csvWriter = csv.writer(f, lineterminator='\n')
            csvWriter.writerow(['Output parameter'])
            for x in range(0, len(reslts)):
                out_row = []
                out_row.append(reslts[x])
                csvWriter.writerow(out_row)


    # Writes CSV file with all the results obtained from running the script so the distibution of the results can be analysed externally (R+ggplot2 presumably)
    def write_output_all_mult(self, FileName, reslts):
        with open(FileName, 'w', newline='') as f:
            csvWriter = csv.writer(f, lineterminator='\n')
            outhead = []
            for k in range(0, len(reslts[0])):
                outhead.append('Output parameter')
            csvWriter.writerow(outhead)
            for x in range(1, len(reslts)):
                out_row = []
                for y in range(0, len(reslts[0])):
                    out_row.append(reslts[x][y])
                csvWriter.writerow(out_row)


    # Gets the config of the csv file
    def getDialect(self, aFile):

        return = csv.Sniffer().sniff(aFile.readline())


    # Reads the CSV file into needed data [one dimension]
    def read_output_one(self, FileName):
        with open(FileName, 'r') as f:
            csvDialect = self.getDialect(f)
            f.seek(0)
            csvReader = csv.reader(f, dialect=csvDialect)
            next(csvReader, None)
            return [row for row in csvReader]

    def read_config(self, FileName):
        """
        Reads config file (xml)

        Example of a config file below:

        <config identifier="test">
            <parameter type="input" kind="integer" low="1" high="3"></parameter>
            <parameter type="output" kind="float" low="0.0" high="4.0" target="2.0"></parameter>
            <parameter type="output" kind="float" low="0.0" high="4.0" target="2.0"></parameter>
            <parameter type="sweeps" number="10"></parameter>
            <parameter type="distance" kind="squared"></parameter>
            <parameter type="script" name="testm" function="main"></parameter>
        </config>

        Notes:
        Identifier of the config file is not used in the code.
        Input and output parameter entries may be repeated for multiples. Output parameters require target stating the hypothesis.
        The number of sweeps should be an integer.
        The distance may be set to either 'euclid' for Euclidean distance or 'squared' for squared Euclidean distance (not technically a metric, however).
        The name of the script to be called and the name of the function returning the parameter within it should be provided [without file extension].
        """

        # Make the variables global, as we use them outside the function
        global par_type
        global par_low
        global par_high
        global out_type
        global out_low
        global out_high
        global out_target
        global sweep_num
        global script_name
        global funct_name
        global dist_type

        par_type = self.par_type
        par_low = self.par_low
        par_high = self.par_high
        out_type = self.out_type
        out_low = self.out_low
        out_high = self.out_high
        out_target = self.out_target
        sweep_num = self.sweep_num
        script_name = self.script_name
        funct_name = self.funct_name
        dist_type = self.dist_type

        # Open the file
        from xml.etree import ElementTree
        xmlText = open(FileName).read()

        element = ElementTree.XML(xmlText)

        # Loop over all entries in the xml file, getting all the required values
        for subelement in element:
            if (subelement.attrib['type'] == 'input'):
                if (subelement.attrib['kind'] == 'integer'):
                    par_type.append("int")
                    par_low.append(int(subelement.attrib['low']))
                    par_high.append(int(subelement.attrib['high']))
                elif (subelement.attrib['kind'] == 'float'):
                    par_type.append("float")
                    par_low.append(float(subelement.attrib['low']))
                    par_high.append(float(subelement.attrib['high']))
                else:
                    print("Error reading config file.")
            elif (subelement.attrib['type'] == 'output'):
                if (subelement.attrib['kind'] == 'integer'):
                    out_type.append("int")
                    out_low.append(int(subelement.attrib['low']))
                    out_high.append(int(subelement.attrib['high']))
                    out_target.append(int(subelement.attrib['target']))
                elif (subelement.attrib['kind'] == 'float'):
                    out_type.append("float")
                    out_low.append(float(subelement.attrib['low']))
                    out_high.append(float(subelement.attrib['high']))
                    out_target.append(float(subelement.attrib['target']))
                else:
                    print("Error reading config file.")
            elif (subelement.attrib['type'] == 'sweeps'):
                sweep_num = int(subelement.attrib['number'])
            elif (subelement.attrib['type'] == 'distance'):
                dist_type = subelement.attrib['kind']
            elif (subelement.attrib['type'] == 'script'):
                script_name = subelement.attrib['name']
                funct_name = subelement.attrib['function']
            else:
                print("Error reading config file.")


#
# WORKER METHODS
#

    def read_input(self):

        # Make the variables global, as we use them outside the function
        global par_type
        global par_low
        global par_high
        global out_type
        global out_low
        global out_high
        global out_target
        global sweep_num
        global script_name
        global funct_name
        global dist_type
        adding_par = True
        adding_out = True

        par_type = self.par_type
        par_low = self.par_low
        par_high = self.par_high
        out_type = self.out_type
        out_low = self.out_low
        out_high = self.out_high
        out_target = self.out_target
        sweep_num = self.sweep_num
        script_name = self.script_name
        funct_name = self.funct_name
        dist_type = self.dist_type

        # Add input parameters
        while adding_par:
            par_test = input("Do you want to add another input parameter (float/integer/no): ")
            if par_test == 'no':
                adding_par = False
            elif par_test == 'integer':
                par_type.append("int")
                par_low.append(int(input("Enter the lower parameter bound: ")))
                par_high.append(int(input("Enter the higher parameter bound: ")))
            elif par_test == 'float':
                par_type.append("float")
                par_low.append(float(input("Enter the lower parameter bound: ")))
                par_high.append(float(input("Enter the higher parameter bound: ")))
            else:
                print("Unrecognized reply, use float, integer, or no.")

        # Add output parameters
        while adding_out:
            par_test = input("Do you want to add another output parameter (float/integer/no): ")
            if par_test == 'no':
                adding_out = False
            elif par_test == 'integer':
                out_type.append("int")
                out_low.append(int(input("Enter the lower parameter bound: ")))
                out_high.append(int(input("Enter the higher parameter bound: ")))
                out_target.append(int(input("Enter the target parameter bound: ")))
            elif par_test == 'float':
                out_type.append("float")
                out_low.append(float(input("Enter the lower parameter bound: ")))
                out_high.append(float(input("Enter the higher parameter bound: ")))
                out_target.append(float(input("Enter the target parameter bound: ")))
            else:
                print("Unrecognized reply, use float, integer, or no.")

        # Add the number of samples
        sweep_num = int(input("Enter the number of times the simulation should be ran: "))
        # Add the distance to be used
        dist_type = input("Enter type of distance to be used (euclid for Euclidean, squared for squared Euclidean): ")
        # Add the script name to be ran
        script_name = input("Enter the name of the script that should be ran: ")
        # Add the function name to be called within the script
        funct_name = input("Enter the name of fuction to be called inside the script: ")


    """
    abmgoodness
    """
    def abmgoodness(self, confName):
        """
        Main program
        """

        # self.read_input() #This is to be uncommented [and the below line commented out] if manual parameter entry
        # is desired
        self.read_config(str(confName))

        # Here we randomise the parameter space to get a random sample and call the script with these random
        # parameters, looping this the desired number of times
        if len(par_type) > 0 and len(out_type) > 0:
            for sweeping in range(0, sweep_num):
                par_sample = []
                # We have the parameters, need to draw a random sample from uniform distribution supported on [min;max]
                for i in range(0, len(par_type)):
                    if par_type[i] == 'int':
                        par_sample.append(random.randint(par_low[i], par_high[i]))
                    else:
                        par_sample.append(random.uniform(par_low[i], par_high[i]))

                # Here we call the desired script and append the results with the returned value
                test = importlib.import_module(script_name)

                # this will need to be amended to whatever the script returns # TESTING ONLY
                # out_gotten.append(test.main(par_sample))

                # this will need to be amended to whatever fits what the script returns
                self.out_gotten.append(getattr(test, funct_name)(par_sample))

            # print(par_sample) #  this is for testing only
            # print(out_gotten) #  this is for testing only

            """
            Below we can get the full output for the external analysis of the results
            Uncomment the appropriate line for this purpose
            """
            # Here we can output all parameters returned by the analysed script, to do so uncomment the below
            # self.write_output_all_one('Results_full.csv', self.out_gotten)
            # self.write_output_all_mult('Results_full.csv', self.out_gotten)

            # Here we calculate the goodness of the model using either Euclidean or squared Euclidean distance from
            # the hypothesis
            if dist_type == "euclid":

                if len(out_type) == 1:
                    # Calculating goodness for one output
                    # out_gotten[i]
                    # First, calculate the maximum possible difference for normalisation
                    max_diff = 0
                    if (out_high[0] - out_target[0]) >= (out_target[0] - out_low[0]):
                        max_diff = abs(out_high[0] - out_target[0])
                    else:
                        max_diff = abs(out_target[0] - out_low[0])
                    # Then, calculate the sum of normalised differences between target in the hypothesis and the
                    # obtained results
                    intermediate=0
                    for x in range(0, len(self.out_gotten)):
                        intermediate += abs(self.out_gotten[x] - out_target[0]) / max_diff
                    # Finally, we average the results (with respect to sample length) and get the goodness of the
                    # model, which is printed out and saved in the decomposed form
                    goodness = 0
                    goodness = 1 - ( intermediate / float(len(self.out_gotten)) )
                    # print (goodness)
                    # Add return goodness if you so desire
                    # We write the output to .csv file for collating in case of parallel runs, the filename is unique
                    # based on system time
                    self.write_output_one('goodness_' + "".join(i for i in str(time.time()) if not ord(i)==46) + '.csv', intermediate, len(self.out_gotten))
                    return goodness
                else:
                    # Calculating goodness for multiple outputs
                    # out_gotten[i][j]
                    # First, calculate the maximum possible difference for normalisation [multidimensional]
                    max_diff = []
                    for x in range(0, len(out_type)):
                        if (out_high[x] - out_target[x]) >= (out_target[x] - out_low[x]):
                            max_diff.append(abs(out_high[x] - out_target[x]))
                        else:
                            max_diff.append(abs(out_target[x] - out_low[x]))
                    # Then, calculate the sum of normalised differences between target in the hypothesis and the obtained results [multidimensional]
                    intermediate=0
                    for x in range(0, len(self.out_gotten)):
                        anotherinter = 0
                        for y in range(0, len(self.out_gotten[x])):
                            anotherinter += (self.out_gotten[x][y] - out_target[y]) ** 2
                        intermediate += math.sqrt(anotherinter)
                    goodness = 0
                    # Calculate the Euclidean maximum for normalisation
                    max_euclid = 0
                    for x in range(0, len(out_type)):
                        max_euclid += max_diff[x] ** 2
                    max_euclid = math.sqrt(max_euclid)
                    # Finally, calculate goodness
                    goodness = 1 - ( intermediate / ( max_euclid * float(len(self.out_gotten) ) ) )
                    # print (goodness)
                    # Add return goodness if you so desire
                    # We write the output to .csv file for collating in case of parallel runs, the filename is unique based on system time
                    self.write_output_mult('goodness_' + "".join(i for i in str(time.time()) if not ord(i)==46) + '.csv', intermediate, max_euclid, len(self.out_gotten))
                    return goodness

            elif dist_type == "squared": # NOT A METRIC!

                if len(self.out_type) == 1:
                    # Calculating goodness for one output
                    # out_gotten[i]
                    # First, calculate the maximum possible (squared) difference for normalisation
                    max_diff = 0
                    if (out_high[0] - out_target[0]) >= (out_target[0] - out_low[0]):
                        max_diff = abs(out_high[0] - out_target[0]) ** 2
                    else:
                        max_diff = abs(out_target[0] - out_low[0]) ** 2
                    # Then, calculate the sum of normalised (squared) differences between target in the hypothesis and the obtained results
                    intermediate=0
                    for x in range(0, len(self.out_gotten)):
                        intermediate += (abs(self.out_gotten[x] - out_target[0]) ** 2) / max_diff
                    # Finally, we average the results (with respect to sample length) and get the goodness of the model, which is printed out and saved in the decomposed form
                    goodness = 0
                    goodness = 1 - ( intermediate / float(len(self.out_gotten) ) )
                    # print (goodness)
                    # Add return goodness if you so desire
                    # We write the output to .csv file for collating in case of parallel runs, the filename is unique based on system time
                    self.write_output_one('goodness_' + "".join(i for i in str(time.time()) if not ord(i)==46) + '.csv', intermediate, len(self.out_gotten))
                    return goodness
                else:
                    # Calculating goodness for multiple outputs
                    # out_gotten[i][j]
                    # First, calculate the maximum possible difference for normalisation [multidimensional]
                    max_diff = []
                    for x in range(0, len(out_type)):
                        if (out_high[x] - out_target[x]) >= (out_target[x] - out_low[x]):
                            max_diff.append((abs(out_high[x] - out_target[x]))**2)
                        else:
                            max_diff.append((abs(out_target[x] - out_low[x]))**2)
                    # Then, calculate the sum of (squared) differences between target in the hypothesis and the obtained results [multidimensional]
                    intermediate=0
                    for x in range(0, len(self.out_gotten)):
                        anotherinter = 0
                        for y in range(0, len(self.out_gotten[x])):
                            anotherinter += (self.out_gotten[x][y] - self.out_target[y]) ** 2
                        intermediate += anotherinter
                    goodness = 0
                    # Calculate the Euclidean maximum for normalisation
                    max_euclid = 0
                    for x in range(0, len(out_type)):
                        max_euclid += max_diff[x]
                    # max_euclid = max_euclid
                    # Finally, calculate goodness
                    goodness = 1 - ( intermediate / ( max_euclid * float(len(self.out_gotten) ) ) )
                    # print (goodness)
                    # Add return goodness if you so desire
                    # We write the output to .csv file for collating in case of parallel runs, the filename is unique based on system time
                    self.write_output_mult('goodness_' + "".join(i for i in str(time.time()) if not ord(i)==46) + '.csv', intermediate, max_euclid, len(self.out_gotten))
                    return goodness

            else:
                print("Wrong distance type entered (should be euclid for Euclidean or squared for squared Euclidean).")

        else:
            print("No input or output parameters entered.")


    """
    collate
    """
    def collate(self):
        '''
        Main program
        '''

        # Get data from all csv files in the directory [make sure there are no other csv files in the current directory]
        for files in glob.glob("*.csv"):
            all_read = self.all_read
            int_sample = self.int_sample
            int_good = self.int_good
            all_read.append(self.read_output_one(files))

        if len(all_read[0][0]) == 2:
            # calculate together (weighted average) for single output
            # First, calculate the number of sweeps that were ran together
            for x in range(0, len(all_read)):
                int_sample += int(all_read[x][0][1])
            # Then, calculate the average difference weighed by the number of sweeps in particular streams
            for x in range(0, len(all_read)):
                int_good +=  (float(all_read[x][0][0]) / float(all_read[x][0][1])) * (int(all_read[x][0][1]) / int_sample)
            goodness = 1 - int_good
            # Print goodness - may need to return it if used externally
            # print(goodness)
            return goodness
        # Add return goodness if you so desire
        elif len(all_read[0][0]) > 2:
            # calculate together (weighted average) for multiple outputs
            # First, calculate the number of sweeps that were ran together
            for x in range(0, len(all_read)):
                int_sample += int(all_read[x][0][2])
            # Then, calculate the average difference weighed by the number of sweeps in particular streams
            for x in range(0, len(all_read)):
                int_good +=  (float(all_read[x][0][0]) /  float(all_read[x][0][1]) / int_sample )
            goodness = 1 - int_good
            # Print goodness - may need to return it if used externally
            # print(goodness)
            return goodness
        # Add return goodness if you so desire
        else:
            print("Nothing has been read.")


    """
    initialize_run_parameters
    """
    def initialize_run_parameters(self, config):
        # there are config.static_parameters['runs'] runs
        self.num_simulations = int(config.static_parameters['num_simulations'])

        # create a dict of self.model_parameters, one for each run
        for i in range(0,self.num_simulations):
            # for each variable parameter, we need a value that is drawn from within the range
            self.model_parameters = {}  # clear the existing model parameters
            for param_key in sorted(config.variable_parameters.keys()):
                lower = config.variable_parameters[param_key][0]
                upper = config.variable_parameters[param_key][1]
                value = random.uniform(lower, upper)
                self.model_parameters[param_key] = value
            self.run_parameters.append(self.model_parameters)


    """
    runner
    """
    def runner(self, config):
        # first, initialize the run parameters
        self.initialize_run_parameters(config)
        # at this point, we have static parameters with the number of runs and the model config file

        for entry in self.run_parameters:
            print entry
        print self.num_simulations, len(self.run_parameters)
