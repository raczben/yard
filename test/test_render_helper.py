"""
Test util functions
"""
import pytest
import os

import yard.renderhelper

here = os.path.abspath(os.path.join(__file__, os.pardir))
repo_root = os.path.abspath(os.path.join(here, os.pardir))

'''
--------------------------------------
        TEST DataBase
--------------------------------------
'''

longTestString = 'In 1827, Jedlik started experimenting with electromagnetic rotating devices which he called lightning-magnetic self-rotors, and in 1828 he demonstrated the first device which contained the three main components of practical direct current motors: the stator, rotor, and commutator.'

commentedTestString = \
'''-- In 1827, Jedlik started experimenting with electromagnetic rotating devices
-- which he called lightning-magnetic self-rotors, and in 1828 he demonstrated
-- the first device which contained the three main components of practical
-- direct current motors: the stator, rotor, and commutator.'''

def test_fmt_comment():
    assert commentedTestString == yard.renderhelper.fmt_comment(longTestString)
    
    
listOfHungarianNobels = [
    'Philipp Lenard',
    'Robert Bárány',
    'Richard Adolf Zsigmondy',
    'Albert Szent-Györgyi',
    'George de Hevesy',
    'Georg von Békésy',
    'Eugene Wigner',
    'Dennis Gabor',
    'John Polanyi',
    'George Olah',
    'John Harsanyi',
    'Imre Kertész',
    'Avram Hershko'
    ]
    
formattedList = '''Philipp Lenard, Robert Bárány, Richard Adolf Zsigmondy, Albert Szent-Györgyi,
George de Hevesy, Georg von Békésy, Eugene Wigner, Dennis Gabor, John Polanyi,
George Olah, John Harsanyi, Imre Kertész, Avram Hershko'''
    
def test_fmt_list():
    assert formattedList == yard.renderhelper.fmt_list(listOfHungarianNobels)