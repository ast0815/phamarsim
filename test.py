# coding:utf-8

from __future__ import division
import numpy as np
import scipy as sc
from matplotlib import pyplot as plt

import logging
#logging.basicConfig(level='DEBUG')

import phamarsim as pa

M = pa.mediums.SimpleAir(25.0)
E = pa.environments.SimpleEnvironment(M)

S = pa.sources.SineSource(4400)
Sp = pa.speakers.Speaker(S)
E.add_object(Sp)

mics = []
for x in np.linspace(-.1, .1, 15):
    mic = pa.microphones.Microphone()
    mic.set_position(x, 0, 0)
    mics.append(mic)

E.add_objects(mics)

integration_time = 0.1
sample_frequency = 50000
t = np.linspace(0, integration_time, int(integration_time*sample_frequency))
X = np.linspace(-1, 1, 30)
Y = np.logspace(-1.3, 0.2, 30)
XX = np.tile(X, len(Y))
YY = np.repeat(Y, len(X))

(x0, y0, z0) = (0.5, 1.2, 0.0)
r0 = np.sqrt(x0**2 + y0**2 + z0**2)
dts = []
c = M.get_speed_of_sound()
for mic in mics:
    x,y,z = mic.get_position()
    Dx = x0-x
    Dy = y0-y
    Dz = z0-z
    r = np.sqrt(Dx**2 + Dy**2 + Dz**2)
    dr = r - r0
    dts.append(dr / c)

print dts

PP = []
PN = []
XX = [x0] + list(XX)
YY = [y0] + list(YY)
XY = zip(XX, YY)
ref = None
refn = None
for x, y in XY:
    Sp.set_position(x,y,0)
    # Calculate the signal
    p = np.zeros_like(t)
    for mic, dt in zip(mics, dts):
        p += mic.get_voltage_signal(t+dt)
    p /= len(mics)
    p = np.std(p)
    pn = p * np.sqrt(x**2 + y**2)
    if ref is None:
        print 'ref', x, y, p, pn
        ref = p
        refn = pn
    p /= ref
    pn /= refn
    PP.append(p)
    PN.append(pn)

fig, ax = plt.subplots()
ax.set_title("Direkt")
cont = ax.tricontourf(XX, YY, np.log10(PP))
ax.plot(x0,y0,'*')
ax.set_aspect('equal')
ax.plot(XX,YY,',k')
#ax.grid()
fig.colorbar(cont)
fig.show()

fig, ax = plt.subplots()
ax.set_title("Abstandskorrigiert")
cont = ax.tricontourf(XX, YY, np.log10(PN))
ax.plot(x0,y0,'*')
ax.set_aspect('equal')
ax.plot(XX,YY,',k')
#ax.grid()
fig.colorbar(cont)
fig.show()
raw_input()
