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
            super().init_pre(sim)
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
                rel_mal = row['malnutrition']
            )

        # Store results
        self.df = df
        self.data = data
        return

    def step(self):
        """ Dynamics controlled by HealthSystem and apply_product() """
        pass

    def apply_product(self, product, uids, verbose=True):
        """ Apply the product to the disease for the selected people """
        prod = self.data[product]
        dis = self.sim.diseases
        disease = dis[prod.disease]
        if 'malnutrition' in dis:
            malnourished = dis.malnutrition.malnourished[uids]
        else:
            malnourished = 0.0

        # Calculate product effects
        mal_factor = 1.0 - prod.rel_mal*malnourished
        sus_eff    = 1.0 - prod.rel_sus*mal_factor
        death_eff  = 1.0 - prod.rel_death*mal_factor

        # Apply to the diseases
        if verbose:
            pre_sus = disease.rel_sus[uids].mean()
            pre_death = disease.rel_death[uids].mean()
        disease.rel_sus[uids] *= sus_eff
        disease.rel_death[uids] *= death_eff

        if verbose:
            post_sus = disease.rel_sus[uids].mean()
            post_death = disease.rel_death[uids].mean()
            print(f'DEBUG: t={self.ti} product={product} disease={prod.disease}: p_sus={pre_sus} -> {post_sus}, p_death={pre_death} -> {post_death}')

        # Record doses given
        self[product][uids] = True

        return


class HealthSystem(ss.Module):

    def init_pre(self, sim=None, d=None):
        """ Initialize including the data """
        if sim:
            super().init_pre(sim)
            d = sim.d

        # # Get the data
        # df = d['disease_trajectories']

        # mapping = {
        #     'disease': 'Condition',
        #     'product': 'Preventative intervention',
        #     'rel_death': 'Mortality rate modifier (efficacy)',
        #     'rel_sus': 'Disease rate modifier (efficacy)',
        #     'malnutrition': 'Malnutrition efficacy reduction (multiplier)'
        # }

        # df = sc.dataframe({k:df[v] for k,v in mapping.items()})

        # # Map disease names and product names to internal keys
        # df['disease'] = df['disease'].map(phc.disease_map)
        # df['product'] = df['product'].map(self.label_to_key)

        # # Convert dataframe to dictionary keyed by product
        # data = sc.objdict()
        # for i, row in df.iterrows():
        #     product = row['product']
        #     data[product] = sc.objdict(
        #         disease = row['disease'],
        #         rel_death = row['rel_death'],
        #         rel_sus = row['rel_sus'],
        #         rel_mal = row['malnutrition']
        #     )

        # # Store results
        # self.df = df
        # self.data = data
        return


    def step(self):
        pass