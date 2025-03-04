"""
Define diseases
"""

import numpy as np
import starsim as ss

__all__ = ['Measles', 'Meningitis', 'YellowFever', 'HPV', 'Malnutrition']


class SimpleDisease(ss.Disease):
    """ A simple disease that is applied probabilistically; based on ss.NCD """

    def __init__(self, pars=None, **kwargs):
        super().__init__()
        self.define_pars(
            p_acquire = ss.bernoulli(p=ss.peryear(0.3)), # Probability of acquisition per timestep
            p_death = ss.bernoulli(p=0.1), # Probability of death per infection
        )
        self.update_pars(pars=pars, **kwargs)

        self.define_states(
            ss.State('infected', label='Infected'),
            ss.FloatArr('ti_infected', label='Time of infection'),
            ss.FloatArr('ti_dead', label='Time of death'),
            ss.FloatArr('rel_sus', label='Relative susceptability'),
            ss.FloatArr('rel_death', label='Relative mortality'),
        )
        return

    def init_results(self):
        """
        Initialize results
        """
        super().init_results()
        self.define_results(
            ss.Result('new_infections', dtype=int,   label='Infections'),
            ss.Result('new_deaths',     dtype=int,   label='Deaths'),
            ss.Result('prevalence',     dtype=float, label='Prevalence'),
        )
        return

    def step(self):
        ti = self.ti

        # Infection
        susceptible = (~self.infected).uids
        infections = self.pars.p_acquire.filter(susceptible)
        self.infected[infections] = True
        self.ti_infected[infections] = ti

        # Death
        deaths = self.pars.p_death.filter(infections)
        self.sim.people.request_death(deaths)
        self.ti_dead[deaths] = ti

        # Results
        self.results.new_infections[ti] = len(infections)
        self.results.new_deaths[ti] = len(deaths)
        self.results.prevalence[self.ti] = np.count_nonzero(self.infected)/len(self.sim.people)

        return infections


class Measles(SimpleDisease):
    def __init__(self, pars=None, **kwargs):
        super().__init__()
        self.define_pars( # TODO: load from sheet
            label = 'Measles',
            p_acquire = ss.peryear(0.5),
            p_death = 0.07,
        )
        return


class Meningitis(SimpleDisease):
    def __init__(self, pars=None, **kwargs):
        super().__init__()
        self.define_pars( # TODO: load from sheet
            label = 'Meningitis',
            p_acquire = ss.peryear(0.0005),
            p_death = 0.5,
        )
        return


class YellowFever(SimpleDisease):
    def __init__(self, pars=None, **kwargs):
        super().__init__()
        self.define_pars( # TODO: load from sheet
            label = 'Yellow fever',
            p_acquire = ss.peryear(0.0005),
            p_death = 0.4,
        )
        return


class HPV(SimpleDisease):
    def __init__(self, pars=None, **kwargs):
        super().__init__()
        self.define_pars( # TODO: load from sheet
            label = 'HPV',
            p_acquire = ss.peryear(0.0),
            p_death = 0.0,
        )
        return



class Malnutrition(ss.Module):
    def __init__(self, pars=None, **kwargs):
        super().__init__()
        self.update_pars(pars=pars, **kwargs)
        self.define_states(
            ss.State('malnourished', label='Malnourished', default=ss.bernoulli(p=0.05)), # TODO: load from data
        )
        return

    def step(self):
        """ Malnutrition is static for now """
        pass