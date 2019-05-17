"""
Test util functions
"""
import pytest

import yard.util


def test_toInt():
    assert yard.util.toInt('0') == 0
    assert yard.util.toInt('-0') == 0
    assert yard.util.toInt('1') == 1
    assert yard.util.toInt('-1') == -1
    assert yard.util.toInt('1000') == 1000
    
    assert yard.util.toInt('0x0') == 0
    assert yard.util.toInt('0x6') == 0x6
    assert yard.util.toInt('0xabcd') == 0xabcd
    assert yard.util.toInt('0x1234567') == 0x1234567
    
    assert yard.util.toInt('0.0') == 0
    assert yard.util.toInt('3.1415') == 3
    assert yard.util.toInt('0.000001') == 0
    assert yard.util.toInt('123456.0') == 123456
    
    with pytest.raises(Exception):
        yard.util.toInt('Test throw')
    with pytest.raises(Exception):
        yard.util.toInt('')

test_string = 'Puskás started his career in Hungary playing for Kispest and Budapest Honvéd. He was the top scorer in the Hungarian League on four occasions, and in 1948, he was the top goal scorer in Europe. During the 1950s, he was both a prominent member and captain of the Hungarian national team, known as the Mighty Magyars. In 1958, two years after the Hungarian Revolution, he emigrated to Spain where he played for Real Madrid. While playing with Real Madrid, Puskás won four Pichichis and scored seven goals in two European Champions Cup finals.'
first_sentence = 'Puskás started his career in Hungary playing for Kispest and Budapest Honvéd.'

def test_getFirstSentence():
    assert yard.util.getFirstSentence(test_string) == first_sentence
    
