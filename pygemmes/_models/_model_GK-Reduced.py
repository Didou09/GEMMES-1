# -*- coding: utf-8 -*-
"""
ABSTRACT: This is a 3 sector model : bank, household, and production.
* Everything is stock-flow consistent, but capital is not created by real products
* The model is driven by offer
* Negociation by philips is impacted by the profit
* Loans from banks are limited by solvability
TYPICAL BEHAVIOR : convergent oscillation around a solow point / debt crisis
LINKTOARTICLE : Goodwin, Richard, 1967. ‘A growth cycle’, in:
    Carl Feinstein, editor, Socialism, capitalism
    and economic growth. Cambridge, UK: Cambridge University Press.
Created on Wed Jul 21 15:11:15 2021
@author: Paul Valcke
"""

import numpy as np

# ---------------------------
# user-defined function order (optional)


_FUNC_ORDER = None


# ---------------------------
# user-defined model
# contains parameters and functions of various types


_LOGICS = {
    'ode': {
        'lambda': {
            'func': lambda itself=0, g=0, alpha=0, beta=0: itself * (g - alpha - beta),
            'com': 'reduced 2variables dynamical expression'
        },
        'omega': {
            'func': lambda itself=0, phillips=0, i=0, gamma=0: itself * phillips - (0.5)*i,
            'com': 'reduced 2variables dynamical expression',
            # 'initial': 0.8,
        },
        'd': {
            'func': lambda itself =0, kappa=0, pi=0, g=0, i=0: kappa - pi - itself*(g+i),
            'com': 'no solvability in loans'
        }
    },
    'statevar': {
        'phillips': {
            'func': lambda phi0=0, phi1=0, lamb=0: (-phi0 + phi1 / (1 - lamb)**2),
            'com': 'salary negociation on employement and profit',
        },
        'g': {
            'func': lambda kappa=0, nu=1, delta=0: kappa / nu - delta,
            'com': 'Goodwin explicit Growth',
        },
        'pi': {
            'func': lambda omega=0, r=0, d=0: 1. - omega - r * d,
            'com': 'Goodwin relative profit',
        },
        'kappa': {
            'func': lambda k0=0, k1=0, k2=0, pi=0, solvability=0: (k0 + k1 * np.exp(k2 * pi))*solvability,
            'com': 'Relative GDP investment through relative profit',
        },
        'solvability': {
            'func': lambda d=0, nu=1, zsolv=0: 1,  # (1-d/nu)**zsolv,
            'com': 'loan dampening if non solvable',
        },
        'i': {
            'func': lambda mu=0, eta=0, omega=0: eta*(mu*omega-1),
            'com': 'Markup dynamics',
        },
    },
}


# ---------------------------
# List of presets for specific interesting simulations

_PRESETS = {'default': {
    'fields': {
        'lambda': 0.95,
        'omega': 0.85,
        'd': 2,
        'alpha': 0.02,
        'beta': 0.025,
        'nu': 3,
        'delta': .005,
        'phinull': .04,
        'k0': -0.0065,
        'k1': np.exp(-5),
        'k2': 20,
        'r': 0.03, },
    'com': ' Default run'},
}
