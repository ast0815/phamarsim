# coding:utf-8
"""Simple mediums for use in simple environments"""

from __future__ import division
import numpy as np
import scipy as sc

class SimpleMedium():
    """Base class for simple mediums"""

    def set_speed_of_sound(self, c):
        self._speed_of_sound = c
    def get_speed_of_sound(self):
        """Returns the speed of sound in the medium."""
        return self._speed_of_sound
    
    def __init__(self, c):
        """Creates a simple medium with a speed of sound of c m/s."""

        self.set_speed_of_sound(c)

class Air(SimpleMedium):
    """Simple medium: dry air"""

    def __init__(self, temp=25.0):
        """Creates a simple medium "dry air" with temperature temp °C.

        The speed of sound in dry air can be approximated with the formula

            c = 331.3 m/s * sqrt(1 + theta/273.15),

        where theta is the temperature in °C.
        This relation is true for all ideal (approximately) gases.
        """

        self.set_speed_of_sound(331.3 * np.sqrt(1 + temp/273.15))
