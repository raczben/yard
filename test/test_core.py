"""
Test util functions
"""
import pytest
import os

import yard.core

here = os.path.abspath(os.path.join(__file__, os.pardir))
repo_root = os.path.abspath(os.path.join(here, os.pardir))

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


def test_stride():
    stride_yard = os.path.join(repo_root, 'examples', 'stride_test.yard')
    db = yard.core.DataBase(stride_yard)
    assert db['name'] == 'stride_test'

    db.fillAllFields()
    db.resolveAddress()
    
    for iface in db['interfaces']:
        registers = iface['registers']
        
        # full_spec_reg
        # 0:stride:4:0x100
        full_spec_reg = registers[0]
        assert full_spec_reg['name'] == 'full_spec_reg'
        pAddr = full_spec_reg['parsedAddress']
        assert pAddr['count'] == 4
        assert pAddr['increment'] == 0x100
        assert pAddr['serialNumber'] == -1
        assert pAddr['start'] == 0
        assert pAddr['value'] == [0, 0x100, 0x200, 0x300]
        
        # auto_start_reg1
        # -1:stride:4:0x100
        auto_start_reg1 = registers[1]
        assert auto_start_reg1['name'] == 'auto_start_reg1'
        pAddr = auto_start_reg1['parsedAddress']
        assert pAddr['count'] == 4
        assert pAddr['increment'] == 0x100
        assert pAddr['serialNumber'] == -1
        assert pAddr['start'] == 4
        assert pAddr['value'] == [4, 0x104, 0x204, 0x304]
        
        # auto_start_reg2
        # -1:stride:4:0x100
        auto_start_reg2 = registers[2]
        assert auto_start_reg2['name'] == 'auto_start_reg2'
        pAddr = auto_start_reg2['parsedAddress']
        assert pAddr['count'] == 4
        assert pAddr['increment'] == 0x100
        assert pAddr['serialNumber'] == -1
        assert pAddr['start'] == 8
        assert pAddr['value'] == [8, 0x108, 0x208, 0x308]
        
        # auto_start_auto_step_reg1
        # -1:stride:4
        auto_start_auto_step_reg1 = registers[3]
        assert auto_start_auto_step_reg1['name'] == 'auto_start_auto_step_reg1'
        pAddr = auto_start_auto_step_reg1['parsedAddress']
        assert pAddr['count'] == 4
        assert pAddr['increment'] == 0x4
        assert pAddr['serialNumber'] == -1
        assert pAddr['start'] == 0xc
        assert pAddr['value'] == [0xc, 0xc+4, 0xc+8, 0xc+12]
        
        # auto_start_auto_step_reg2
        # -1:stride:4
        auto_start_auto_step_reg2 = registers[4]
        assert auto_start_auto_step_reg2['name'] == 'auto_start_auto_step_reg2'
        pAddr = auto_start_auto_step_reg2['parsedAddress']
        assert pAddr['count'] == 4
        assert pAddr['increment'] == 0x4
        assert pAddr['serialNumber'] == -1
        assert pAddr['start'] == 0x1C
        assert pAddr['value'] == [0x1c, 0x1c+4, 0x1c+8, 0x1c+12]
    
    