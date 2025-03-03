"""
Test demographics components
"""

import phcsim as phc

def test_births():
    d = phc.load_data()
    sim = phc.Sim()
    births = phc.Births()
    births.init_pre(sim)
    assert births.df is not None
    assert births.df.shape[0] > 0
    assert births.df.shape[1] > 0