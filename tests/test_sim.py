"""
Test full sim
"""

import sciris as sc
import phcsim as phc

do_plot = False


def test_basic_sim(do_plot=do_plot):
    sc.heading('Testing basic sim')
    sim = phc.Sim(demographics=None)
    sim.init()
    sim.run()
    return sim


if __name__ == '__main__':

    do_plot = True

    T = sc.timer()

    sim = test_basic_sim(do_plot=do_plot)

    T.toc()
