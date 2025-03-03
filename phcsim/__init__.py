"""
Import all PHCsim modules
"""

from .version import __version__, __versiondate__, __license__
from .data import *
from .demographics import *
from .diseases import *
from .healthcare import *
from .sim import *

# Assign the root folder
import sciris as sc
root = sc.thispath(__file__).parent
del sc # Don't keep this in the module