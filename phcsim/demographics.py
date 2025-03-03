"""
Define births and deaths
"""

import starsim as ss

__all__ = ['Births', 'Deaths']

class Births(ss.Demographics):

    def init_pre(self, sim=None, d=None):
        if sim:
            super().init_pre(sim)
            d = sim.d
        if d is None:
            errormsg = 'Must supply a sim, or else the data file'
            raise ValueError(errormsg)
        df = d['fertility_mortality_rates']
        df = df[df.Type=='Fertility' & df.Sex=='F']
        df = df.rename(columns={'Age Start':'min_age', 'Age End':'max_age', 'Initial Value':'val', 'Secular Trend':'trend'})
        self.df = df
        return



class Deaths(ss.Demographics):
    pass