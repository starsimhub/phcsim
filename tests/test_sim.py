"""
Test full sim
"""

import sciris as sc
import phcsim as phc

do_plot = False
sc.options(dpi=200)


def test_basic_sim(do_plot=do_plot):
    sc.heading('Testing basic sim')
    sim = phc.Sim(n_agents=10e3)
    sim.init()
    sim.run()
    print(sim.results)
    if do_plot:
        sim.plot()
    return sim


if __name__ == '__main__':

    do_plot = True

    T = sc.timer()

    sim = test_basic_sim(do_plot=do_plot)

    T.toc()
