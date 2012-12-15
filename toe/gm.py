from __future__ import print_function

import numpy as np
import astropy.units as u
from astropy.constants import si
from bart import _bart, QuadraticLimbDarkening


# YES!
G = si.G.to(u.R_sun ** 3 / (u.M_sun * u.hour ** 2)).value

# Default LDP.
ldp = QuadraticLimbDarkening(10, 0.39, 0.1)


def get_period(star, planet):
    return 2 * np.pi * np.sqrt(planet.a ** 2 / G / star.mass)


def get_duration(star, planet):
    i = np.abs(star.inclination + planet.di)
    T = get_period(star, planet)
    b = planet.a / star.radius / np.tan(i)
    oneplusk = 1 + planet.r / star.radius
    return T * np.arcsin(star.radius / planet.a * np.sqrt(
            oneplusk * oneplusk - b * b) / np.sin(i)) / np.pi


def get_depth(star, planet):
    b = planet.a / star.radius / np.tan(np.abs(star.inclination + planet.di))
    return _bart.ldlc(planet.r / star.radius, ldp.bins, ldp.intensity, b)


class InclinationPrior(object):

    def __init__(self, var):
        self._ivar = 1.0 / var
        self._std = np.sqrt(var)

    def sample(self, size=1):
        return self._std * np.random.randn(size)

    def __call__(self, i):
        return -0.5 * np.sum(i ** 2 * self._ivar) - np.log(self._std)


class PowerLawPrior(object):

    def __init__(self, mn, mx, alpha):
        self.mn = mn
        self.mx = mx
        self.alpha = alpha

    def sample(self, size):
        raise NotImplementedError()

    def __call__(self, x):
        inds = (x < self.mn) * (x > self.mx)
        return 0.0 * inds + self.alpha * np.log(x) * ~inds


def tanh_model(x, x0, w):
    return 0.5 + 0.5 * np.tanh((x - x0) / w)


class SelectionFunction(object):

    def __init__(self):
        pass


class Star(object):

    def __init__(self, flux, radius, mass, inclination):
        self.flux = flux
        self.radius = radius
        self.mass = mass
        self.inclination = inclination


class Planet(object):

    def __init__(self, r, a, di):
        self.r = r
        self.a = a
        self.di = di
