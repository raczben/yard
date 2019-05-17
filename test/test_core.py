"""
Test util functions
"""
import pytest

import yard.core

'''
--------------------------------------
        TEST DataBase
--------------------------------------
'''


def test_init_defaults():
    db = yard.core.DataBase()
    
    assert db._defaults['generalDefaults']['name'] == 'gpio'
    assert db._defaults['interfaceDefaults']['type'] == 'AXI'
    assert db._defaults['interfaceDefaults']['type'] == 'AXI'
    assert db._defaults['registerDefaults']['parsedAddress']['value'] == None
    assert db._defaults['fieldsDefaults']['brief'] == ''
    