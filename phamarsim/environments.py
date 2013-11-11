# coding:utf-8
"""Environments for Phamarsim"""

from __future__ import division
import numpy as np

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
        for obj in objects:
            self.add_object(obj)

    def add_objects(self, objs):
        """Add multiple objects at once.

        Parameters
        ----------
        objs : list
            A list of objects to be added to the environment.

        """
        for obj in objs:
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
