"""
Define health system
"""

import sciris as sc
import starsim as ss
import phcsim as phc

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

        mapping = {
            'disease': 'Condition',
            'product': 'Preventative intervention',
            'rel_death': 'Mortality rate modifier (efficacy)',
            'rel_sus': 'Disease rate modifier (efficacy)',
            'malnutrition': 'Malnutrition efficacy reduction (multiplier)'
        }

        df = sc.dataframe({k:df[v] for k,v in mapping.items()})

        # Map disease names and product names to internal keys
        df['disease'] = df['disease'].map(phc.disease_map)
        df['product'] = df['product'].map(self.label_to_key)

        # Convert dataframe to dictionary keyed by product
        data = sc.objdict()
        for i, row in df.iterrows():
            product = row['product']
            data[product] = sc.objdict(
                disease = row['disease'],
                rel_death = row['rel_death'],
                rel_sus = row['rel_sus'],
                malnutrition = row['malnutrition']
            )

        # Store results
        self.df = df
        self.data = data
        return

    def step(self):
        """ Dynamics controlled by HealthSystem and apply_product() """
        pass

    def apply_product(self, product, uids):
        """ Apply the product to the


class HealthSystem(ss.Module):
    def step(self):
        pass