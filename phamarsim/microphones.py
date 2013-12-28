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

class Microphone(objects.SimpleObject):
    """Base class for microphones
    
    Parameters
    ----------
    digitzer : SoundSource, optional
        A Digitizer the microphone will connected to.
    amplification : float, optional
        Amplification factor for the translation of sound pressure.
        This is only a general amplification factor and can be modulated by
        the microphones spatial or temporal characterisitcs.
        Unit: V/mPa
    kwargs : dictionary
        Will be passed to the `SimpleObject` constructor.
    
    """
    def __init__(self, digitizer=None, amplification=1.0, **kwargs):
        objects.SimpleObject.__init__(self, **kwargs)
        self._digitizer = None
        self._amplification = amplification
        if digitizer is not None:
            self.connect_to_digitizer(digitizer)
    
    def get_voltage_signal(self, t):
        """Return the voltage signal at the specified times.
        
        Parameters
        ----------
        t : array-like
            Times at which the signal signal should be evaluated [s].

        Returns
        -------
        U : ndarray
            The voltage signal [V].

        Notes
        -----
        This simple microphone is isotropic with the same gain in all directions.
        
        """
        x,y,z = self.get_position()
        return self.get_environment().get_pressure_signal(t, x,y,z) * self.get_amplification()
    
    def set_amplification(self, amplification):
        self._amplification = amplification

    def get_amplification(self):
        return self._amplification

    def connect_to_digitizer(self, digitizer):
        """Connect the microphone to a digitizer.

        Parameters
        ----------
        digitizer : Digitizer
            The digitzer the microphone should be connected with.
        
        Notes
        -----
        Microphones can only be connected to a single digitizer.
        If the microphone is already connected to another digitizer,
        it will be disconnected from it.

        Raises ValueError if the microphone is already connected to the digitizer.

        """
        if digitizer == self._digitizer:
            raise ValueError("The microphone is alread connected to the digitizer.")

        # Disconnect from possible old source.
        if self._digitizer is not None:
            self.disconnect_from_digitizer(self._digitizer)

        # Connect new source
        self._digitizer = digitizer
        try:
            digitizer.connect_microphone(self)
        except ValueError:
            # Catch ValueErrors so a mutual connect does not raise an Error.
            pass
        except:
            # The speaker was not able to connect. Reset and raise Error.
            self._digitizer = None
            raise
        log.debug("%s is now connected to %s."%(self, digitizer))

    def disconnect_from_digitizer(self, digitizer):
        """Disconnect the microphone from a digitzer.
        
        Raises ValueError if the digitizer is not connected.
        
        """
        if self._digitizer != digitizer:
            raise ValueError("The source is not connected to the speaker.")

        self._digitizer = None
        try:
            digitizer.disconnect_microphone(self)
        except ValueError:
            # Catch ValueErrors so a mutual disconnect does not raise an Error.
            pass
        log.debug("%s is now disconnected from %s."%(self, digitizer))

    def get_digitizer(self):
        return self._digitizer
