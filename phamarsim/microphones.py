# coding:utf-8
"""Phamarsim - a phased microhpone array simulation library"""

from __future__ import division
# coding:utf-8
"""Microphones for Phamarsim

Microphones translate the plane sound waves in the medium to voltage signals.
They must provide a method

>>> get_voltage_signal(t),

which produces an ndarray of the voltages at the specified times.

"""

from __future__ import division
import numpy as np

import logging
log = logging.getLogger(__name__)

import objects

class Speaker(objects.SimpleObject):
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
        objects.SimpleObject.__init__(self, **kwargs)
        self._source = None
        self._amplification = amplification
        if src is not None:
            self.connect_to_source(src)
    
    def get_pressure_signal(self, t, theta=0.0, phi=0.0):
        """Return the pressure signal for a plane wave in the specified direction.
        
        Parameters
        ----------
        t : array-like
            Times at which the signal signal should be evaluated [s].
        theta : array-like
            The polar angle of the outgoing wave as measurde from the speaker's z-axis [deg].
        phi : array-like
            The azimuthal angle of outgoing wave as measured from the speaker's x-axis [deg].

        Returns
        -------
        p : ndarray
            The pressure signal for the specified direction.

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
