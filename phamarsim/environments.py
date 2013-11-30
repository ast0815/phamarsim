# coding:utf-8
"""Environments for Phamarsim

Environments must define the function

>>> get_plane_waves(t,x,y,z)

which returns a representation of the local sound field:

>>> [ (array(t), array(theta), array(phi), array(p)), ( ), ... ]

Each tuple `(t, theta, phi, p)` represents a sound wave that is propagating in
direction theta and phi. Theta and phi do not have to be constant.
The sum over the `p`-arrays of all waves yields the (only time-dependent) pressure
signal at position `x, y, z`. This simpler signal is also returned by the function

>>> get_pressure_signal(t,x,y,z)

which will call `get_plane_waves` internally.

"""
from __future__ import division
import numpy as np

import objects
import mediums
import speakers

import warnings
import logging
log = logging.getLogger(__name__)

class Environment():
    """Base class for environments

    Parameters
    ----------
    objects : iterable, optional
        The objects that should be added to the environment.

    """
    def __init__(self, objects=[]):
        self._objects = []
        self.add_objects(objects)

    def add_objects(self, objects):
        """Add multiple objects at once.

        Parameters
        ----------
        objects : iterable
            An iterable of objects to be added to the environment.

        """
        for obj in objects:
            self.add_object(obj)

    def add_object(self, obj):
        """Add an object to the environment.
        
        Raises a ValueError if the object is already a part of the environment.
        
        """
        if obj in self._objects:
            raise ValueError("The object is already a part of the environment.")

        # Add the object
        self._objects.append(obj)
        try:
            obj.add_to_environment(self)
        except ValueError:
            # Catch ValueErrors so a mutual adding does not raise an error.
            pass
        except:
            # The object could not be added. Reset.
            self._objects.remove(obj)
            raise
        log.debug("%s now includes %s."%(self, obj))

    def remove_object(self, obj):
        """Remove an object from the environment.

        Raises a ValueError if the object is not a part of the environment.

        """
        if obj not in self._objects:
            raise ValueError("The object is no part of the environment.")

        # Remove the object
        self._objects.remove(obj)
        try:
            obj.remove_from_environment(self)
        except ValueError:
            # Don't raise an error on mutual removal.
            pass
        log.debug("%s no longer includes %s."%(self, obj))

    def get_objects(self, typ=objects.SimpleObject):
        """Return a list of all objects in the environment of type typ."""
        return [o for o in self._objects if isinstance(o, typ)]

    def get_plane_waves(self, t, x, y, z):
        warnings.warn("Tried to get plane waves from the Environment base class.")
        return []

    def get_pressure_signal(self, t, x, y, z):
        waves = self.get_plane_waves(t,x,y,z)
        signal = np.zeros_like(t)
        for tt, theta, phi, p in waves:
            signal += p
        return signal

class SimpleEnvironment(Environment):
    """Creates a very simple environment with a homogeneous material and point-like objects.

    Parameters:
    -----------
    medium : SimpleMedium, optional
        The medium of the environment. Defaults to `mediums.SimpleAir()`.
    objects : iterable, optional
        An iterable of the objects that should be added to the environment.

    """
    def __init__(self, medium=mediums.SimpleMedium(), **kwargs):
        Environment.__init__(self, **kwargs)
        self._medium = None
        self.set_medium(medium)

    def set_medium(self, medium):
        self._medium = medium
        log.debug("The medium of %s is now %s."%(self, medium))

    def get_medium(self):
        return self._medium

    def get_plane_waves(self, t, x, y, z):
        """Return the local plane waves pressure signals."""

        waves = []
        dummy = objects.SimpleObject(x=x, y=y, z=z)
        for spk in self.get_objects(speakers.Speaker):
            # Direction of the point in the speaker's coordinate system
            ltheta, lphi, lr = objects.cartesian_to_spherical( *spk.global_to_local_position(x, y, z) )
            # Time delay due to distance to speaker
            Dt = lr / self.get_medium().get_speed_of_sound()
            # Weakened signal due to spherical expansion in space
            p = spk.get_pressure_signal(t - Dt, ltheta, lphi) / lr
            # Direction of the sound wave in global coordinates
            theta, phi, r = objects.cartesian_to_spherical( *(dummy.get_position() - spk.get_position()) )
            # The final wave
            waves.append( (t, theta, phi, p) )

        return waves

