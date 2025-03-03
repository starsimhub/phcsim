"""
Define births and deaths
"""

import numpy as np
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


class Births(ss.Births):

    def __init__(self, pars=None, scale_factor=1.0, **kwargs):
        super().__init__()
        self.define_pars(
            inherit = False,
            unit = 'month',
            scale_factor = scale_factor
        )
        self.update_pars(pars, **kwargs)
        return

    def init_pre(self, sim=None, d=None):
        """ Initialize including the data """
        if sim:
            ss.Demographics.init_pre(self, sim) # TODO: make more elegant
            d = sim.d

        self.df = map_data('fertility', d)
        return

    def get_births(self, randomize=True):
        """
        Extract the right birth rates to use and translate it into a number of people to add.
        """
        sim = self.sim
        df = self.df
        ages = sim.people.age[sim.people.female] # Get female ages
        age_bins = df.min_age.values.astype(float)
        probs = df.val.values.astype(float)
        probs = sc.cat(probs, 0) # Add an extra zero # TODO: make more elegant
        categories = np.digitize(ages, age_bins)
        age_probs = probs[categories]

        # Final calculation, corrected for time
        factor = ss.time_ratio(unit1=self.t.unit, dt1=self.t.dt, unit2='year', dt2=1.0)
        n_new = age_probs.sum() * factor * self.pars.scale_factor

        if randomize:
            n_new = np.random.poisson(lam=n_new)
        return n_new

    def update_results(self):
        self.results.new[self.ti] = self.n_births
        births_per_year = self.n_births/self.sim.t.dt_year
        denom = self.sim.people.alive.sum()
        self.results.cbr[self.ti] = births_per_year/denom
        return


class Deaths(ss.Deaths): # TODO: use age-specific data

    def __init__(self, pars=None, **kwargs):
        super().__init__()
        self.define_pars(
            unit = 'month',
            rate_units = 1.0,
        )
        self.update_pars(pars, **kwargs)
        return

    def init_pre(self, sim=None, d=None):
        if sim:
            super().init_pre(sim)
            d = sim.d

        df = map_data('mortality', d)

        df_f = sc.dataframe(age=df.min_age, sex='f', value=df.val_f)
        df_m = sc.dataframe(age=df.min_age, sex='m', value=df.val_m)
        self.df = df_f.concat(df_m)
        metadata = dict( # TODO: shouldn't be needed
            data_cols = {'sex':'sex', 'age':'age', 'value':'value'},
            sex_keys = {'f':'f', 'm':'m'},
        )
        death_rate = ss.standardize_data(data=self.df, metadata=metadata)
        death_rate = death_rate.unstack(level='age')
        self.death_rate_data = death_rate

        # self.update_pars(
        # )
        return