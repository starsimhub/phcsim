"""
Define health system
"""

import starsim as ss

__all__ = ['Products', 'HealthSystem']


class Products(ss.Module):

    def __init__(self, pars=None, **kwargs):
        super().__init__()
        self.define_states(
            ss.BoolArr('mcv_1', label='MCV 1'),
            ss.BoolArr('mcv_2', label='MCV 2'),
            ss.BoolArr('meningitis_vaccine', label='Meningitis vaccine'),
            ss.BoolArr('vitamin_a', label='Vitamin A'),
            ss.BoolArr('hpv_vaccine_1', label='HPV vaccine 1'),
            ss.BoolArr('hpv_vaccine_2', label='HPV vaccine 2'),
            ss.BoolArr('yellow_fever_vaccine', label='Yellow fever vaccine'),
        )
        self.key_to_label = {s.name:s.label for s in self.states}
        self.label_to_key = {v:k for k,v in self.key_to_label.items()}
        self.update_pars(pars=pars, **kwargs)
        return

    def init_pre(self, sim=None, d=None):
        """ Initialize including the data """
        if sim:
            ss.Module.init_pre(self, sim) # TODO: make more elegant
            d = sim.d

        # Get the data
        df = d['disease_trajectories']

        # mapping = {
        #     'min_age': 'Age Start',
        #     'max_age': 'Age End',
        #     'val_f': 'Female Value',
        #     'val_m': 'Male Value',
        # }

        # df = sc.dataframe({k:df[v] for k,v in mapping.items()})

        self.df = df
        return

    def step(self):
        pass


class HealthSystem(ss.Module):
    def step(self):
        pass