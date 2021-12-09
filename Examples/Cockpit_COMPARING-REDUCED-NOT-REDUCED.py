# -*- coding: utf-8 -*-
'''
THIS COCKPIT ALLOW ONE TO TEST IF HIS MODEL IS GIVING BACK
'''

import imageio
import cv2
import os
import numpy as np

import pygemmes as pgm
from pygemmes import _plots as plots
import matplotlib.pyplot as plt


# SOLVER ####################################################################
dsolvers = pgm.get_available_solvers(
    returnas=dict, verb=False,
)
# _SOLVER = 'eRK4-homemade'  # (One we created by ourself, that we can tweak)
# _SOLVER = 'eRK2-scipy'  # (an Runge Kutta solver of order 2)
_SOLVER = 'eRK4-scipy'  # (an Runge Kutta solver of order 4)
# _SOLVER = 'eRK8-scipy'  # (an Runge Kutta solver of order 8)


### MODELS LIST ##############################################################
dmodels = pgm.get_available_models(
    returnas=dict, details=False, verb=False,
)

_MODEL = 'GK'
_MODEL_REDUCED = _MODEL+"-Reduced"


Basefields = {
    'dt': 0.01,
    'a': 1,
    'N': 1,
    'K': 2.9,
    'w': .85*1.2,
    'alpha': 0.02,
    'n': 0.025,
    'nu': 3,
    'delta': .005,
    'k0': -0.0065,
    'k1': np.exp(-5),
    'k2': 20,
    'r': 0.03,
    'p': 1.3,
    'eta': 0.1,
    'gammai': 0.5,
}

_DPRESET = {'default': {
    'fields': Basefields,
    'com': '',
    'plots': [],
},
}


# %% LOADING AND COPYING MODELS #############################################

preset = 'default'

hub = pgm.Hub(_MODEL, preset='default', dpresets=_DPRESET, verb=False)
hub_reduced = pgm.Hub(_MODEL_REDUCED, verb=False)

hub.set_dparam(key='p', value=10)
# COPY OF THE PARAMETERS INTO A NEW DICTIONNARY
FieldToLoad = hub_reduced.get_dparam(returnas=dict, eqtype=[None, 'ode'],
                                     group=('Numerical',),)
R = hub.get_dparam(returnas=dict)
tdic = {}
for k, v in FieldToLoad.items():
    val = R[k]['value']
    if 'initial' in v.keys():
        tdic[k] = val[0][0]
    else:
        tdic[k] = val

_DPRESETS = {'Copy'+_MODEL: {'fields': tdic, }, }

# LOADING THE MODEL WITH A NEW MODEL
hub_reduced = pgm.Hub(_MODEL_REDUCED, preset='Copy'+_MODEL,
                      dpresets=_DPRESETS)

# RUNS
hub_reduced.run(verb=0, solver=_SOLVER)
hub.run(verb=0, solver=_SOLVER)
hub.plot()
hub.get_summary()
# PLOTS
R = hub.get_dparam(returnas=dict)
Rr = hub_reduced.get_dparam(returnas=dict)

Tocompare = ['lambda', 'omega', 'd',
             'phillips', 'kappa', 'pi', 'g']

plt.figure()
for i, k in enumerate(Tocompare):
    plt.subplot(4, 2, i+1)
    plt.plot(R['time']['value'], R[k]['value'], label='Full')
    plt.plot(Rr['time']['value'], Rr[k]['value'], ls='--', label='Reduced')
    plt.ylabel(k)
plt.legend()
plt.suptitle('Comparison model GK Full and Reduced')
plt.show()


Tocompare = ['lambda', 'omega',
             'phillips', 'pi', 'g']

# TRAJECTORIES-TIME

plt.figure('TimeTrajectories')
for i, k in enumerate(Tocompare):
    plt.subplot(4, 2, i+1)
    plt.plot(R['time']['value'], R[k]['value'], label='Full')
    plt.plot(Rr['time']['value'], Rr[k]['value'], ls='--', label='Reduced')
    plt.ylabel(k)
plt.suptitle('Comparison model GK Full and Reduced')
plt.show()

# TRAJECTORIES - PHASESPACE
Listphasespace = [['omega', 'lambda'],
                  ['lambda', 'd'],
                  ['omega', 'd'],
                  ['kappa', 'pi'],
                  ['omega', 'inflation'],
                  ['pi', 'd'], ]

plt.figure('Phasespace')
for i, k in enumerate(Listphasespace):
    # lambda-omega
    plt.subplot(3, 2, i+1)

    plt.plot(R[k[0]]['value'], R[k[1]]['value'], label='Full')
    plt.plot(Rr[k[0]]['value'], Rr[k[1]]['value'], ls='--', label='Reduced')
    plt.xlabel(k[0])
    plt.ylabel(k[1])
plt.suptitle('Comparison model GK Full and Reduced')
# plt.axis('scaled')
plt.show()

# %%
hub.get_summary()
print(100*'###')
hub_reduced.get_summary()

# COMPARING GK WITH ITS OWN REDUCED VARIABLES
omegap = np.gradient(R['omega']['value'][:, 0])
omegapp = np.gradient(omegap)
lambdap = np.gradient(R['lambda']['value'][:, 0])
lambdapp = np.gradient(lambdap)


omegaptheo = np.array(R['omega']['value']*(R['phillips']
                      ['value'] - R['alpha']['value']))[:, 0]
lambdaptheo = np.array(R['lambda']['value'] * (R['g']
                       ['value'] - R['alpha']['value'] - R['n']['value']))[:, 0]
gtheo = np.array((1-R['omega']['value']) / R['nu']
                 ['value'] - R['delta']['value'])[:, 0]
gp = np.gradient(R['g']['value'][:, 0])

plt.figure('compare theo')
ax1 = plt.subplot(121)
ax12 = plt.twinx(ax1)
ax1.plot(R['time']['value'], (omegap-omegaptheo), c='b')
ax12.plot(R['time']['value'], omegapp, c='k', ls='--')
ax1.set_ylabel('omegap effective - theo')
ax12.set_ylabel('omegapp')
ax1.set_xlabel('t')

ax2 = plt.subplot(122)
ax22 = plt.twinx(ax2)
ax2.plot(R['time']['value'], (lambdap-lambdaptheo), c='b')
ax22.plot(R['time']['value'], lambdapp, c='k', ls='--')
ax2.set_ylabel('lambdap effective - theo')
ax2.set_ylabel('lambdapp')
ax2.set_xlabel('t')

plt.show()
