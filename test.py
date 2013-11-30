# coding:utf-8

from __future__ import division
import numpy as np
import scipy as sc
from matplotlib import pyplot as plt

import logging
#logging.basicConfig(level='DEBUG')

import phamarsim as pa

S1 = pa.sources.SineSource(440)
S2 = pa.sources.SineSource(500)

Sp1 = pa.speakers.Speaker()
Sp2 = pa.speakers.Speaker()
Sp3 = pa.speakers.Speaker()

Sp1.connect_to_source(S1)
S2.connect_speaker(Sp2)
Sp3.connect_to_source(S1)

M = pa.mediums.SimpleAir(25.0)

E = pa.environments.SimpleEnvironment()
E.set_medium(M)

E.add_objects(S1.get_speakers())
E.add_objects(S2.get_speakers())

Sp1.set_position(-1,0,0)
Sp2.set_position(0,0,0)
Sp3.set_position(1,0,0)

integration_time = 1
sample_frequency = 10000
t = np.linspace(0, integration_time, int(integration_time*sample_frequency))
X = np.linspace(-10, 10, 50)
Y = np.logspace(-1, 1, 50)
XX = np.tile(X, len(Y))
YY = np.repeat(Y, len(X))
PP = []

for x, y in zip(XX, YY):
    print x, y
    p = E.get_pressure_signal(t,x,y,0)
    # Calculate the RMS pressure signal
    PP.append(np.std(p))

fig, ax = plt.subplots()
cont = ax.tricontourf(XX,YY,np.log(PP))
ax.set_aspect('equal')
ax.grid()
fig.colorbar(cont)
fig.show()
raw_input()
