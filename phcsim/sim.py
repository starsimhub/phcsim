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
