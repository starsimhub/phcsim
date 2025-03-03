"""
Define births and deaths
"""

import sciris as sc
import starsim as ss

__all__ = ['People', 'Births', 'Deaths']


class People(ss.People):
    pass


def map_data(which, d):

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


class Births(ss.Demographics):
    def init_pre(self, sim=None, d=None):
        if sim:
            super().init_pre(sim)
            d = sim.d
        self.df = map_data('fertility', d)
        return


class Deaths(ss.Demographics):
    def init_pre(self, sim=None, d=None):
        if sim:
            super().init_pre(sim)
            d = sim.d

        self.df = map_data('mortality', d)
        return