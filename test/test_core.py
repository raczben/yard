"""
Test util functions
"""
import pytest
import os
import logging 

from . import util

import yard.core

here = os.path.abspath(os.path.join(__file__, os.pardir))
repo_root = os.path.abspath(os.path.join(here, os.pardir))
work_dir = '.test/core'

'''
--------------------------------------
        TEST DataBase
--------------------------------------
'''


def test_init_defaults():
    db = yard.core.DataBase()
    
    assert db._defaults['generalDefaults']['name'] == 'gpio'
    assert db._defaults['interfaceDefaults']['type'] == 'AXI'
    assert db._defaults['registerDefaults']['parsedAddress']['value'] == None
    assert db._defaults['fieldsDefaults']['brief'] == ''
    
    
def test_loadDefaults():
    db = yard.core.DataBase()
    
    assert db['name'] == 'gpio'
    # assert db['interfaces'][0]['type'] == 'AXI'
    
  
def test_getDatawidth():
    db = yard.core.DataBase()
    
    with pytest.raises(yard.core.YardException):
        db.getDatawidth()
    
    db.addInterface()
    assert db.getDatawidth() == 32
    

def test_load_from_file():
    minimal_yard = os.path.join(repo_root, 'examples', 'minimal.yard')
    db = yard.core.DataBase(minimal_yard)
    assert db['name'] == 'minimal'
    assert db['interfaces'][0]['name'] == 'axi'
    assert db['interfaces'][0]['type'] == 'AXI'
    assert db['interfaces'][0]['registers'][0]['name'] == 'data'
    assert db['interfaces'][0]['registers'][0]['access'] == 'RW'
    with pytest.raises(KeyError):
        db['interfaces'][0]['registers'][0]['address']
        
    db.loadDefaults()
    assert db['interfaces'][0]['registers'][0]['address'] == None
    assert db['interfaces'][0]['registers'][0]['width'] == None
    assert db['interfaces'][0]['registers'][0]['type'] == 'std_logic_vector'


def test_fillAllFields():
    gpio_yard = os.path.join(repo_root, 'examples', 'gpio.yard')
    db = yard.core.DataBase(gpio_yard)
    assert db['name'] == 'gpio'
    assert len(db['interfaces'][0]['registers']) == 4
        
    db.fillAllFields()
    assert db['interfaces'][0]['registers'][0]['address'] == -1
    assert db['interfaces'][0]['registers'][0]['width'] == 32
    assert db['interfaces'][0]['registers'][0]['type'] == 'std_logic_vector'


def test_array():
    array_yard = os.path.join(repo_root, 'examples', 'array_test.yard')
    db = yard.core.DataBase(array_yard)
    assert db['name'] == 'array_test'

    db.fillAllFields()
    db.resolveAddress()
    
    for iface in db['interfaces']:
        registers = iface['registers']
        
        # full_spec_reg
        # 0:array:4:0x100
        full_spec_reg = registers[0]
        assert full_spec_reg['name'] == 'full_spec_reg'
        pAddr = full_spec_reg['parsedAddress']
        assert pAddr['count'] == 4
        assert pAddr['increment'] == 0x100
        assert pAddr['serialNumber'] == -1
        assert pAddr['start'] == 0
        assert pAddr['value'] == [0, 0x100, 0x200, 0x300]
        
        # auto_start_reg1
        # -1:array:4:0x100
        auto_start_reg1 = registers[1]
        assert auto_start_reg1['name'] == 'auto_start_reg1'
        pAddr = auto_start_reg1['parsedAddress']
        assert pAddr['count'] == 4
        assert pAddr['increment'] == 0x100
        assert pAddr['serialNumber'] == -1
        assert pAddr['start'] == 4
        assert pAddr['value'] == [4, 0x104, 0x204, 0x304]
        
        # auto_start_reg2
        # -1:array:4:0x100
        auto_start_reg2 = registers[2]
        assert auto_start_reg2['name'] == 'auto_start_reg2'
        pAddr = auto_start_reg2['parsedAddress']
        assert pAddr['count'] == 4
        assert pAddr['increment'] == 0x100
        assert pAddr['serialNumber'] == -1
        assert pAddr['start'] == 8
        assert pAddr['value'] == [8, 0x108, 0x208, 0x308]
        
        # auto_start_auto_step_reg1
        # -1:array:4
        auto_start_auto_step_reg1 = registers[3]
        assert auto_start_auto_step_reg1['name'] == 'auto_start_auto_step_reg1'
        pAddr = auto_start_auto_step_reg1['parsedAddress']
        assert pAddr['count'] == 4
        assert pAddr['increment'] == 0x4
        assert pAddr['serialNumber'] == -1
        assert pAddr['start'] == 0xc
        assert pAddr['value'] == [0xc, 0xc+4, 0xc+8, 0xc+12]
        
        # auto_start_auto_step_reg2
        # -1:array:4
        auto_start_auto_step_reg2 = registers[4]
        assert auto_start_auto_step_reg2['name'] == 'auto_start_auto_step_reg2'
        pAddr = auto_start_auto_step_reg2['parsedAddress']
        assert pAddr['count'] == 4
        assert pAddr['increment'] == 0x4
        assert pAddr['serialNumber'] == -1
        assert pAddr['start'] == 0x1C
        assert pAddr['value'] == [0x1c, 0x1c+4, 0x1c+8, 0x1c+12]
    

def test_array_roll_out():
    array_yard = os.path.join(repo_root, 'examples', 'array_test.yard')
    db = yard.core.DataBase(array_yard)
    assert db['name'] == 'array_test'

    db.fillAllFields()
    db.resolveAddress()
    db.rollOutStride()
    
    for iface in db['interfaces']:
        registers = iface['registers']
        
        # full_spec_reg
        # 0:array:4:0x100
        for i, full_spec_reg in zip(range(0, 4), registers[0:4]):
            assert full_spec_reg['name'] == 'full_spec_reg'
            pAddr = full_spec_reg['parsedAddress']
            assert pAddr['count'] == -1
            assert pAddr['increment'] == -1
            assert pAddr['serialNumber'] == i
            assert pAddr['start'] == [0, 0x100, 0x200, 0x300][i]
            assert pAddr['value'] == [[0, 0x100, 0x200, 0x300][i]]
        
        # auto_start_reg1
        # -1:array:4:0x100
        for i, auto_start_reg1 in zip(range(0, 4), registers[4:8]):
            assert auto_start_reg1['name'] == 'auto_start_reg1'
            pAddr = auto_start_reg1['parsedAddress']
            assert pAddr['count'] == -1
            assert pAddr['increment'] == -1
            assert pAddr['serialNumber'] == i
            assert pAddr['start'] == [4, 0x104, 0x204, 0x304][i]
            assert pAddr['value'] == [[4, 0x104, 0x204, 0x304][i]]
        
        # auto_start_reg2
        # -1:array:4:0x100
        for i, auto_start_reg2 in zip(range(0, 4), registers[8:12]):
            assert auto_start_reg2['name'] == 'auto_start_reg2'
            pAddr = auto_start_reg2['parsedAddress']
            assert pAddr['count'] == -1
            assert pAddr['increment'] == -1
            assert pAddr['serialNumber'] == i
            assert pAddr['start'] == [8, 0x108, 0x208, 0x308][i]
            assert pAddr['value'] == [[8, 0x108, 0x208, 0x308][i]]
        
        # auto_start_auto_step_reg1
        # -1:array:4
        for i in range(4):
            auto_start_auto_step_reg1 = registers[i+12]
            assert auto_start_auto_step_reg1['name'] == 'auto_start_auto_step_reg1'
            pAddr = auto_start_auto_step_reg1['parsedAddress']
            assert pAddr['count'] == -1
            assert pAddr['increment'] == -1
            assert pAddr['serialNumber'] == i
            assert pAddr['start'] == [0xc, 0xc+4, 0xc+8, 0xc+12][i]
            assert pAddr['value'] == [[0xc, 0xc+4, 0xc+8, 0xc+12][i]]
        
        # auto_start_auto_step_reg2
        # -1:array:4
        for i in range(4):
            auto_start_auto_step_reg2 = registers[i+16]
            assert auto_start_auto_step_reg2['name'] == 'auto_start_auto_step_reg2'
            pAddr = auto_start_auto_step_reg2['parsedAddress']
            assert pAddr['count'] == -1
            assert pAddr['increment'] == -1
            assert pAddr['serialNumber'] == i
            assert pAddr['start'] == [0x1c, 0x1c+4, 0x1c+8, 0x1c+12][i]
            assert pAddr['value'] == [[0x1c, 0x1c+4, 0x1c+8, 0x1c+12][i]]
    
def test_bitfields():
    util.copy_to_work_dir(work_dir, 'examples/bitfields.yard')
    
    bitfields_yard = os.path.join(work_dir, 'bitfields.yard')
    db = yard.core.DataBase(bitfields_yard)
    assert db['name'] == 'bitfields'

    logging.info("Starting fill all fields...")
    db.fillAllFields()
    
    logging.info("Starting dumping...")
    db.export()
    
    for iface in db['interfaces']:
        registers = iface['registers']
        fruit_reg = registers[0]
        apple_bf = fruit_reg['fields'][0]
        assert apple_bf['name'] == 'apple'
        assert apple_bf['brief'] == 'Apple at 0'
        assert apple_bf['detail'] == 'Apple bit located at the LSB.'
        assert apple_bf['_positionLength'] == 1
        assert apple_bf['_positionStart'] == 0
        assert apple_bf['access'] == 'RW'
        
        blueberry_bf = fruit_reg['fields'][1]
        assert blueberry_bf['name'] == 'blueberry'
        assert blueberry_bf['_positionStart'] == 2
        assert blueberry_bf['_positionLength'] == 3
        assert blueberry_bf['access'] == 'RW'
        
        staccato_reg = registers[1]
        for i in range(32):
            bf = staccato_reg['fields'][i]
            assert bf['access'] == 'R'
            assert bf['name'] == chr(ord('a') + int(i/26)) + chr(ord('a') + i%26)
            assert bf['_positionLength'] == 1
            assert bf['_positionStart'] == i
            
        legato_reg = registers[2]
        bf = legato_reg['fields'][0]
        assert bf['access'] == 'WO'
        assert bf['name'] == 'abcdefghijklmnopqrstuvwxyz'
        assert bf['_positionLength'] == 32
        assert bf['_positionStart'] == 0
    
    