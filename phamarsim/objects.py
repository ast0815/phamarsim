# coding:utf-8
"""Objects for Phamarsim

"""
from __future__ import division
import numpy as np

import warnings
import logging
log = logging.getLogger(__name__)

def cartesian_to_spherical(x, y, z):
    """Convert a set of cartesian coordinates to spherical ones.
    
    Parameters
    ----------
    x : float
        The x-position [m].
    y : float
        The y-position [m].
    z : float
        The z-position [m].

    Returns
    -------
    theta : float
        The polar angle as measured from the z-axis [deg].
    phi : float
        The azimuthal angle as measured from the x-axis [deg].
    r : float
        The distance of the coordinates from the center of the coordinate system [m].

    """
    r = np.sqrt( x**2 + y**2 + z**2 )
    theta = np.arccos(z/r) * 180. / np.pi
    phi = np.arctan2(y, x) * 180. / np.pi

    return theta, phi, r

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
    alpha : float
        The objects rotation around its own z-axis.

    """
    def __init__(self, environment=None, x=None, y=None, z=None, theta=None, phi=None, alpha=None):
        self._x = 0.
        self._y = 0.
        self._z = 0.
        self._theta = 0.
        self._phi = 0.
        self._alpha = 0.
        self.set_position(x,y,z)
        self.set_orientation(theta,phi,alpha)
        self._environment = None
        if environment is not None:
            self.add_to_environment(environment)

    def set_position(self, x=None, y=None, z=None):
        """Set the position of the object.

        Parameters
        ----------
        x : float, optional
            The new x-position of the object [m].
        y : float, optional
            The new y-position of the object [m].
        z : float, optional
            The new z-position of the object [m].

        """
        if x is not None:
            self._x = x
        if y is not None:
            self._y = y
        if z is not None:
            self._z = z

    def set_orientation(self, theta=None, phi=None, alpha=None):
        """Set the orientation of the object.
        
        Parameters
        ----------
        theta : float, optional
            The new polar angle of the object as measured from the z-axis [deg].
        phi : float, optional
            The new azimuthal angle of the object as measured from the x-axis [deg].
        alpha : float, optional
            The objects rotation around its own z-axis.

        """
        if theta is not None:
            self._theta = theta
        if phi is not None:
            self._phi = phi
        if alpha is not None:
            self._alpha = alpha
        
    def get_position(self):
        """Get the position of the object.

        Returns
        ----------
        x : float
            The x-position of the object [m].
        y : float
            The y-position of the object [m].
        z : float
            The z-position of the object [m].

        """
        return np.array( (self._x, self._y, self._z) )

    def get_orientation(self):
        """Get the orientation of the object.

        Returns
        -------
        theta : float
            The polar angle of the object as measured from the z-axis [deg].
        phi : float
            The azimuthal angle of the object as measured from the x-axis [deg].
        alpha : float
            The objects rotation around its own z-axis.

        """
        return self._theta, self._phi, self._alpha
    
    def local_to_global_position(self, x, y, z):
        """Convert the local coordinates `x, y, z` to global coordinates.

        Parameters
        ----------
        x : float
            The x-position in local coordinates [m].
        y : float
            The y-position in local coordinates [m].
        z : float
            The z-position in local coordinates [m].

        Returns
        ----------
        x1 : float
            The x-position in global coordinates [m].
        y1 : float
            The y-position in global coordinates [m].
        z1 : float
            The z-position in global coordinates [m].
        
        """
        # Get objects position and orientation.
        x0, y0, z0 = self.get_position()
        theta, phi, alpha = self.get_orientation()

        # Shortcuts for sine and cosine of the angles:
        st = np.sin(np.pi * theta/180)
        ct = np.cos(np.pi * theta/180)
        sp = np.sin(np.pi * phi/180)
        cp = np.cos(np.pi * phi/180)
        sa = np.sin(np.pi * alpha/180)
        ca = np.cos(np.pi * alpha/180)
        
        # Coordinates as vectors:
        v = np.matrix([[x], [y], [z]])
        v0 = np.matrix([[x0], [y0], [z0]])

        # The rotation matrices:
        # Rotation around the z-axis by alpha
        M1 = np.matrix([[ ca, -sa,  0.],
                        [ sa,  ca,  0.],
                        [ 0.,  0.,  1.]])
        # Rotation around the y-axis by theta
        M2 = np.matrix([[ ct,  0.,  st],
                        [ 0.,  1.,  0.],
                        [-st,  0.,  ct]])
        # Rotation around the z-axis by phi
        M3 = np.matrix([[ cp, -sp,  0.],
                        [ sp,  cp,  0.],
                        [ 0.,  0.,  1.]])

        # Apply rotation and translation.
        v1 = v0 + M3*M2*M1 * v
        
        # Return flattened array of coordinates.
        return v1.A1
    
    def global_to_local_position(self, x, y, z):
        """Convert the global coordinates `x, y, z` to local coordinates.

        Parameters
        ----------
        x : float
            The x-position in global coordinates [m].
        y : float
            The y-position in global coordinates [m].
        z : float
            The z-position in global coordinates [m].

        Returns
        ----------
        x1 : float
            The x-position in local coordinates [m].
        y1 : float
            The y-position in local coordinates [m].
        z1 : float
            The z-position in local coordinates [m].
        
        """
        # Get objects position and orientation.
        x0, y0, z0 = self.get_position()
        theta, phi, alpha = self.get_orientation()

        # Shortcuts for sine and cosine of the angles:
        st = np.sin(np.pi * theta/180)
        ct = np.cos(np.pi * theta/180)
        sp = np.sin(np.pi * phi/180)
        cp = np.cos(np.pi * phi/180)
        sa = np.sin(np.pi * alpha/180)
        ca = np.cos(np.pi * alpha/180)

        # Coordinates as vectors:
        v = np.matrix([[x],
                       [y],
                       [z]])
        v0 = np.matrix([[x0],
                        [y0],
                        [z0]])

        # The inverse rotation matrices:
        # Rotation around the z-axis by alpha
        M1 = np.matrix([[ ca,  sa,  0.],
                        [-sa,  ca,  0.],
                        [ 0.,  0.,  1.]])
        # Rotation around the y-axis by theta
        M2 = np.matrix([[ ct,  0., -st],
                        [ 0.,  1.,  0.],
                        [ st,  0.,  ct]])
        # Rotation around the z-axis by phi
        M3 = np.matrix([[ cp,  sp,  0.],
                        [-sp,  cp,  0.],
                        [ 0.,  0.,  1.]])

        # Apply rotation and translation in reverse.
        v1 = M1*M2*M3 * (v - v0)
        
        # Return flattened array of coordinates.
        return v1.A1


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

