def Struvite4(ww, br, Mg_source, Mg_P_ratio, pH_reactor, base, ACP, QaQw, KLa, HRT, depth, KWh_cost): 

    """Struvite Precipitation Reactor Equilibrium Simulation""
    """
    # Import standard library modules first.
    import os
    # Then get third party modules.
    from win32com.client import Dispatch 
    import numpy as np 
    from math import exp,sqrt
    import scipy.optimize as optimize
   
    def selected_array(db_path, input_string):
        """Load database via COM and run input string.
        """
        dbase = Dispatch('IPhreeqcCOM.Object')
        dbase.LoadDatabase(db_path)
        dbase.RunString(input_string)
        return dbase.GetSelectedOutputArray()

    def phreecalc(input_string):
        """Get results from PHREEQC"""
        PHREEQC_output = selected_array('minteq.v4.dat', input_string)
        return PHREEQC_output
    
    def func(qaqw):
            return 1/(1+CO2_Ct*H*qaqw*(1-exp(-KLa*60*HRT/H/qaqw))) - Cout_Cin

    H=1.14     #CO2 unitless Henry coefficient 

    if base[0]=="NaOH": 
        mw_b=39.99711
    elif base[0]=="Mg(OH)2":
        mw_b=58.31968
        
    if Mg_source[0] == "Mix with brine":
        Mg_dose=(Mg_P_ratio*ww[2]-ww[4])/br[2]   #mass balance determining mixing ratio based on determined Mg to P ratio
        CO2_mix_input1="""
        PHASES
         Fix_H+
            H+=H+
            log_k     0
        SOLUTION 0 -wastewater
            temp      %f
            pH        %f
            pe        4
            redox     pe
            units     mol/l
            P         %f
            N(-3)     %f
            Mg        %f
            Na        %f
            Cl        %f
            Ca        %f
            K         %f
            S(6)      %f
            Alkalinity %f
            -water    1 # kg
        SOLUTION 1 -Brine 
            temp      %f
            pH        %f
            pe        4
            redox     pe
            units     mol/l
            Mg        %f
            Na        %f
            Cl        %f
            Ca        %f
            K         %f
            S(6)      %f
            Alkalinity  %f
            -water    1 # kg
        MIX 1
            0    1
            1    %f
        EQUILIBRIUM_PHASES 1
            Fix_H+    -%f %s      1            
        SELECTED_OUTPUT
            -selected_out         true
            -reset                false
            -ph                   true
            -alkalinity           true 
            -ionic_strength       true
            -totals               Cl  Mg  P  Ca  K  N(-3) C(4) Na S(6)
            -molalities           H2CO3
            -equilibrium_phases   Fix_H+
        END"""%(ww[0],ww[1],ww[2],ww[3],ww[4],ww[5],ww[6],ww[7],ww[8],ww[9],ww[10],br[0],br[1],
                br[2],br[3],br[4],br[5],br[6],br[7],br[8],Mg_dose,pH_reactor,base[0])
        
        CO2_mix_output1 = phreecalc(CO2_mix_input1)
        Ct_in = CO2_mix_output1[3][9]  #Find inlet Ct
        CO2_Ct = CO2_mix_output1[3][12]/CO2_mix_output1[3][9]   #find CO2/Ct ratio
        Ct_out = Ct_in/(1+CO2_Ct*H*QaQw*(1-exp(-KLa*HRT*60/H/QaQw))) #find outlet Ct according to the kinetic model
        CO2_kinetic = Ct_in - Ct_out  #find the ammount of CO2 stripped [M] according to the kinetic model
              
        Mg_dose=(Mg_P_ratio*ww[2]-ww[4])/br[2]  #mass balance determining mixing ratio
        CO2_mix_input2="""
        PHASES
        Struvite
            MgNH4PO4(H2O)6 = 6H2O + Mg+2 + NH4+ + PO4-3
            log_k     -13.26
            delta_h   22.6 kJ
        Fix_H+
            H+=H+
            log_k     0
        SOLUTION 0 -wastewater
            temp      %f
            pH        %f
            pe        4
            redox     pe
            units     mol/l
            P         %f
            N(-3)     %f
            Mg        %f
            Na        %f
            Cl        %f
            Ca        %f
            K         %f
            S(6)      %f
            Alkalinity %f
            -water    1 # kg
        SOLUTION 1 -Brine 
            temp      %f
            pH        %f
            pe        4
            redox     pe
            units     mol/l
            Mg        %f
            Na        %f
            Cl        %f
            Ca        %f
            K         %f
            S(6)      %f
            Alkalinity  %f
            -water    1 # kg
        MIX 1
            0    1
            1    %f
        EQUILIBRIUM_PHASES 1
            CO2(g)    -3.398  0
            Struvite  0 0
        SELECTED_OUTPUT
            -selected_out         true
            -reset                false
            -ph                   true
            -alkalinity           true
            -ionic_strength       true
            -totals               Cl  Mg  P  Ca  K  N(-3) C(4) Na S(6)                         
            -equilibrium_phases   Struvite  CO2(g)
        END"""%(ww[0],ww[1],ww[2],ww[3],ww[4],ww[5],ww[6],ww[7],ww[8],ww[9],ww[10],br[0],br[1],
                br[2],br[3],br[4],br[5],br[6],br[7],br[8],Mg_dose)
        
        CO2_mix_output2 = phreecalc(CO2_mix_input2)  #get results for the above input
               
        CO2_strip_potential = CO2_mix_output2[3][15]   #find the maximun ammount of CO2 that could be stripped by air (equilibrium)               
        pH_CO2_mix = CO2_mix_output2[3][0]  #find the resulting pH
        
        CO2_max_operational = 100.0  #initialize this parameter

        if pH_CO2_mix > pH_reactor:    #If the potential for CO2 stripping is larger than needed to mintain the reactor pH:
            mix_input="""
            PHASES
            Struvite
                MgNH4PO4(H2O)6 = 6H2O + Mg+2 + NH4+ + PO4-3
                log_k     -13.26
                delta_h   22.6 kJ
            Fix_H+
                H+=H+
                log_k     0
            SOLUTION 0 -wastewater
                temp      %f
                pH        %f
                pe        4
                redox     pe
                units     mol/l
                P         %f
                N(-3)     %f
                Mg        %f
                Na        %f
                Cl        %f
                Ca        %f
                K         %f
                S(6)      %f
                Alkalinity %f
                -water    1 # kg
            SOLUTION 1 -Brine 
                temp      %f
                pH        %f
                pe        4
                redox     pe
                units     mol/l
                Mg        %f
                Na        %f
                Cl        %f
                Ca        %f
                K         %f
                S(6)      %f
                Alkalinity  %f
                -water    1 # kg
            MIX 1
                0    1
                1    %f
            EQUILIBRIUM_PHASES 1
                Fix_H+    -%f  CO2(g)    1
                Struvite  0 0
            SELECTED_OUTPUT
                -selected_out         true
                -reset                false
                -ph                   true
                -alkalinity           true
                -ionic_strength       true
                -totals               Cl  Mg  P  Ca  K  N(-3) C(4) Na S(6)                         
                -equilibrium_phases   Struvite  Fix_H+
            END"""%(ww[0],ww[1],ww[2],ww[3],ww[4],ww[5],ww[6],ww[7],ww[8],ww[9],ww[10],br[0],br[1],
                    br[2],br[3],br[4],br[5],br[6],br[7],br[8],Mg_dose,pH_reactor)
            
            mix_output = phreecalc(mix_input)
            CO2_max_operational = mix_output[3][15]   #find the practical ammount of CO2 need to be stripped to maintain the reactor pH 
            base_dose = 0
        
        if CO2_kinetic < CO2_max_operational:  #if CO2_stripped found by the kinetic model is lower than needed, use it as reactant and add strong base as needed
            CO2_stripped = CO2_kinetic
            mix_input="""
            PHASES
            Struvite
                MgNH4PO4(H2O)6 = 6H2O + Mg+2 + NH4+ + PO4-3
                log_k     -13.26
                delta_h   22.6 kJ
            Fix_H+
                H+=H+
                log_k     0
            SOLUTION 0 -wastewater
                temp      %f
                pH        %f
                pe        4
                redox     pe
                units     mol/l
                P         %f
                N(-3)     %f
                Mg        %f
                Na        %f
                Cl        %f
                Ca        %f
                K         %f
                S(6)      %f
                Alkalinity %f
                -water    1 # kg
            SOLUTION 1 -Brine 
                temp      %f
                pH        %f
                pe        4
                redox     pe
                units     mol/l
                Mg        %f
                Na        %f
                Cl        %f
                Ca        %f
                K         %f
                S(6)      %f
                Alkalinity  %f
                -water    1 # kg
            MIX 1
                0    1
                1    %f
            REACTION 1
                CO2(g)     -%f
                1 moles in 1 steps
            EQUILIBRIUM_PHASES 1
                Fix_H+    -%f %s      1
                Struvite  0 0
            SELECTED_OUTPUT
                -selected_out         true
                -reset                false
                -ph                   true
                -alkalinity           true
                -ionic_strength       true
                -totals               Cl  Mg  P  Ca  K  N(-3) C(4) Na S(6)                         
                -equilibrium_phases   Struvite  Fix_H+
            END"""%(ww[0],ww[1],ww[2],ww[3],ww[4],ww[5],ww[6],ww[7],ww[8],ww[9],ww[10],br[0],br[1],
                    br[2],br[3],br[4],br[5],br[6],br[7],br[8],Mg_dose,CO2_stripped,pH_reactor,base[0])

            mix_output = phreecalc(mix_input)
            base_dose = -mix_output[3][15] 

        cost_Mg = Mg_source[1]*Mg_dose   #operational cost of Mg chemical
        cost_base = base_dose*mw_b*1e-3*base[1]    #price of base 
        cost_tot = cost_Mg + cost_base  #total operational cost in $/m^3 wastewater
        cost_Kg_P = cost_tot/(ww[2]*30.97376)  #total operational cost in $/kg-P removed
        
        Struvite=mix_output[3][13]; ACP_precip = 0
        P_removal = Struvite/ww[2]; Struvite_purity=1.0
        P_eff = mix_output[3][5]; N_eff = mix_output[3][8]; Cl_eff = mix_output[3][3]; Na_eff = mix_output[3][10]
        Mg_eff = mix_output[3][4]; Ca_eff = mix_output[3][6]; K_eff = mix_output[3][7]; SO4_eff=mix_output[3][11]
        Alk_eff = mix_output[3][1]
        
     #Chemical dosage Option:   
    else:
        if Mg_source[0]=="MgSO4:7H2O":
            mw_Mg = 246.3676
        if Mg_source[0]=="MgCl2:6H2O":
            mw_Mg = 203.211

        Mg_dose=Mg_P_ratio*ww[2]-ww[4]
        if Mg_dose<0:
            Mg_dose=0

        CO2_dose_input1="""
        PHASES
        Struvite
            MgNH4PO4(H2O)6 = 6H2O + Mg+2 + NH4+ + PO4-3
            log_k     -13.26
            delta_h   22.6 kJ
        Fix_H+
            H+=H+
            log_k     0
        MgSO4:7H2O
            MgSO4(H2O)7 = Mg+2 + SO4-2 +7H2O
            log_k     10
        MgCl2:6H2O
            MgCl2(H2O)6 = Mg+2 + 2Cl- + 6H2O
            log_k     10
        SOLUTION 0 -wastewater
            temp      %f
            pH        %f
            pe        4
            redox     pe
            units     mol/l
            P         %f
            N(-3)     %f
            Mg        %f
            Na        %f
            Cl        %f
            Ca        %f
            K         %f
            S(6)      %f
            Alkalinity %f
            -water    1 # kg
        REACTION 1
            %s   1
            %f moles in 1 steps
        EQUILIBRIUM_PHASES 1
            Fix_H+    -%f %s      1            
        SELECTED_OUTPUT
            -selected_out         true
            -reset                false
            -ph                   true
            -alkalinity           true 
            -ionic_strength       true
            -totals               Cl  Mg  P  Ca  K  N(-3) C(4) Na S(6)
            -molalities           H2CO3
            -equilibrium_phases   Fix_H+
        END"""%(ww[0],ww[1],ww[2],ww[3],ww[4],ww[5],ww[6],ww[7],ww[8],ww[9],ww[10],Mg_source[0],Mg_dose,pH_reactor,base[0])
         
        CO2_dose_output1 = phreecalc(CO2_dose_input1)
        Ct_in = CO2_dose_output1[2][9]  #Find inlet Ct using mass balance
        CO2_Ct = CO2_dose_output1[2][12]/CO2_dose_output1[2][9]   #find CO2/Ct ratio
        Ct_out = Ct_in/(1+CO2_Ct*H*QaQw*(1-exp(-KLa*HRT*60/H/QaQw))) #find outlet Ct according to the kinetic model
        CO2_kinetic = Ct_in - Ct_out  #find the ammount of CO2 stripped [M] according to the kinetic model        
        
        CO2_dose_input2="""
        PHASES
        Struvite
            MgNH4PO4(H2O)6 = 6H2O + Mg+2 + NH4+ + PO4-3
            log_k     -13.26
            delta_h   22.6 kJ
        Fix_H+
            H+=H+
            log_k     0
        MgSO4:7H2O
            MgSO4(H2O)7 = Mg+2 + SO4-2 +7H2O
            log_k     10
        MgCl2:6H2O
            MgCl2(H2O)6 = Mg+2 + 2Cl- + 6H2O
            log_k     10
        SOLUTION 0 -wastewater
            temp      %f
            pH        %f
            pe        4
            redox     pe
            units     mol/l
            P         %f
            N(-3)     %f
            Mg        %f
            Na        %f
            Cl        %f
            Ca        %f
            K         %f
            S(6)      %f
            Alkalinity %f
            -water    1 # kg
        REACTION 1
            %s   1
            %f moles in 1 steps
        EQUILIBRIUM_PHASES 1
            CO2(g)    -3.398  0
            Struvite  0 0
        SELECTED_OUTPUT
            -selected_out         true
            -reset                false
            -ph                   true
            -alkalinity           true
            -ionic_strength       true
            -totals               Cl  Mg  P  Ca  K  N(-3) C(4) Na S(6)                         
            -equilibrium_phases   Struvite  CO2(g)
        END"""%(ww[0],ww[1],ww[2],ww[3],ww[4],ww[5],ww[6],ww[7],ww[8],ww[9],ww[10],Mg_source[0],Mg_dose)
        CO2_dose_output2 = phreecalc(CO2_dose_input2)

        CO2_strip_potential = CO2_dose_output2[2][15]   #find the maximun ammount of CO2 that could be stripped by air
        pH_CO2_dose = CO2_dose_output2[2][0] 
        CO2_max_operational = 100.0  #initialize this parameter

        if pH_CO2_dose > pH_reactor:
            dose_input="""
            PHASES
            Struvite
                MgNH4PO4(H2O)6 = 6H2O + Mg+2 + NH4+ + PO4-3
                log_k     -13.26
                delta_h   22.6 kJ
            Fix_H+
                H+=H+
                log_k     0
            MgSO4:7H2O
                MgSO4(H2O)7 = Mg+2 + SO4-2 +7H2O
                log_k     10
            MgCl2:6H2O
                MgCl2(H2O)6 = Mg+2 + 2Cl- + 6H2O
                log_k     10
            SOLUTION 0 -wastewater
                temp      %f
                pH        %f
                pe        4
                redox     pe
                units     mol/l
                P         %f
                N(-3)     %f
                Mg        %f
                Na        %f
                Cl        %f
                Ca        %f
                K         %f
                S(6)      %f
                Alkalinity %f
                -water    1 # kg
            REACTION 1
                %s   %f
                1 moles in 1 steps
            EQUILIBRIUM_PHASES 1
                Fix_H+    -%f  CO2(g)    1
                Struvite  0 0
            SELECTED_OUTPUT
                -selected_out         true
                -reset                false
                -ph                   true
                -alkalinity           true
                -ionic_strength       true
                -totals               Cl  Mg  P  Ca  K  N(-3) C(4) Na S(6)                         
                -equilibrium_phases   Struvite  Fix_H+
            END"""%(ww[0],ww[1],ww[2],ww[3],ww[4],ww[5],ww[6],ww[7],ww[8],ww[9],
                    ww[10],Mg_source[0],Mg_dose,pH_reactor)

            dose_output = phreecalc(dose_input)
            CO2_max_operational = dose_output[2][15]
            base_dose = 0
        
        if CO2_kinetic < CO2_max_operational:
            CO2_stripped = CO2_kinetic
            dose_input="""
            PHASES
            Struvite
                MgNH4PO4(H2O)6 = 6H2O + Mg+2 + NH4+ + PO4-3
                log_k     -13.26
                delta_h   22.6 kJ
            Fix_H+
                H+=H+
                log_k     0
            MgSO4:7H2O
                MgSO4(H2O)7 = Mg+2 + SO4-2 +7H2O
                log_k     10
            MgCl2:6H2O
                MgCl2(H2O)6 = Mg+2 + 2Cl- + 6H2O
                log_k     10
            SOLUTION 0 -wastewater
                temp      %f
                pH        %f
                pe        4
                redox     pe
                units     mol/l
                P         %f
                N(-3)     %f
                Mg        %f
                Na        %f
                Cl        %f
                Ca        %f
                K         %f
                S(6)      %f
                Alkalinity %f
                -water    1 # kg
            REACTION 1
                %s   %f
                CO2  -%f
                1 moles in 1 steps
            EQUILIBRIUM_PHASES 1
                Fix_H+    -%f %s      1
                Struvite  0 0
            SELECTED_OUTPUT
                -selected_out         true
                -reset                false
                -ph                   true
                -alkalinity           true
                -ionic_strength       true
                -totals               Cl  Mg  P  Ca  K  N(-3) C(4) Na S(6)                         
                -equilibrium_phases   Struvite  Fix_H+
            END"""%(ww[0],ww[1],ww[2],ww[3],ww[4],ww[5],ww[6],ww[7],ww[8],ww[9],
                    ww[10],Mg_source[0],Mg_dose,CO2_stripped,pH_reactor,base[0])

            dose_output = phreecalc(dose_input)
            base_dose = -dose_output[2][15]        
        
        cost_Mg = Mg_source[1]*Mg_dose*mw_Mg*1e-3   #operational cost of Mg chemical
        cost_base = base_dose*mw_b*1e-3*base[1]    #price of base 
        cost_tot = cost_Mg + cost_base  #total operational cost in $/m^3 wastewater
        cost_Kg_P = cost_tot/(ww[2]*30.97376)  #total operational cost in $/kg-P removed
        
        Struvite = dose_output[2][13]; ACP_precip = 0
        P_removal = Struvite/ww[2]; Struvite_purity=1.0
        P_eff = dose_output[2][5]; N_eff = dose_output[2][8]; Cl_eff = dose_output[2][3];
        Na_eff = dose_output[2][10]; SO4_eff = dose_output[2][11]; Mg_eff = dose_output[2][4];
        Ca_eff = dose_output[2][6]; K_eff = dose_output[2][7]; Alk_eff = dose_output[2][1] 
       
    if ACP==1:

        ACP_input="""
            PHASES
            Fix_H+
            H+ = H+
            log_k     0
        SOLUTION 0 -wastewater
            temp      %f
            pH        %f
            pe        4
            redox     pe
            units     mol/l
            P         %f
            N(-3)     %f
            Mg        %f
            Na        %f
            Cl        %f
            Ca        %f
            K         %f
            S(6)      %f
            Alkalinity %f
            -water    1 # kg
        EQUILIBRIUM_PHASES 1
            Ca3(PO4)2(beta) 0 0
            Fix_H+    -%f %s      1
        SELECTED_OUTPUT
            -selected_out         true
            -reset                false
            -ph                   true
            -alkalinity           true
            -ionic_strength       true
            -totals               Cl  Mg  P  Ca  K  N(-3) C(4) Na S(6)                        
            -equilibrium_phases   Ca3(PO4)2(beta)  Fix_H+
        END"""%(ww[0],ww[1],P_eff,N_eff,Mg_eff,Na_eff,Cl_eff,Ca_eff,K_eff,SO4_eff,Alk_eff,pH_reactor,base[0])
        
        ACP_output = phreecalc(ACP_input)
        base_dose = base_dose - ACP_output[2][15]  #new base price
        if base_dose < 0:
            base_dose = 0
        cost_base = base_dose*mw_b*1e-3*base[1]    #price of base 
        ACP_precip=ACP_output[2][13]; Struvite_purity = Struvite/(Struvite + ACP_precip)
        P_eff = ACP_output[2][5]; N_eff = ACP_output[2][8]; Cl_eff = ACP_output[2][3]; Na_eff = ACP_output[2][10]
        SO4_eff = ACP_output[2][11]; Mg_eff = ACP_output[2][4]; Ca_eff = ACP_output[2][6];
        K_eff = ACP_output[2][7]; Alk_eff=ACP_output[2][1]
        P_removal = 1.0 - P_eff/ww[2]
    
    if CO2_kinetic > CO2_max_operational:
        Cout_Cin =(Ct_in - CO2_max_operational)/Ct_in
        QaQw = optimize.newton(func ,0.0001 , tol=1e-10, maxiter=400)
        CO2_stripped = CO2_max_operational
                        
    Gs = QaQw*273.15*(101.325 + depth*9.81 + 6.89)/101.325/(ww[0]+273.15)
    CO2_KWh = 0.1*Gs*(((101.325+depth*9.81 + 6.89)/101.325)**0.283 - 1)/0.6   #energy consumption efficiency = 0.6
    CO2_cost = CO2_KWh*KWh_cost
    
    cost_tot = cost_Mg + cost_base + CO2_cost  #total operational cost in $/m^3 wastewater
    cost_Kg_P = cost_tot/(ww[2]*30.97376)  #total operational cost in $/kg-P removed
       
    eff = [cost_tot, P_removal, P_eff, N_eff, Cl_eff, Na_eff, Mg_eff, Ca_eff, K_eff, SO4_eff, Alk_eff,
           Mg_dose, base_dose, Struvite, ACP_precip, Struvite_purity, cost_Mg, cost_base,
           CO2_cost, cost_Kg_P, QaQw, CO2_KWh, CO2_stripped]
    
    
    return eff



