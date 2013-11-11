# coding:utf-8
"""Speakers for Phamarsim

Speakers translate the signal of a SoundSource to (direction dependent) plane
sound waves.  They must provide a method

>>> get_wave(t, theta, phi),

which produces an ndarray of the wave form in the specified direction. Theta
and phi are to be interpreted as relative to the speaker, *not* as absolute
angles in the environment. The units of t, theta and phi are s, deg and deg
respectively.

Since all speakers are assumed to be point like, the waveform will be
attenuated with 1/r, where r is the distance in metres. This means that the
unit of the plane wave is mPa * m.

Another way to look at it is that get_wave() produces the pressure signal [mPa]
that would be measured 1 m away from the speaker in the direction specified by
theta and phi, albeit ignoring the time delay.

According to Wikipedia, a normal conversation has a sound pressure of 2~20 mPa.

"""

from __future__ import division
import numpy as np

import logging
log = logging.getLogger(__name__)

import environments as environments

class Speaker(environments.SimpleObject):
    """Base class for speakers
    
    Parameters
    ----------
    src : SoundSource, optional
        A SoundSource the speaker will connected to.
    amplification : SoundSource, optional
        Amplification factor for the translation of sound signals to sound pressure.
        Unit: mPa * m
    kwargs : dictionary
        Will be passed to the `SimpleObject` constructor.
    
    """
    def __init__(self, src=None, amplification=1.0, **kwargs):
        environments.SimpleObject.__init__(self, **kwargs)
        self._source = None
        self._amplification = amplification
        if src is not None:
            self.connect_to_source(src)
    
    def get_sound_wave(self, t, theta=0.0, phi=0.0):
        """Return plane wave signal in the specified direction.
        
        Parameters
        ----------
        t : float
            Times at which the signal signal should be evaluated [s].
        theta : float
            The polar angle of the outgoing wave as measurde from the speaker's z-axis [deg].
        phi : float
            The azimuthal angle of outgoing wave as measured from the speaker's x-axis [deg].
        
        Notes
        -----

        This simple speaker emulates an isotropic sound source with the same
        gain in all directions, so the signal is independent of the chosen
        theta and phi.
        
        """
        return self.get_source().get_sound_signal(t) * self.get_amplification()
    
    def set_amplification(self, amplification):
        self._amplification = amplification

    def get_amplification(self):
        return self._amplification

    def connect_to_source(self, src):
        """Connect the speaker to a sound source.

        Parameters
        ----------
        src : SoundSource
            The sound source the speaker should be connected with.
        
        Notes
        -----
        Speakers can only be connected to a single source.
        If the speaker is already connected to another sound source, it will be
        disconnected from it.

        Raises ValueError if the speaker is already connected to the source.

        """
        if src == self._source:
            raise ValueError("The speaker is alread connected to the source.")

        # Disconnect from possible old source.
        if self._source is not None:
            self.disconnect_from_source(self._source)

        # Connect new source
        self._source = src
        try:
            src.connect_speaker(self)
        except ValueError:
            # Catch ValueErrors so a mutual connect does not raise an Error.
            pass
        except:
            # The speaker was not able to connect. Reset and raise Error.
            self._source = None
            raise
        log.debug("%s is now connected to %s."%(self, src))

    def disconnect_from_source(self, src):
        """Disconnect the speaker from a sound source.
        
        Raises ValueError if the source is not connected.
        
        """
        if self._source != src:
            raise ValueError("The source is not connected to the speaker.")

        self._source = None
        try:
            src.disconnect_speaker(self)
        except ValueError:
            # Catch ValueErrors so a mutual disconnect does not raise an Error.
            pass
        log.debug("%s is now disconnected from %s."%(self, src))

    def get_source(self):
        return self._source
