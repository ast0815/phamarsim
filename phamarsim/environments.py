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

import mediums
import speakers

import warnings
import logging
log = logging.getLogger(__name__)

class SimpleObject():
    """Simple point-like objects with a position and orientation in an environment

    Parameters
    ----------
    environment : Environment, optional
        The environment in which the object should be placed.
    x : float, optional
        The x-position of the object [m].
    y : float, optional
        The y-position of the object [m].
    z : float, optional
        The z-position of the object [m].
    theta : float, optional
        The polar angle of the object as measured from the z-axis [deg].
    phi : float, optional
        The azimuthal angle of the object as measured from the x-axis [deg].

    """
    def __init__(self, environment=None, x=None, y=None, z=None, theta=None, phi=None):
        self._x = x
        self._y = y
        self._z = z
        self._theta = theta
        self._phi = phi
        self._environment = None
        if environment is not None:
            self.add_to_environment(environment)

    def set_position(self, x=None, y=None, z=None, theta=None, phi=None):
        """Set position and orientation of the object.

        Parameters
        ----------
        x : float, optional
            The new x-position of the object [m].
        y : float, optional
            The new y-position of the object [m].
        z : float, optional
            The new z-position of the object [m].
        theta : float, optional
            The new polar angle of the object as measured from the z-axis [deg].
        phi : float, optional
            The new azimuthal angle of the object as measured from the x-axis [deg].

        """
        if x is not None:
            self._x = x
        if y is not None:
            self._y = y
        if z is not None:
            self._z = z
        if theta is not None:
            self._theta = theta
        if phi is not None:
            self._phi = phi
        
    def get_postion(self):
        """Get the position and orientation of the object.

        Returns
        ----------
        x : float
            The x-position of the object [m].
        y : float
            The y-position of the object [m].
        z : float
            The z-position of the object [m].
        theta : float
            The polar angle of the object as measured from the z-axis [deg].
        phi : float
            The azimuthal angle of the object as measured from the x-axis [deg].

        """
        return self._x, self._y, self._z, self._theta, self._phi
    
    def get_relative_position(self, obj):
        """Return the position relative to another object.
        
        Parameters
        ----------
        origin : SimpleObject
            The object relative to which the position should be returned.

        Returns
        ----------
        x : float
            The x-position of the object relative to `origin` [m].
        y : float
            The y-position of the object relative to `origin` [m].
        z : float
            The z-position of the object relative to `origin` [m].
        theta : float
            The polar angle of the object as measured from the z-axis of `origin` [deg].
        phi : float
            The azimuthal angle of the object as measured from the x-axis of `origin` [deg].

        
        """

    def get_environment(self):
        """Return the current environment."""
        return self._environment

    def add_to_environment(self, environment):
        """Add the object to an environment.

        Parameters
        ----------
        environment : Environment
            The environment the object should be added to.

        Notes
        -----
        An object can only be present in one environment at the time.
        It will be removed from any previous environments.

        If the object is already part of the environment, a ValueError will be raised.

        """
        if self._environment == environment:
            raise ValueError("The object is already part of the environment.")

        # Remove object from previous environment
        if self._environment is not None:
            self.remove_from_environment(self._environment)
        
        # Add to new environment
        self._environment = environment
        try:
            environment.add_object(self)
        except ValueError:
            # Catch ValueErrors so a mutual addition does not raise an Error.
            pass
        except:
            # The environment was not able to add the object. Reset and raise Error.
            self._environment = None
            raise
        log.debug("%s is now part of %s."%(self, environment))
    
    def remove_from_environment(self, environment):
        """Remove the object from an environment.
        
        Raises ValueError if the object is not part of the environment."""
        if self._environment != environment:
            raise ValueError("The object is not part of the environment.")
        
        self._environment = None
        try:
            environment.remove_object(self)
        except ValueError:
            # Catch ValueErrors so a mutual removal does not raise an Error.
            pass
        log.debug("%s is no longer a part of %s."%(self, environment))

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

    def get_objects(self, typ=SimpleObject):
        """Return a list of all objects in the environment of type typ."""
        return [o for o in self._objects if isinstance(o, typ)]

    def get_plane_waves(self, t, x, y, z):
        warnigns.warn("Tried to get plane waves from the Environment base class.")
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

    def get_medium(self, medium):
        return self._medium

    def get_plane_waves(self, t, x, y, z):
        """Return the local plane waves pressure signals."""

        waves = []
        for spk in self.get_objects(speakers.Speaker):
            
        return

