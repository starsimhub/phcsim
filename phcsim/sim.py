"""
Customization of Starsim Sim object
"""

import sciris as sc
import starsim as ss
import phcsim as phc

class Sim(ss.Sim):
    def __init__(self, path=None, demographics='default', diseases='default', connectors='default', **kw):
        kw = sc.objdict()
        self.path = path
        self.d = phc.load_data(path)
        df = self.d['model_pars']
        keys = df.Parameter
        vals = df.Value
        data_pars = {k:v for k,v in zip(keys, vals)}
        pars = dict(
            start = ss.date(data_pars['Start year']),
            stop = ss.date(data_pars['End year']),
            unit = data_pars['Time unit'],
        )
        kw.update(pars)
        if demographics == 'default':
            kw.demographics = [phc.Births(), phc.Deaths()]
        if diseases == 'default':
            kw.diseases = [phc.Malnutrition(), phc.Measles(), phc.Meningitis(), phc.YellowFever()]
        if connectors == 'default':
            kw.connectors = [phc.Vaccines(), phc.HealthSystem()]
        super().__init__(**kw)
        return

    def init_people(self, verbose=None, **kwargs):
        """
        Initialize people within the sim
        Sometimes the people are provided, in which case this just adds a few sim properties to them.
        Other time people are not provided and this method makes them.

        Args:
            kwargs  (dict): passed to phc.People()
        """
        # Handle inputs
        people = self.pars.pop('people')

        # If people have not been supplied, make them -- typical use case
        if people is None:
            n_agents = self.pars.n_agents
            labelstr = f' "{self.label}"' if self.label else ''
            print(f'Initializing sim{labelstr} with {n_agents:0n} agents')
            people = phc.People(n_agents=n_agents, data=self.d, **kwargs)  # This just assigns UIDs and length

        # Finish up (NB: the People object is not yet initialized)
        self.people = people
        self.people.link_sim(self)
        return self.people
