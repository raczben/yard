# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 15:28:15 2019

@author: usr
"""

# Import build in modules
#  - os needed for file and directory manipulation
#  - sys needed for Python path manipulations
#  - argparse needed to parse command line arguments
import os
import sys
import argparse

# To run standalone we need to add this module to pythonpath.
yard_module_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(yard_module_path)

# import YARD modules
import core


def main():
    parser = argparse.ArgumentParser(description='YARD: Yet Another Register Designer tool for FPGA')
    parser.add_argument('yardfile', nargs='+', help='YARD register descriptor file.')
    args = parser.parse_args()
    if isinstance(args.yardfile, list):
        args.yardfile = args.yardfile[0]
    print(args.yardfile)

    datafile = args.yardfile
    
    ctrl = core.Controller(datafile=datafile)
    ctrl.doAll()
    
 
    
if __name__ == '__main__':
    """ The main function requires a filepath pointing on a yard file, then process it.
    """
    main()

