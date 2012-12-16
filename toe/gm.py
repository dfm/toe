from __future__ import print_function

import numpy as np
import astropy.units as u
from astropy.constants import si
from bart import _bart, QuadraticLimbDarkening


# YES!
G = si.G.to(u.R_sun ** 3 / (u.M_sun * u.hour ** 2)).value

# Default LDP.
ldp = QuadraticLimbDarkening(10, 0.39, 0.1)


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

    def __init__(self, t0, tw, f0, fw):
        self.t0, self.tw = t0, tw
        self.f0, self.fw = f0, fw

    def __call__(self, dt, df):
        return tanh_model(dt, self.t0, self.tw) \
                * tanh_model(df, self.f0, self.fw)


class Star(object):

    def __init__(self, flux, radius, mass, logg, inclination):
        self.flux = flux
        self.radius = radius
        self.mass = mass
        self.inclination = inclination

    @property
    def mass(self):
        g = 10 ** (self.logg - 2)
        r = self.radius * si.R_sun.value
        return g * r * r / si.G.value / si.M_sun.value


class Planet(object):

    def __init__(self, r, a, di, star):
        self.r = r
        self.a = a
        self.di = di
        self.star = star

    @property
    def period(self):
        return 2 * np.pi * np.sqrt(self.a ** 2 / G / self.star.mass)

    @property
    def duration(self):
        star = self.star
        i = np.abs(star.inclination + self.di)
        T = self.period
        b = self.a / star.radius / np.tan(i)
        oneplusk = 1 + self.r / star.radius
        return T * np.arcsin(star.radius / self.a * np.sqrt(
                oneplusk * oneplusk - b * b) / np.sin(i)) / np.pi

    @property
    def depth(self):
        star = self.star
        b = self.a / star.radius / np.tan(np.abs(star.inclination + self.di))
        return _bart.ldlc(self.r / star.radius, ldp.bins, ldp.intensity, b)


class TransitFit(object):

    def __init__(self, selection, a_prior, di_prior, star, dt_data, df_data):
        self.selection = selection
        self.a_prior = a_prior
        self.di_prior = di_prior
        self.star = star
        self.dt_data = dt_data
        self.df_data = df_data

    def __call__(self, p):
        r, a, di = p
        planet = Planet(r, a, di, self.star)

        dt, df = planet.duration, planet.depth * self.star.flux
        s = self.selection(dt, df)
        if s == 0:
            return -np.inf

        ap = self.a_prior(self.a)
        if np.isinf(ap):
            return -np.inf

        ip = self.di_prior(self.di)
        if np.isinf(ip):
            return -np.inf

        lnlike = -0.5 * (self.dt_data[0] - dt) ** 2 * self.dt_data[1]
        lnlike += -0.5 * (self.df_data[0] - df) ** 2 * self.df_data[1]

        return lnlike + np.log(s) + ap + ip

    def sample(self):
        pass
