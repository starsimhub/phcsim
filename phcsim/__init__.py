"""
Import all PHCsim modules
"""

def root():
    """ Return the root folder of the PHCsim package """
    import sciris as sc
    return sc.thispath(__file__).parent

from .version import __version__, __versiondate__, __license__
from .utils import *
from .demographics import *
from .diseases import *
from .healthcare import *
from .sim import *