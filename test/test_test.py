import pytest


def test_answer():
    with pytest.raises(Exception):
        a= 0/0
        
    # with pytest.raises(Exception):
        # a= 1/2