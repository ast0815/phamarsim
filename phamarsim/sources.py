# coding:utf-8
"""Sound sources for Phamarsim

Sound sources must define the method

>>> get_sound_signal(t)

which returns the signal of the source for every point in time t [s].

The unit of the signal is 1 and will be translated to soundwaves by a speaker.
It should be centered at 0 and the amplitude should be <= 1.

"""
from __future__ import division
import numpy as np

import warnings
import logging
log = logging.getLogger(__name__)

import speakers

class SoundSource():
    """Base class for sound sources"""

    def __init__(self):
        self._speakers = []

    def get_sound_signal(self, t): 
        warnigns.warn("Tried to get a sound signal from the SoundSource base class.")
        return  t * 0.0

    def connect_speaker(self, speaker):
        """Connect a speaker to the sound source.

        Parameters
        ----------
        speaker : Speaker
            Speaker to connect to the sound source.
        
        Notes
        -----
        Multiple speakers can be connected to a single source.

        Raises ValueError if the speaker is already connected to the source.

        If the speaker is already connected to another sound source, it will be disconnected from it.

        """
        if speaker not in self._speakers:
            self._speakers.append(speaker)
            try:
                speaker.connect_to_source(self)
            except ValueError:
                # Catch ValueErrors so a mutual connect does not raise an Error.
                pass
            except:
                # The speaker was not able to connect. Reset and raise Error.
                self._speakers.remove(speaker)
                raise
        else:
            raise ValueError("Speaker already connected to source")
        log.debug("%s is now connected to %s."%(self, speaker))

    def disconnect_speaker(self, speaker):
        """Disconnect a speaker from the sound source.
        
        Raises ValueError if the speaker is not connected."""
        self._speakers.remove(speaker)
        try:
            speaker.disconnect_from_source(self)
        except ValueError:
            # Catch ValueErrors so a mutual disconnect does not raise an Error.
            pass
        log.debug("%s is now disconnected from %s."%(self, speaker))

    def get_speakers(self, typ=speakers.Speaker):
        """Return all speakers of type typ"""
        return [S for S in self._speakers if isinstance(S, typ)]

class SineSource(SoundSource):
    """Simple sine wave sound generator
    
    Parameters
    ----------
    freq : float, optional
        The frequency in Hz.
    amp : float, optional
        The amplitude of the signal.
    phi : float, optional
        The phase of the signal [rad].
    
    Notes
    -----
    The signal will be
    
        signal = amp * sin(2*pi*freq*t + phi).

    """
    def __init__(self, freq=440.0, amp=1.0, phi = 0.0):
        SoundSource.__init__(self)
        self.set_frequency(freq)
        self.set_amplitude(amp)
        self.set_phase(phi)

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

    def get_sound_signal(self, t):
        return self.get_amplitude() * np.sin(2*np.pi*self.get_frequency()*t + self._phase)

