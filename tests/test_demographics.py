"""
Test demographics components
"""

import sciris as sc
import phcsim as phc

do_plot=False


def test_data_load():
    sc.heading('Testing data load')
    d = phc.load_data()
    return d


def test_people():
    sc.heading('Testing people')
    d = phc.load_data()
    ppl = phc.People(1000, data=d)
    return ppl


def test_births():
    sc.heading('Testing births')
    d = phc.load_data()
    births = phc.Births()
    births.init_pre(d=d)
    return births


def test_deaths():
    sc.heading('Testing deaths')
    d = phc.load_data()
    deaths = phc.Deaths()
    deaths.init_pre(d=d)
    return deaths


def test_sim(do_plot=do_plot):
    sc.heading('Testing sim')
    sim = phc.Sim(diseases=None, connectors=None)
    sim.init()
    if do_plot:
        sim.people.plot_ages()
    return sim


if __name__ == '__main__':

    do_plot = True

    T = sc.timer()

    d = test_data_load()
    ppl = test_people()
    births = test_births()
    deaths = test_deaths()
    sim = test_sim(do_plot=do_plot)

    T.toc()
