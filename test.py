# coding:utf-8

from __future__ import division
import numpy as np
import scipy as sc
from matplotlib import pyplot as plt

import phamarsim as pa

S1 = pa.sources.SineSource()
S2 = pa.sources.SineSource(500, 1.3, 1)

M = pa.simple_mediums.Air(25.0)

O1 = pa.environments.SimpleObject()
O2 = pa.environments.SimpleObject()

E = pa.environments.Environment()

E.add_object(O1)
O2.add_to_environment(E)
print E.get_objects()
E.remove_object(O2)
print E.get_objects()
