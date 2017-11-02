"""
Created on the 19th of October, 2017

Container module for GapiExceptions
"""

class GapiException(Exception):
    pass

class GapiHardExit(GapiException):
    pass
