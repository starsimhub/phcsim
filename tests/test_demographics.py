"""
Test demographics components
"""

import phcsim as phc


def test_data_load():
    d = phc.load_data()
    return d


def test_births():
    d = phc.load_data()
    births = phc.Births()
    births.init_pre(d=d)
    return births


def test_deaths():
    d = phc.load_data()
    deaths = phc.Deaths()
    deaths.init_pre(d=d)
    return deaths


if __name__ == '__main__':
    d = test_data_load()
    births = test_births()
    deaths = test_deaths()
