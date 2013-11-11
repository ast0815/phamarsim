# coding:utf-8

from __future__ import division
import numpy as np
import scipy as sc
from matplotlib import pyplot as plt

import logging
logging.basicConfig(level='DEBUG')

import phamarsim as pa

S1 = pa.sources.SineSource()
S2 = pa.sources.SineSource(500, 1.3, 1)

Sp1 = pa.speakers.Speaker()
Sp2 = pa.speakers.Speaker()
Sp3 = pa.speakers.Speaker()

Sp1.connect_to_source(S1)
S2.connect_speaker(Sp2)
Sp3.connect_to_source(S1)

Sp3.connect_to_source(S2)

M = pa.simple_mediums.Air(25.0)

O1 = pa.environments.SimpleObject()
O2 = pa.environments.SimpleObject()

E = pa.environments.Environment()

E.add_object(O1)
O2.add_to_environment(E)
E.add_objects(S1.get_speakers())
E.add_objects(S2.get_speakers())

t = np.linspace(0, 1/200, 50)
fig, ax = plt.subplots(1,1)
for S in [S1, S2]:
    ax.plot(t, S.get_sound_signal(t))
fig.show()
raw_input("Hit Enter.")
fig, ax = plt.subplots(1,1)
for S in E.get_objects(pa.speakers.Speaker):
    ax.plot(t, S.get_sound_wave(t, 0.0, 0.0))
fig.show()
raw_input("Hit Enter.")

