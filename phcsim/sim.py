"""
Customization of Starsim Sim object
"""

import starsim as ss
import phcsim as phc

class Sim(ss.Sim):
    def __init__(self, path=None, demographics='default', diseases='default', connectors='default', **kwargs):
        self.path = path
        self.d = phc.load_data(path)
        if demographics == 'default':
            demographics = [phc.Births(), phc.Deaths()]
        if diseases == 'default':
            diseases = [phc.Measles(), phc.Meningitis(), phc.YellowFever(), phc.HPV()]
        if connectors == 'default':
            connectors = [phc.Vaccines(), phc.HealthSystem()]
        super().__init__(**kwargs)
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
