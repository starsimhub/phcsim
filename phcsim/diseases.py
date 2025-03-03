"""
Define diseases
"""

import starsim as ss

__all__ = ['Measles', 'Meningitis', 'YellowFever', 'HPV', 'Malnutrition']


class SimpleDisease(ss.Disease):
    """ A simple disease that is applied probabilistically """
    def init_pre(self, sim=None, d=None):
        """ Initialize including the data """
        if sim:
            super().init_pre(sim)
            d = sim.d

        self.df = map_data('fertility', d)
        return
    pass


class Measles(SimpleDisease):
    pass


class Meningitis(SimpleDisease):
    pass


class YellowFever(SimpleDisease):
    pass


class HPV(SimpleDisease):
    pass


class Malnutrition(SimpleDisease):
    pass