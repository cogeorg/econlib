#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys
from abmtools import ABMTools


"""
Testing for the robustness check for Agent-Based Models (conceivably other models as well) across the whole of the multidimensional parameter space.

    test_abmtools test_number config_file_name

Author: Pawel Fiedor (pawel@fiedor.eu)
        Co-Pierre Georg (cogeorg@gmail.com)

Version: 0.03

Date of last update: 2015-09-13 (Cape Town)

"""
if __name__ == '__main__':

    args = sys.argv

    # we have multiple tests, first argument specifies which test to run, further arguments depend on the test, see below
    test_number = args[1]


"""
Test 1: Running the goodness check across parameter space with one output parameter

Argument 1 should be the number of the test, i.e. 1
Argument 2 should be the filename of the config file

python test_abmtools 1 config.xml

Config file example (config.xml):

<config identifier="test">
    <parameter type="input" kind="integer" low="1" high="3"></parameter>
    <parameter type="output" kind="float" low="0.0" high="4.0" target="2.0"></parameter>
    <parameter type="sweeps" number="10"></parameter>
    <parameter type="distance" kind="squared"></parameter>
    <parameter type="script" name="test" function="main"></parameter>
</config>

Input parameter needs its kind (integer/float) and domain (low and high values).
Output parameter needs its kind (integer/float) and domain (low and high values), as well as target value tested in the
hypothesis (target). The config may contain multiple instances of both output and input parameters (as necessitated by
the script to be tested). The number of sweeps should be an integer.

The distance used should be either 'euclid' for Euclidean distance or 'squared' for squared Euclidean distance.
Script parameter should contain the name of the script to be tested and the name of the function called within it (which returns the results).

"""
if test_number == "1":
    abmtools = ABMTools()
    testout = abmtools.abmgoodness(args[2])
    print("ABMTools version: " + str(abmtools.__version__))
    print("Test number: " + str(args[1]))
    print("Ran with " + str(args[2]) + " and gotten goodness of " + str(testout))


"""
Test 2: Running the goodness check across parameter space with multiple output parameters

Argument 1 should be 2
Argument 2 should be the filename of the config file

python test_abmtools 2 configm.xml

Config file example (configm.xml):

<config identifier="test">
    <parameter type="input" kind="integer" low="1" high="3"></parameter>
    <parameter type="output" kind="float" low="0.0" high="4.0" target="2.0"></parameter>
    <parameter type="output" kind="float" low="0.0" high="4.0" target="2.0"></parameter>
    <parameter type="sweeps" number="10"></parameter>
    <parameter type="distance" kind="euclid"></parameter>
    <parameter type="script" name="testm" function="main"></parameter>
</config>

Input parameter needs its kind (integer/float) and domain (low and high values).
Output parameter needs its kind (integer/float) and domain (low and high values), as well as target value tested in the hypothesis (target).
The config may contain multiple instances of both output and input parameters (as necessitated by the script to be tested).
The number of sweeps should be an integer.
The distance used should be either 'euclid' for Euclidean distance or 'squared' for squared Euclidean distance.
Script parameter should contain the name of the script to be tested and the name of the function called within it (which returns the results).
"""
if test_number == "2":
    abmtools = ABMTools()
    testout = abmtools.abmgoodness(args[2])
    print("ABMTools version: " + str(abmtools.__version__))
    print("Test number: " + str(args[1]))
    print("Ran with " + str(args[2]) + " and gotten goodness of " + str(testout))


"""
Test 3: Collating results from parallel ran instances [the csv files saved from these runs, should be in the working directory, need to include no other csv files in the directory] of the above (need to be from the same config, obviously)

Argument 1 should be 3

python test_abmtools 3

"""
if test_number == "3":
    abmtools = ABMTools()
    testout = abmtools.collate()
    print("ABMTools version: " + str(abmtools.__version__))
    print("Test number: " + str(args[1]))
    print("Ran to collate results and gotten goodness of " + str(testout))



"""
Test 4:
"""
if test_number == "4":
    # imports besides abmtools
#    from conftools import Config

    # we have a second parameter
    config_file_name = args[2]

    abmtools = ABMTools()
    config = Config()
    config.read_xml_config_file(config_file_name)

    abmtools.runner(config)



if test_number == "5":
    from src.abmtools.baseconfig import BaseConfig

    class Config(BaseConfig):
        identifier = None

        def __init__(self, _identifier):
            self.set_identifier(_identifier)

        def get_identifier(self):
            return self.identifier
        def set_identifier(self, _identifier):
            super(Config, self).set_identifier(_identifier)


    arr = "f"#['0','1']
    a = Config("a")
    print a.get_identifier()
    b = Config("b")
    print b.get_identifier(), a.get_identifier()