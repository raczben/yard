"""
Test util functions
"""
import pytest
import os
import logging 
import subprocess
import shutil

import yard.core

here = os.path.abspath(os.path.join(__file__, os.pardir))
repo_root = os.path.abspath(os.path.join(here, os.pardir))

'''
--------------------------------------
        TEST C Generator
--------------------------------------
'''


def generate_tcl_file(fname):
    minimal_yard = os.path.join(repo_root, 'examples', fname)
    
    logging.info("Reading descriptor...")
    db = yard.core.DataBase(minimal_yard)
        
    logging.info("Starting fill all fields...")
    db.fillAllFields()
    
    logging.info("Starting resolveAddress...")
    db.resolveAddress()
    
    logging.info("Starting dumping...")
    db.export()
    
    logging.info("Starting rendering C ")
    gen = yard.core.TCLBaseGenerator(db)
    
    logging.info("  Starting generateRenderData...")
    gen.generateRenderData()
    
    gen.exportRenderJobs()
    
    logging.info("  Starting render...")
    gen.render()
     
     
def syntax_check(fname):
    errFile = '~stderr.txt'
    outFile = '~stdout.txt'
    cmd = 'gcc -c {}'.format(fname)
    
    # Pytest asserts the non-zero return status of subprocess
    out = subprocess.check_output(cmd.split(' '))
    
    # Dump the error file (regardless of the content)
    # print(open(errFile).read())
    
    # Raise error if the error file isn't empty:
    # assert os.stat(errFile).st_size == 0
    
def functional_check(dirname):
    src = os.path.join('test', 'minimal_main.c')
    dst = os.path.join(dirname, 'minimal_main.c')
    shutil.copyfile(src, dst)

    srcfiles = ['minimal_main.c', 'minimal.c']
    srcfiles = ' '.join([os.path.join(dirname, x) for x in srcfiles])
    cmd = 'gcc -o minimal {}'.format(srcfiles)
    
    # Pytest asserts the non-zero return status of subprocess
    out = subprocess.check_output(cmd.split(' '))
    
    # Run the compiled test program:
    out = subprocess.check_output("./minimal")
    

def test_minimal():
    generate_tcl_file('minimal.yard')
    
    # Check that files has been generated:
    tclpath = 'examples/src/minimal.tcl'
    assert os.path.isfile(tclpath)
    
    src = os.path.join('test', 'minimal_main.tcl')
    dst = os.path.join('examples/src', 'minimal_main.tcl')
    shutil.copyfile(src, dst)
    
    cmd = 'tclsh {}'.format('minimal_main.tcl')
    out = subprocess.check_output(cmd.split(' '), cwd=r'examples/src')
    
    shutil.rmtree('examples/src')
    
    
    