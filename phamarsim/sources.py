# coding:utf-8
"""Sound sources for Phamarsim"""

from __future__ import division
import numpy as np
import scipy as sc

class SoundSource():
    """Base class for sound sources"""

    def get_sound_pressure(self, t): 
        """Returns the instantaneous pressure signal of the source for each moment t.
        
        The unit of pressure is mPa."""
        return  t * 0.0

class SineSource(SoundSource):
    """Simple sine sound generator"""

    def set_frequency(self, freq):
        self._frequency = freq
    def get_frequency(self):
        return self._frequency

    def set_phase(self, phi):
        self._phase = phi
    def get_phase(self):
        return self._phase

    def set_amplitude(self, amp):
        self._amplitude = amp
    def get_amplitude(self):
        return self._amplitude

    def get_sound_pressure(self, t):
        return self._amplitude * np.sin(2*np.pi*self._frequency*t + self._phase)

    def __init__(self, freq=440.0, amp=1.0, phi = 0.0):
        """Creates a sine wave sound generator with frequency freq in Hz and amp in mPa."""

        self.set_frequency(freq)
        self.set_amplitude(amp)
        self.set_phase(phi)
