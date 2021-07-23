# -*- coding: utf-8 -*-
import _core
import matplotlib.pyplot as plt
### Get the list of models already existing 

import models._def_fields_NEWFORMALISM as dfields 

# DESCRIPTIONS ################################################################
dfields.print_fields(value=False,
                     com=True,
                     unit=False,
                     group=False) # DESCRIBE ALL FIELDS

_core._class_checks.models.describe_available_models()  # DESCRIBE ALL MODELS

# LIST OF POSSIBILITES FOR THE SOLVER #########################################
Solvers = [         # list of existing solver 
    'eRK4-homemade', 
    'eRK2-scipy',
    'eRK4-scipy',
    'eRK8-scipy',
          ]
verb = [ 
    0,             # no verbose 
    1,             # verbose with flush at each iteration (NOT FOR IDE) 
    2,             # verbose with no flush at each iteration (NOT FOR IDE) 
    .5,            # When float, verbose at every verb seconds (.5 : 2 time per second) 
       ]

ListOfModels = _core._class_checks.models.get_available_models(returnas=list)

### THE LOOP FOR V1 THAT HAS TO WORK WELL
"""
for NameOfTheModel in ListOfModels :
    sol = _core.Hub(NameOfTheModel)
    PRESETS = []
    for preset in PRESETS :
        sol = _core.Hub(NameOfTheModel)
        
        #sol.load_preset(preset)
        
        sol.load_field({'a' : 1})
        sol.load_field({'a' : [1,2,'lin']})
        sol.load_field({'a' : [1,2,'log'],
                        'alpha' : 0.03})
        sol.load_field({'nx': 100})   
        sol.load_field({'a': [1,2,3]}) 
        
        sol.get_summary()
        sol.run(solver='eRK4-homemade', verb=1.1)
        
        sol.getCycleAnalysis(key='lambda')
        sol.getCycleAnalysis(key=False)
        
        Result = sol.get_dparam(returnas=dict)
                
        plt.figure()
        plt.subplot(211);plt.plot(Result['time']['value'],Result['omega']['value']);plt.ylabel('Omega')
        plt.subplot(212);plt.plot(Result['time']['value'],Result['lambda']['value']);plt.ylabel('Lambda')
        plt.suptitle(NameOfTheModel+' '+preset)
        plt.show()
"""


# #############################################################################
NameOfTheModel = 'G_Reduced'
sol = _core.Hub(NameOfTheModel)
sol.get_summary()
sol.run(verb=0)

Result = sol.get_dparam(returnas=dict)
#

plt.figure()
plt.subplot(211);plt.plot(Result['time']['value'],Result['omega']['value']);plt.ylabel('Omega')
plt.subplot(212);plt.plot(Result['time']['value'],Result['lambda']['value']);plt.ylabel('Lambda')
plt.suptitle(NameOfTheModel)
plt.show()

# #############################################################################
NameOfTheModel = 'GK'
sol = _core.Hub(NameOfTheModel)
sol.run(verb=0)

Result = sol.get_dparam(returnas=dict)
#sol.get_summary()

plt.figure()
plt.subplot(411);plt.plot(Result['time']['value'],Result['W']['value']);plt.ylabel('W')
plt.subplot(412);plt.plot(Result['time']['value'],Result['L']['value']);plt.ylabel('L')
plt.plot(Result['time']['value'],Result['N']['value'])
plt.subplot(413);plt.plot(Result['time']['value'],Result['omega']['value']);plt.ylabel('Omega')
plt.subplot(414);plt.plot(Result['time']['value'],Result['lambda']['value']);plt.ylabel('Lambda')
plt.suptitle(NameOfTheModel)
plt.show()
