# coding:utf-8
"""Mediums for Phamarsim"""

from __future__ import division
import numpy as np
import scipy as sc

class SimpleMedium():
    """Base class for simple mediums.

    Parameters
    ----------
    c : float, optional
        The speed of sound in the medium in m/s. Defaults to 331.3 m/s.
    
    Notes
    -----
    SimpleMediums only have to provide a constant speed of sound.
    
    """
    def __init__(self, c=331.3):
        self.set_speed_of_sound(c)

    def set_speed_of_sound(self, c):
        self._speed_of_sound = c
    def get_speed_of_sound(self):
        """Returns the speed of sound in the medium."""
        return self._speed_of_sound
    

class SimpleAir(SimpleMedium):
    """Creates a simple medium "dry air".

    Parameters
    ----------
    temp : float, optional
        The medium's temperature in °C. Defaults to 0.0 °C.
    
    Notes
    -----
    The speed of sound in dry air can be approximated with the formula

        c = 331.3 m/s * sqrt(1 + theta/273.15),

    where theta is the temperature in °C.
    This relation is true for all (approximately) ideal gases.
    
    """
    def __init__(self, temp=0.0, **kwargs):
        SimpleMedium.__init__(self, **kwargs)
        self.set_temperature(temp)

    def set_temperature(self, temp):
        """Set the temperature of the gas and thus the speed of sound.
        
        Parameters
        ----------
        temp : float
            The temperature of the medium in °C.
        
        """
        self.set_speed_of_sound(331.3 * np.sqrt(1 + temp/273.15))
