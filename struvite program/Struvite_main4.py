                               
                                        

import numpy as np 
from Struvite4 import Struvite4



"""Input Waste water composition: all concentrations in M, alkalinity in N"""
T=25.0; pH=7.2; P=0.00371; Nt=0.0304; Mg=0.00103; Na=0.007
Cl=0.03; Ca=0.00203; K=0.00195; S=0.0016; Alkalinity=0.025

ww=[T,pH,P,Nt,Mg,Na,Cl,Ca,K,S,Alkalinity]

"""Choose Mg source"""

"""for mixing with brines: Input brine source and price in $/m^3"""
"""temp, pH, Mg, Na, Cl, Ca, K, S, Alk"""
br=[25,8,0.328,0.543,0.781,0.037,0.240,0.03,0.003735]


"""for Mg chemicals additions: Input Mg source and price in $/ton or in $/m3 for brine: [#source,price]
MgSO4:7H2O; MgCl2:6H2O; Mix with brine"""

Mg_source=['MgSO4:7H2O',275.0]          #paper: NF=0.64$/m^3 MgSO4:7H20=275$/ton , MgCl2=140$/ton

"""Select Base type: [base, price] (price in $/ton of pure chemical
 NaOH, Mg(OH)2"""

base = ['NaOH',650.0]

"""Input Mg/P molar ratio and operational pH"""
Mg_P_ratio=1.1
pH_reactor=7.71

"""CO2 Stripping parameters"""
QaQw = 0.5
KLa = 20*10**-3   #1/s from Chaumat et al 2005 for industrial co-current bubble column
HRT = 30.0  #Hydraulic Retention Time (min)
depth = 5.0  #reactor depth (m)
KWh_cost = 0.068  #$/KWh

"""Precipitate Amorphous Calcium Phosphate (ACP)? Yes: ACP=1;  No: ACP=0"""
ACP=0

"""Run Scenarios"""
pH_reactor = np.arange(8.0, 9.0, 0.2)
cost = np.arange(8.0, 9.0, 0.2)
Prem = np.arange(8.0, 9.0, 0.2)
i=0


for i in range (len(cost)):
    scenario = Struvite4(ww, br, Mg_source, Mg_P_ratio, pH_reactor[i], base, ACP, QaQw, KLa, HRT, depth, KWh_cost)
    cost[i] = scenario[19]
    Prem[i] = scenario[1]
    
    
   
    
print ('pH')
print ('\n'.join(map(str, pH_reactor)))
print ('\nCost')
print ('\n'.join(map(str, cost)))
print ('\nP removal')
print ('\n'.join(map(str, Prem)))

