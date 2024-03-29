# -*- coding: utf-8 -*-
import time                   # Time (run speed) printing
import Parameters as Par      # All the parameters of the system
import ClassesGoodwin as C    # Core of models
import Miscfunc as M          # All miscellaneous functions
import VariableDictionnary as VarD # Useful infos on variables
import plots as plts          # Already written plot functions

SYS    = C.GK_Reduced()#FULL()#GK_Reduced()  #GK_FULL#     # SYSTEM SOLVED 

### WELCOME MESSAGE ################################################################################
"""
GOODWIN-TYPE RESOLUTION ALGORITHM 

This python code has been created to simulate Goodwin-Keen simulations, with all the variants to it. 
Do not worry about the number of section : the architecture is thought to be user-friendly and coder-friendly

WHAT ARE THE SPECIFICITIES OF THIS CODE ? 
* The algorithm solve parNum['Nx'] system in parrallel : the idea is that later we will couple the systems altogether ("spatial/network properties").
* For now, there is no much coupling, but you can use it to test many initial conditions and array of parameters values 
* The steps are :
    - Creation of the parameters dictionnaries 
        * params   : The physical parameters
        * parNum   : The numerical parameters
        * initCond : The initial vector state
    - Translation into machine friendly variable y
    - Calculation of all the dynamics variable Y_s (the temporal loop)
    - Translation into user-friendly result in the dictionnary results 
    - Additional analysis (period, slow enveloppe mouvement...)
    - Plot of variables and analysis through results

HOW TO IMPLEMENT YOUR TOY-MODEL ? 
    0 Go in ClassesGoodwin
    1 Copy one version that looks alike (typically choose between intensive and extensive type)
    2 Change the name
    3 Change the list of hypothesis in the class description\
    4 Create your list of variables, parameters
    5 Code intermediary functions ( combination of variable and parameters that are practical)
    6 Add them in intermediaryfuncs 
    7 Change the core ( self.f ) of the dynamics 
    8 Change the list of plots  

WHAT I AM (Paul) LOOKING FOR IN FURTHER DEVELOPMENT 
* An Extensive dynamical model 
* Add spatial operators which are non unstable ( I have implicit scheme elsewhere but it's a different kind of resolution, and much more work when you change a model)
* Have a list of all models existing in this framework (copingwithcollapse, Harmoney, predatory-prey...) and code them
* The plots are UGLY ! Let's do something nicer
* As Iloveclim and Dymends are not in python, prepare some bindings 
"""

### PARAMETERS INITIALISATION ######################################################################
####################################################################################################    
parNum   = Par.parnum()                     # Value of numerical parameters 
params   = Par.BasicParameters()            # Value of "Physical" parameters 
params   = Par.Modifications (   params, parNum ) # Original modification you might want to do
initCond = Par.initCond      (   params ,parNum ) # Values of the initial parameters
op       = M.prepareOperators(           parNum ) # Spatial operators initialisation
#params   = SYS.keepUsefulParams( params )   # Cleaning the params dictionnary to be lighter 

print(SYS.description)
SYS.printParameters(params)
M  .PrintNumericalparameters(parNum)

tim=time.time();print('Start simulation...',end='')
y        = SYS.initializeY(initCond,parNum)             ### The vector y containing all the state of a time t.
Y_s, t_s = M.TemporalLoop(y,SYS,op,parNum,params) ### Calculation of all timesteps
print('done ! elapsed time :', time.time()-tim,'s')        

#if p['Save'] : FG.savedata(rootfold,t,Y_s,p,op) # Save the data as a pickle file in a new folder
### Results interpretation #########################################################################
####################################################################################################
"""Now that the simulation is done, we can translate its results in a more readable fashion. 
r is the expansion of Y_s into all the relevant variables we are looking for, stored as a dictionnary.
Then, the other parts are simply plots of the result"""
results = SYS.expandY_simple(Y_s,t_s,op,params)  # Result dictionnary 
results = M.getperiods(results,parNum,op)      # Period measurements 

UsefulVarDic,OrganisedVar = VarD.VariableDictionnary(results)
 

### PLOTS ##########################################################################################
#################################################################################################### 
#SYS.plotlitst_simple(results,parNum)
plts.AllUsefulVariablesSeparate(results,UsefulVarDic)
#plts.OrganisedVar(results,UsefulVarDic, OrganisedVar)

