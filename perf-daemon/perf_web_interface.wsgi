#!/usr/bin/python
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from perf_web_interface import app as application

# uncomment this to get more information
#application.debug = True
