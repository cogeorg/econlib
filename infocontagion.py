#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys
import random

from src.abmimplementation.config import Config
from src.abmimplementation.runner import Runner

if __name__ == '__main__':
    runner_config_file_name = sys.argv[1]

    runner_config = Config()
    runner_config.read_xml_config_file(runner_config_file_name)

    runner = Runner(runner_config)
    runner.do_run()

