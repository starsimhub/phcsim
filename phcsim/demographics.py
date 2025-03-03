"""
Define births and deaths
"""

import sciris as sc
import starsim as ss

__all__ = ['People', 'Births', 'Deaths']


class People(ss.People):
    def __init__(self, n_agents, data=None, extra_states=None):
        if data is not None:
            if isinstance(data, dict): # Typical use case: use sim.d
                init_pop = data['initial_population']
                data = init_pop.F # TODO: use separate male and female age distributions
        super().__init__(n_agents=n_agents, age_data=data, extra_states=extra_states)
        return


def map_data(which, d):
    """ Map data for births and deaths """

    if d is None:
        errormsg = 'Must supply a sim, or else the data file'
        raise ValueError(errormsg)

    if which == 'fertility':
        df = d['fertility_rates']
        mapping = {
            'min_age': 'Age Start',
            'max_age': 'Age End',
            'val': 'Value',
            'trend': 'Secular Trend',
        }
    elif which == 'mortality':
        df = d['mortality_rates']
        mapping = {
            'min_age': 'Age Start',
            'max_age': 'Age End',
            'val_f': 'Female Value',
            'val_m': 'Male Value',
        }
    else:
        errormsg = f'which must be "fertility" or "mortality", not {which}'
        raise ValueError(errormsg)

    df = sc.dataframe({k:df[v] for k,v in mapping.items()})
    return df


class Births(ss.Births): # TODO: use data

    def init_pre(self, sim=None, d=None):
        super().init_pre(sim=sim)
        if sim:
            super().init_pre(sim)
            d = sim.d

        self.df = map_data('fertility', d)
        return


class Deaths(ss.Deaths): # TODO: use data

    def init_pre(self, sim=None, d=None):
        if sim:
            super().init_pre(sim)
            d = sim.d

        self.df = map_data('mortality', d)
        return