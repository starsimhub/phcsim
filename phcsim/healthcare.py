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

    def apply_product(self, product, uids, verbose=False):
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

    def __init__(self, pars=None, *args, **kwargs):
        super().__init__()
        self.define_pars( # TODO: load from sheet
            operational = True,
            p_epi1 = ss.bernoulli(0.5),
            p_epi2 = ss.bernoulli(0.6),
            p_epi3 = ss.bernoulli(0.5),
            p_epi4 = ss.bernoulli(0.5),
            p_epi5 = ss.bernoulli(0.6),
            p_epi6 = ss.bernoulli(0.3),
        )
        self.define_states(
            ss.BoolArr('epi1'),
            ss.BoolArr('epi2'),
            ss.BoolArr('epi3'),
            ss.BoolArr('epi4'),
            ss.BoolArr('epi5'),
            ss.BoolArr('epi6'),
        )
        self.product_map = sc.objdict(
            epi1 = ['vitamin_a'],
            epi2 = ['mcv_1', 'yellow_fever_vaccine', 'meningitis_vaccine'],
            epi3 = ['vitamin_a'],
            epi4 = ['mcv_2'],
            epi5 = ['hpv_vaccine_1'],
            epi6 = ['hpv_vaccine_2'],
        )
        self.epi_keys = self.product_map.keys()
        self.update_pars(pars=pars, **kwargs)
        return

    def init_pre(self, sim=None, d=None):
        """ Initialize including the data """
        if sim:
            super().init_pre(sim)
            d = sim.d

        # Get the data
        self.df = d['need_and_demand_routine']
        self.products = sim.connectors.products # Create a link to make this easier
        return

    def step(self, verbose=False):
        if self.pars.operational:
            for epi_key in self.epi_keys:
                p_key = f'p_{epi_key}'
                eligible = (~self[epi_key]).uids
                if len(eligible):
                    self[epi_key][eligible] = True
                    prob = self.pars[p_key]
                    received = prob.filter(eligible)
                    if len(received):
                        for product in self.product_map[epi_key]:
                            self.products.apply_product(product, received)
                            if verbose:
                                print(f'DEBUG: t={self.ti} epi={epi_key} product={product} received={len(received)}')
        return
