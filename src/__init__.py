from .pypol import *
from .tests import test_pypol

runtests = test_pypol.run

ONE = monomial()
TWO = monomial(2)
THREE = monomial(3)