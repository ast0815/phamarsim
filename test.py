# coding:utf-8

from __future__ import division
import numpy as np
import scipy as sc
from matplotlib import pyplot as plt

import phamarsim as pa

S1 = pa.sources.SineSource()
S2 = pa.sources.SineSource(500, 1.3, 1)

M = pa.simple_mediums.Air(25.0)
print M.get_speed_of_sound()

fig, ax = plt.subplots(1,1)
t = np.linspace(0, 1/200, 50)
p = S1.get_sound_pressure(t)
ax.plot(t, p)
p = S2.get_sound_pressure(t)
ax.plot(t, p)
fig.show()
raw_input()
