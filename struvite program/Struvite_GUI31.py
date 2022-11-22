from tkinter import *

from Struvite4 import Struvite4

class Application(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        self.grid()
        self.create_widgets1()
        self.create_widgets2()
        self.output()
        
    def create_widgets1(self):
        
        self.instructions1 = Label(self, text = "Enter influent properties(M):", font=("Helvetica",12))
        self.instructions1.grid(row = 0,column = 0, columnspan = 3, sticky= W)
        Label(self, text = "pH =").grid(row = 1, column = 0, sticky = E)
        self.pH_ww = Entry(self)
        self.pH_ww.grid(row = 1, column = 1, sticky = W)
        Label(self, text = "T(Celcius) =").grid(row = 1, column = 2, sticky = E)
        self.T_ww = Entry(self)
        self.T_ww.grid(row = 1, column = 3, sticky = W)
        Label(self, text = "Alkalinity(eq/l) =").grid(row = 6, column = 0, sticky = E)
        self.Alk_ww = Entry(self)
        self.Alk_ww.grid(row = 6, column = 1, sticky = W)
        Label(self, text = "P_total =").grid(row = 2, column = 0, sticky = E)
        self.P_ww = Entry(self)
        self.P_ww.grid(row = 2, column = 1, sticky = W)
        Label(self, text = "N_total =").grid(row = 2, column = 2, sticky = E)
        self.N_ww = Entry(self)
        self.N_ww.grid(row = 2, column = 3, sticky = W)
        Label(self, text = "Cl- =").grid(row = 3, column = 0, sticky = E)
        self.Cl_ww = Entry(self)
        self.Cl_ww.grid(row = 3, column = 1, sticky = W)
        Label(self, text = "Na+ =").grid(row = 3, column = 2, sticky = E)
        self.Na_ww = Entry(self)
        self.Na_ww.grid(row = 3, column = 3, sticky = W)
        Label(self, text = "SO4_2- =").grid(row = 4, column = 0, sticky = E)
        self.SO4_ww = Entry(self)
        self.SO4_ww.grid(row = 4, column = 1, sticky = W)
        Label(self, text = "Mg_2+ =").grid(row = 4, column = 2, sticky = E)
        self.Mg_ww = Entry(self)
        self.Mg_ww.grid(row = 4, column = 3, sticky = W)
        Label(self, text = "Ca_2+ =").grid(row = 5, column = 0, sticky = E)
        self.Ca_ww = Entry(self)
        self.Ca_ww.grid(row = 5, column = 1, sticky = W)
        Label(self, text = "K+ =").grid(row = 5, column = 2, sticky = E)
        self.K_ww = Entry(self)
        self.K_ww.grid(row = 5, column = 3, sticky = W)

        self.instructions2 = Label(self, text = "Choose Mg source and enter price:", font=("Helvetica",12))
        self.instructions2.grid(row = 7,column = 0, columnspan = 3, sticky= W)
        self.Mg_source = StringVar()
        self.Mg_source.set(0)
        Radiobutton(self, text = "MgSO4:7H2O", variable = self.Mg_source, value = "MgSO4:7H2O", command = self.create_widgets2).grid(row=8, column=0, sticky=W)
        Radiobutton(self, text = "MgCl2:6H2O", variable = self.Mg_source, value = "MgCl2:6H2O", command = self.create_widgets2).grid(row=8, column=1, sticky=W)
        Radiobutton(self, text = "Mix with brine", variable = self.Mg_source, value = "Mix with brine", command = self.create_widgets2).grid(row=8, column=2, sticky=W)        
    
    def create_widgets2(self):
        
        self.brine_entry_state = "disabled"
        self.brine_cost_entry_state = "disabled"
        self.mineral_cost_entry_state = "disabled"
        if self.Mg_source.get() == "Mix with brine":
            self.brine_entry_state = "normal"
            self.brine_cost_entry_state = "normal"
            self.mineral_cost_entry_state = "disabled"
        if (self.Mg_source.get() == "MgCl2:6H2O") | (self.Mg_source.get()=="MgSO4:7H2O"):
            self.brine_entry_state = "disabled"
            self.brine_cost_entry_state = "disabled"
            self.mineral_cost_entry_state = "normal"

        self.instructions3 = Label(self, text = "Chemical price ($/ton):")
        self.instructions3.grid(row = 9,column = 0, columnspan = 2, sticky= W)
        
        self.mineral_cost = Entry(self, state = self.mineral_cost_entry_state)
        self.mineral_cost.grid(row = 9, column = 1, sticky = W)
        self.instructions4 = Label(self, text = "Brine Cost ($/m^3):")
        
        self.instructions4.grid(row = 9,column = 2, columnspan = 2, sticky= W)
        self.brine_cost = Entry(self, state = self.brine_cost_entry_state)
        self.brine_cost.insert(0,2.5)
        self.brine_cost.grid(row = 9, column = 3, sticky = W)

        self.instructions5 = Label(self, text = "Enter Brine Properties(M):", font=("Helvetica",12))
        self.instructions5.grid(row = 10,column = 0, columnspan = 3, sticky= W)
        
        Label(self, text = "pH =").grid(row = 11, column = 0, sticky = E)
        self.pH_br = Entry(self, state = self.brine_entry_state)
        self.pH_br.insert(0,8)
        self.pH_br.grid(row = 11, column = 1, sticky = W)
        
        Label(self, text = "T(Celcius) =").grid(row = 11, column = 2, sticky = E)
        self.T_br = Entry(self, state = self.brine_entry_state)
        self.T_br.insert(0,25)
        self.T_br.grid(row = 11, column = 3, sticky = W)

        Label(self, text = "Na+ =").grid(row = 12, column = 0, sticky = E)
        self.Na_br = Entry(self, state = self.brine_entry_state)
        self.Na_br.insert(0,0.562)
        self.Na_br.grid(row = 12, column = 1, sticky = W)

        Label(self, text = "Cl- =").grid(row = 12, column = 2, sticky = E)
        self.Cl_br = Entry(self, state = self.brine_entry_state)
        self.Cl_br.insert(0,0.782)
        self.Cl_br.grid(row = 12, column = 3, sticky = W)

        Label(self, text = "Mg_2+ =").grid(row = 13, column = 0, sticky = E)
        self.Mg_br = Entry(self, state = self.brine_entry_state)
        self.Mg_br.insert(0,0.29)
        self.Mg_br.grid(row = 13, column = 1, sticky = W)

        Label(self, text = "SO4_2- =").grid(row = 13, column = 2, sticky = E)
        self.SO4_br = Entry(self, state = self.brine_entry_state)
        self.SO4_br.insert(0,0.2204)
        self.SO4_br.grid(row = 13, column = 3, sticky = W)

        Label(self, text = "Ca_2+ =").grid(row = 14, column = 0, sticky = E)
        self.Ca_br = Entry(self, state = self.brine_entry_state)
        self.Ca_br.insert(0,0.0416)
        self.Ca_br.grid(row = 14, column = 1, sticky = W)
        
        Label(self, text = "Alkalinity(eq/l) =").grid(row = 14, column = 2, sticky = E)
        self.Alk_br = Entry(self, state = self.brine_entry_state)
        self.Alk_br.insert(0,0.003735)
        self.Alk_br.grid(row = 14, column = 3, sticky = W)        
        
        Label(self, text = "K+ =").grid(row = 15, column = 0, sticky = E)
        self.K_br = Entry(self, state = self.brine_entry_state)
        self.K_br.insert(0,0.012)
        self.K_br.grid(row = 15, column = 1, sticky = W)

        self.instructions6 = Label(self, text = "Choose Alkalinity source and enter price:",font=("Helvetica",12))
        self.instructions6.grid(row = 17,column = 0, columnspan = 2, sticky= W)
        self.Alk_source = StringVar()
        self.Alk_source.set("NaOH")
        Radiobutton(self, text = "NaOH", variable = self.Alk_source, value = "NaOH").grid(row=18, column=0, sticky=W)
        Radiobutton(self, text = "Mg(OH)2", variable = self.Alk_source, value = "Mg(OH)2").grid(row=18, column=1, sticky=W)
                
        self.instructions7 = Label(self, text = "Chemical price ($/ton):")
        self.instructions7.grid(row = 19,column = 0, columnspan = 2, sticky= W)
        self.base_price = Entry(self)
        self.base_price.insert(0,500)
        self.base_price.grid(row = 19, column = 1, sticky = W)
        
        self.instructions8 = Label(self, text = "Enter operational conditions:",font=("Helvetica",12))
        self.instructions8.grid(row = 20,column = 0, columnspan = 2, sticky= W)
        self.instructions9 = Label(self, text = "Reactor pH:")
        self.instructions9.grid(row = 21,column = 0, columnspan = 2, sticky= W)
        self.pH_reactor = Entry(self)
        self.pH_reactor.insert(0,7.4)
        self.pH_reactor.grid(row = 21, column = 1, sticky = W)        
        
        self.instructions12 = Label(self, text = "Mg/P molar ratio:")
        self.instructions12.grid(row = 21,column = 2, columnspan = 2, sticky= W)
        self.Mg2P = Entry(self)
        self.Mg2P.insert(0,1.1)
        self.Mg2P.grid(row = 21, column = 3, sticky = W)

        self.instructions121 = Label(self, text = "Retention time (min):")
        self.instructions121.grid(row = 22,column = 0, columnspan = 2, sticky= W)
        self.HRT = Entry(self)
        self.HRT.insert(0,20)
        self.HRT.grid(row = 22, column = 1, sticky = W)

        self.instructions122 = Label(self, text = "Air to water flow Ratio:")
        self.instructions122.grid(row = 22,column = 2, columnspan = 2, sticky= W)
        self.QaQw = Entry(self)
        self.QaQw.insert(0,0.001)
        self.QaQw.grid(row = 22, column = 3, sticky = W)

        self.instructions123 = Label(self, text = "Energy price ($/KWh):")
        self.instructions123.grid(row = 23,column = 0, columnspan = 2, sticky= W)
        self.KWh_price = Entry(self)
        self.KWh_price.insert(0,0.06)
        self.KWh_price.grid(row = 23, column = 1, sticky = W)

        self.instructions124 = Label(self, text = "Reactor depth (m):")
        self.instructions124.grid(row = 23,column = 2, columnspan = 2, sticky= W)
        self.depth = Entry(self)
        self.depth.insert(0,5)
        self.depth.grid(row = 23, column = 3, sticky = W)

        self.instructions125 = Label(self, text = "CO2 mass transfer coefficient -KLa- (1/s):")
        self.instructions125.grid(row = 24,column = 0, columnspan = 2, sticky= W)
        self.KLa = Entry(self)
        self.KLa.insert(0,20e-3)
        self.KLa.grid(row = 24, column = 2, sticky = W)

        self.ACP = IntVar()
        self.ACP_button = Checkbutton(self, text = "Equilibriate with Amorphous Calcium-Phosphate After Struvite Precipitation", variable = self.ACP)
        self.ACP_button.grid(row = 26, column = 0, columnspan=3, sticky = W)

        self.RUN = Button(self, text = "RUN",width = 15, font=("Ariel",14, "bold"), background='green',command = self.GO)
        self.RUN.grid(row = 27, column = 3, columnspan = 3, sticky =W)

        """self.background_image=PhotoImage(file='water.gif')
        self.background_label = Label(image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)"""

    def output(self):    
        self.space1=Label(self,text = "         ").grid(row=0,column=4, sticky=W)
        self.instructions13 = Label(self, text = "Results:", font=("Helvetica",12)).grid(row = 0,column = 5, sticky= W)
        
        self.instructions14 = Label(self, text = "Effluent Composition (M):", font=("Helvetica",12)).grid(row = 1,column = 5, sticky= W)
        self.P_eff_lbl = Label(self, text = "P_total:").grid(row=2, column=5, sticky = E)
        self.P_eff = Text(self, width = 15, height = 1, wrap = WORD, font=("Helvetica",12))
        self.P_eff.grid(row = 2, column = 6, sticky = W)
        
        self.N_eff_lbl = Label(self, text = "N_total:").grid(row=2, column=7, sticky = E)
        self.N_eff = Text(self, width = 15, height = 1, wrap = WORD, font=("Helvetica",12))
        self.N_eff.grid(row = 2, column = 8, sticky = W)

        self.Cl_eff_lbl = Label(self, text = "Cl-:").grid(row=3, column=5, sticky = E)
        self.Cl_eff = Text(self, width = 15, height = 1, wrap = WORD, font=("Helvetica",12))
        self.Cl_eff.grid(row = 3, column = 6, sticky = W)
        
        self.Na_eff_lbl = Label(self, text = "Na+:").grid(row=3, column=7, sticky = E)
        self.Na_eff = Text(self, width = 15, height = 1, wrap = WORD, font=("Helvetica",12))
        self.Na_eff.grid(row = 3, column = 8, sticky = W)

        self.Mg_eff_lbl = Label(self, text = "Mg_2+:").grid(row=4, column=5, sticky = E)
        self.Mg_eff = Text(self, width = 15, height = 1, wrap = WORD, font=("Helvetica",12))
        self.Mg_eff.grid(row = 4, column = 6, sticky = W)
        
        self.Ca_eff_lbl = Label(self, text = "Ca_2+:").grid(row=4, column=7, sticky = E)
        self.Ca_eff = Text(self, width = 15, height = 1, wrap = WORD, font=("Helvetica",12))
        self.Ca_eff.grid(row = 4, column = 8, sticky = W)

        self.K_eff_lbl = Label(self, text = "K+:").grid(row=5, column=5, sticky = E)
        self.K_eff = Text(self, width = 15, height = 1, wrap = WORD, font=("Helvetica",12))
        self.K_eff.grid(row = 5, column = 6, sticky = W)
        
        self.SO4_eff_lbl = Label(self, text = "SO4_2-:").grid(row=5, column=7, sticky = E)
        self.SO4_eff = Text(self, width = 15, height = 1, wrap = WORD, font=("Helvetica",12))
        self.SO4_eff.grid(row = 5, column = 8, sticky = W)

        self.Alk_eff_lbl = Label(self, text = "Alkalinity(eq/L):").grid(row=6, column=5, sticky = E)
        self.Alk_eff = Text(self, width = 15, height = 1, wrap = WORD, font=("Helvetica",12))
        self.Alk_eff.grid(row = 6, column = 6, sticky = W)

        self.instructions15 = Label(self, text = "Minerals Precipitated and CO2 stripped (mol/Liter_influent):",font=("Helvetica",12))
        self.instructions15.grid(row =8 ,column = 5, columnspan=3, sticky= W)
        self.struvite_precip_lbl = Label(self, text = "Struvite:").grid(row=9, column=5, sticky = E)
        self.struvite_precip = Text(self, width = 15, height = 1, wrap = WORD, font=("Helvetica",12))
        self.struvite_precip.grid(row = 9, column = 6, sticky = W)

        self.ACP_precip_lbl = Label(self, text = "Amorphous Calcium-Phosphate:").grid(row=9, column=7, sticky = E, columnspan=1)
        self.ACP_precip = Text(self, width = 15, height = 1, wrap = WORD, font=("Helvetica",12))
        self.ACP_precip.grid(row = 9, column = 8, sticky = W)
        
        self.Struvite_purity_lbl = Label(self, text = "Struvite Purity (Molar Ratio):").grid(row = 10,column = 5, columnspan=1 ,sticky=E)
        self.Struvite_purity = Text(self, width = 15, height = 1, wrap = WORD, font=("Helvetica",12))
        self.Struvite_purity.grid(row = 10, column = 6, sticky = W)

        self.P_remov_lbl = Label(self, text = "P removal(%):").grid(row=11, column=5, sticky = E)
        self.P_removal = Text(self, width = 15, height = 1, wrap = WORD, font=("Helvetica",12))
        self.P_removal.grid(row = 11, column = 6, sticky = W)

        self.CO2_stripped_lbl = Label(self, text = "CO2 stripped(M):").grid(row = 10,column = 7, columnspan=1 ,sticky=E)
        self.CO2_stripped = Text(self, width = 15, height = 1, wrap = WORD, font=("Helvetica",12))
        self.CO2_stripped.grid(row = 10, column = 8, sticky = W)

        self.QaQw_output_lbl = Label(self, text = "Air to water flow ratio:").grid(row = 11,column = 7,columnspan=1,sticky=E)
        self.QaQw_output = Text(self, width = 15, height = 1, wrap = WORD, font=("Helvetica",12))
        self.QaQw_output.grid(row = 11, column = 8, sticky = W)

        self.instructions16 = Label(self, text = "Chemicals/energy consumptions and associated costs per m^3 treated effluent:",font=("Helvetica",12))
        self.instructions16.grid(row =13 ,column = 5, columnspan=4, sticky= W)

        self.Mg_dose_lbl = Label(self, text = "Mg salt dose(M):").grid(row = 14,column = 5,sticky=E)
        self.Mg_dose = Text(self, width = 15, height = 1, wrap = WORD, font=("Helvetica",12))
        self.Mg_dose.grid(row = 14, column = 6, sticky = W)

        self.cost_Mg_lbl = Label(self, text = "Mg salt cost($/m^3):").grid(row = 14,column = 7,sticky=E)
        self.cost_Mg = Text(self, width = 15, height = 1, wrap = WORD, font=("Helvetica",12))
        self.cost_Mg.grid(row = 14, column = 8, sticky = W)

        self.mix_ratio_lbl = Label(self, text = "Brine mixing ratio(l/l):").grid(row = 15,column = 5,sticky=E)
        self.mix_ratio = Text(self, width = 15, height = 1, wrap = WORD, font=("Helvetica",12))
        self.mix_ratio.grid(row = 15, column = 6, sticky = E)

        self.brine_cost_out_lbl = Label(self, text = "Brine cost($/m^3):").grid(row = 15,column = 7,sticky=E)
        self.brine_cost_out = Text(self, width = 15, height = 1, wrap = WORD, font=("Helvetica",12))
        self.brine_cost_out.grid(row = 15, column = 8, sticky = W)
       
        self.base_dose_lbl = Label(self, text = "Base dose (M):").grid(row = 16,column = 5, sticky=E)
        self.base_dose = Text(self, width = 15, height = 1, wrap = WORD, font=("Helvetica",12))
        self.base_dose.grid(row = 16, column = 6, sticky = W)
        
        self.base_cost_lbl = Label(self, text = "Base cost($/m^3):").grid(row=16, column=7, sticky = E)
        self.base_cost = Text(self, width = 15, height = 1, wrap = WORD, font=("Helvetica",12))
        self.base_cost.grid(row = 16, column = 8, sticky = W)

        self.KWh_lbl = Label(self, text = "Energy consumptions KWh/m^3:").grid(row = 17,column = 5, sticky=E)
        self.KWh = Text(self, width = 15, height = 1, wrap = WORD, font=("Helvetica",12))
        self.KWh.grid(row = 17, column = 6, sticky = W)

        self.KWh_cost_lbl = Label(self, text = "Energy cost($/m^3):").grid(row=17, column=7, sticky = E)
        self.KWh_cost = Text(self, width = 15, height = 1, wrap = WORD, font=("Helvetica",12))
        self.KWh_cost.grid(row = 17, column = 8, sticky = E)

        self.opex_lbl = Label(self, text = "Opex($/m^3):",font=("Helvetica",12)).grid(row=19, column=5, sticky = E)
        self.opex = Text(self, width = 15, height = 1, wrap = WORD, font=("Helvetica",12))
        self.opex.grid(row = 19, column = 6, sticky = W)

        self.opex_KgP_lbl = Label(self, text = "Cost per P removed($/Kg-P):",font=("Helvetica",10)).grid(row=19, column=7, sticky = E)
        self.opex_KgP = Text(self, width = 15, height = 1, wrap = WORD, font=("Helvetica",12))
        self.opex_KgP.grid(row = 19, column = 8, sticky = W)

        self.info = Text(self, width = 65, height = 8, wrap = WORD, font=("Helvetica",10))
        self.info.grid(row = 21,rowspan=10, column = 6,columnspan=3, sticky = W)

        self.info.delete(0.0,END)
        self.info.insert(0.0,"The Struvite Process Design and Operation Tool was developed at the Faculty of Civil and Environmental Engineering, Technion, Israel and is now updated and maintained in the Zuckerberg Institute for Water Research, Ben-Gurion University, Israel"
                             ". \n"
                             "For questions and support, please contact Oded Nir (program developer) at odni@bgu.ac.il \n"
                             "Reference Information DOI: 10.1080/09593330.2015.1015455,")
                                            
    def GO(self):

        self.WW = [float(self.T_ww.get()), float(self.pH_ww.get()), float(self.P_ww.get()), float(self.N_ww.get()),
                   float(self.Mg_ww.get()), float(self.Na_ww.get()), float(self.Cl_ww.get()), float(self.Ca_ww.get()),
                   float(self.K_ww.get()), float(self.SO4_ww.get()), float(self.Alk_ww.get())]

        if self.Mg_source.get() == "Mix with brine": 
            self.BR = [float(self.T_br.get()), float(self.pH_br.get()), float(self.Mg_br.get()),
                       float(self.Na_br.get()), float(self.Cl_br.get()), float(self.Ca_br.get()),
                       float(self.K_br.get()), float(self.SO4_br.get()), float(self.Alk_br.get())]
            self.Mg_price = float(self.brine_cost.get())
        else:
            self.BR="null"
            self.Mg_price = float(self.mineral_cost.get())
        
        self.results = Struvite4(self.WW, self.BR, [self.Mg_source.get(),self.Mg_price],float(self.Mg2P.get()), float(self.pH_reactor.get()),
                                 [self.Alk_source.get(), float(self.base_price.get())], float(self.ACP.get()), float(self.QaQw.get()),
                                 float(self.KLa.get()), float(self.HRT.get()), float(self.depth.get()), float(self.KWh_price.get()))

        #print self.results
       
        self.opex.delete(0.0,END)
        self.opex.insert(0.0,round(self.results[0],2))
        
        self.P_removal.delete(0.0,END)
        self.P_removal.insert(0.0,round(100*self.results[1],1))

        self.P_eff.delete(0.0,END)
        self.P_eff.insert(0.0,round(self.results[2], 5))
        
        self.N_eff.delete(0.0,END)
        self.N_eff.insert(0.0,round(self.results[3],5))

        self.Cl_eff.delete(0.0,END)
        self.Cl_eff.insert(0.0,round(self.results[4], 4))
        
        self.Na_eff.delete(0.0,END)
        self.Na_eff.insert(0.0,round(self.results[5], 4))

        self.Mg_eff.delete(0.0,END)
        self.Mg_eff.insert(0.0,round(self.results[6], 4))
        
        self.Ca_eff.delete(0.0,END)
        self.Ca_eff.insert(0.0,round(self.results[7], 4))

        self.K_eff.delete(0.0,END)
        self.K_eff.insert(0.0,round(self.results[8], 4))
        
        self.SO4_eff.delete(0.0,END)
        self.SO4_eff.insert(0.0,round(self.results[9], 4))

        self.Alk_eff.delete(0.0,END)
        self.Alk_eff.insert(0.0,round(self.results[10], 4))

        if self.Mg_source.get() == "Mix with brine": 

            self.mix_ratio.delete(0.0,END)
            self.mix_ratio.insert(0.0,round(self.results[11], 3))

            self.brine_cost_out.delete(0.0,END)
            self.brine_cost_out.insert(0.0,round(self.results[16], 3))

            self.Mg_dose.delete(0.0,END)
            self.cost_Mg.delete(0.0,END)
        else:
            self.Mg_dose.delete(0.0,END)
            self.Mg_dose.insert(0.0,round(self.results[11], 3))

            self.cost_Mg.delete(0.0,END)
            self.cost_Mg.insert(0.0,round(self.results[16], 3))

            self.mix_ratio.delete(0.0,END)
            self.brine_cost_out.delete(0.0,END)

        self.base_dose.delete(0.0,END)
        self.base_dose.insert(0.0,round(self.results[12], 3))

        self.struvite_precip.delete(0.0,END)
        self.struvite_precip.insert(0.0,round(self.results[13], 3))

        self.ACP_precip.delete(0.0,END)
        self.ACP_precip.insert(0.0,round(self.results[14], 3))
        
        self.Struvite_purity.delete(0.0,END)
        self.Struvite_purity.insert(0.0,round(self.results[15], 3))        
       
        self.base_cost.delete(0.0,END)
        self.base_cost.insert(0.0,round(self.results[17], 3))

        self.KWh_cost.delete(0.0,END)
        self.KWh_cost.insert(0.0,round(self.results[18], 3))

        self.opex_KgP.delete(0.0,END)
        self.opex_KgP.insert(0.0,round(self.results[19], 3))

        self.QaQw_output.delete(0.0,END)
        self.QaQw_output.insert(0.0,round(self.results[20], 3))

        self.KWh.delete(0.0,END)
        self.KWh.insert(0.0,round(self.results[21], 3))

        self.CO2_stripped.delete(0.0,END)
        self.CO2_stripped.insert(0.0,round(self.results[22], 4))
                       
      
        
root = Tk()
root.title("Struvite Process Design and Operation Tool")
root.geometry("1250x640")
app = Application(root)
root.mainloop()

        
        
