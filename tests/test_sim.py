"""
Test full sim
"""

import sciris as sc
import starsim as ss
import phcsim as phc

do_plot = False


def test_basic_sim(do_plot=do_plot):
    sc.heading('Testing basic sim')
    sim = phc.Sim(n_agents=10e3)
    sim.init()

    sim.run()
    print(sim.results)
    if do_plot:
        sim.plot()
    return sim


def test_multisim(do_plot=do_plot):
    kw = dict(n_agents=10e3)
    s1 = phc.Sim(label='With health system', **kw).init()
    s2 = phc.Sim(label='No health system', **kw).init()
    s2.connectors.healthsystem.pars.operational = False
    msim = ss.parallel(s1, s2)
    if do_plot:
        msim.plot()
    return msim


if __name__ == '__main__':

    do_plot = True

    T = sc.timer()

    sim = test_basic_sim(do_plot=do_plot)
    msim = test_multisim(do_plot=do_plot)

    T.toc()
