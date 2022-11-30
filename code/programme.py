import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import pyqtgraph as pg
import PyQt5
#import os
import os.path
#import pdfkit
 


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
from pyqtgraph import PlotWidget, plot



from math import exp
from datetime import datetime
from applicazione_rischio_eng import Ui_MainWindow
from widget_eng import Ui_Form




#quanta emission rate from data in:  doi:10.1093/cid/ciaa1057; three shedder's category and different activities
#UV inactivation constant: pg 6: 10.1093/infdis/jiaa334 in agreement with: 10.1080/02786826.2020.1829536



R =  [[4.0,15.8,28.0],[16.0,50.2,85.7],[97.0,382.5,679.0],[4.4,17.4,30.8],[21.0,65.9,112.5],[134.0,528.5,938.0],[5.7,22.5,39.9],[26.5,83.2,142.0],[170.0,670.4,1190.0],[13.3,52.5,93.1],[63.7,199.9,341.3],[408.0,1690.0,2856.0]] 


#function to compute viral concentration as a function of time 
def concentration(c0,alpha,l_vent,l_rh,l_hepa,l_UV,V,r,n_i,t):  
        return c0*exp(-(l_vent+l_rh+l_hepa+l_UV)*t)+ (1-alpha)*r*n_i*(1-exp(-(l_vent+l_rh+l_hepa+l_UV)*t))/(V*(l_vent+l_rh+l_hepa+l_UV))
    
class Dialog(QtWidgets.QDialog, Ui_Form):
    def __init__(self, *args, obj=None, **kwargs):
        super(Dialog, self).__init__(*args, **kwargs)
        self.setupUi(self)   
        





class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.tabWidget.setCurrentIndex(0)
        MainWindow.setObjectName(self,"Risk evaluation")
        
        self.PlotWidget.setBackground('w')
        self.setWindowIcon(QtGui.QIcon(':img/corona-virus.jpg'))
        # per andare avanti tra le tab
        self.pushButton_16.clicked.connect(self.switch1)  #go to the tab: USER
        self.pushButton_14.clicked.connect(self.switch2)  #go to the tab: ROOM
        self.pushButton_12.clicked.connect(self.switch3)  #go to the tab: OCCUPANTs
        self.pushButton_10.clicked.connect(self.switch4)  #go to the tab: RESULTS
        # per andare indietro tra le tab
        self.pushButton_7.clicked.connect(self.switch3)   #to back the tab: OCCUPANTS
        self.pushButton_11.clicked.connect(self.switch2)  #to back the tab: ROOM
        self.pushButton_13.clicked.connect(self.switch1)  #to back the tab: USER
        self.pushButton_15.clicked.connect(self.switch5)  #to back the tab: HOME
        self.b = 0.4824
        self.l_UV = 7.26
        self.pushButton_5.clicked.connect(self.plot)      #per plottare il grafico della concentrazione
        self.pushButton_2.clicked.connect(self.reset)     #per pulire il grafico della concentrazione
        self.pushButton_4.clicked.connect(self.infobox)   #per la tabellina con i quanta di emissione
        self.pushButton_6.clicked.connect(self.saveFile)  #per il salvataggio del file di testo
 

    def switch1 (self):
        
        self.tabWidget.setCurrentIndex(1)
        
    
    def switch2 (self):        
        
        self.tabWidget.setCurrentIndex(2)
        
        
    def switch3 (self):
        
        self.tabWidget.setCurrentIndex(3)

        
    def switch4 (self):
                
        self.tabWidget.setCurrentIndex(4)
        
    
    def switch5 (self):
        
        self.tabWidget.setCurrentIndex(0)    

        
#function to collect input data       
    def loadData (self):
        
        
        #tab1 parameters
        
        self.username    = self.lineEdit_4.text()                       #user's name 
        self.usersurname = self.lineEdit_5.text()                       #user's surname
        self.pres        = self.lineEdit_2.text()                       #name of the facility
        self.ssd         = self.lineEdit.text()                         #name of the department
        self.room        = self.lineEdit_6.text()                       #name/number of the room
        
        
        #tab2 parameters
        
        self.A       = float(self.lineEdit_7.text())                    #room surface
        self.height  = float(self.lineEdit_8.text())                    #room height
        self.V       = self.A*self.height                               #room volume
        self.l_vent  = float(self.lineEdit_9.text())                    #number of air exchange per hour
        self.rh      = float(self.comboBox_3.currentText())*0.01        #room relative humidity
        self.time    = float(self.lineEdit_10.text())                   #permanence time in the room
        
        
        #tab3 parameters
        
        self.n_i      = float(self.lineEdit_16.text())                  #number of infectious individuals
        if (self.lineEdit_15.text() != ""): 
            self.n_h      = float(self.lineEdit_15.text())              #number of susceptible individuals   
        else:
            self.n_h = 0
        
        self.m        = self.comboBox.currentText()                     #category of susceptible occupants
    
        if (self.checkBox_4.isChecked() == True):
            self.l_hepa = self.l_vent*0.9997                              #virus decay constant due to HEPA filters (filter efficacy = 99%)
        else:
            self.l_hepa = 0
        
        
        
        
        
        
        
        self.h = 0.5*10**(-3)                           
        
        self.n_step = int((self.time)*1./(self.h))
        self.X = np.zeros(self.n_step+1)
        self.T = np.zeros(self.n_step+1)

#function to select the activity of infectious individuals and the corresponding quanta emission rate      
    def getActivity(self):       
        
            # ACTIVITY : Breathing/resting
        if ((self.comboBox_6.currentText() == "Breathing/resting") and (self.comboBox_7.currentText() == "Low")):
                self.r = R[0][0]
            
        elif ((self.comboBox_6.currentText() == "Breathing/resting" ) and ( self.comboBox_7.currentText() == "Medium" )):
                self.r = R[0][1]
               
            
        elif ((self.comboBox_6.currentText() == "Breathing/resting" ) and ( self.comboBox_7.currentText() == "High" )):
                self.r = R[0][2]
        
        elif ((self.comboBox_6.currentText() == "Breathing/resting" ) and ( self.comboBox_7.currentText() == "Shedder's category" )):
                self.r = R[0][2]
              
       
            
            # ACTIVITY : Speaking, coughing or sneezing/resting
        elif ((self.comboBox_6.currentText() == "Speaking, coughing or sneezing/resting" ) and ( self.comboBox_7.currentText() == "Low" )):
                self.r = R[1][0]     
            
        elif ((self.comboBox_6.currentText() == "Speaking, coughing or sneezing/resting" ) and ( self.comboBox_7.currentText() == "Medium" )):
                self.r = R[1][1]    
            
        elif ((self.comboBox_6.currentText() == "Speaking, coughing or sneezing/resting" ) and ( self.comboBox_7.currentText() == "High" )):
                self.r = R[1][2]    
            
        elif ((self.comboBox_6.currentText() == "Speaking, coughing or sneezing/resting" ) and ( self.comboBox_7.currentText() == "Shedder's category" )):
                self.r = R[1][2] 
        
        # ACTIVITY : Loudly speaking or singing/resting
        elif ((self.comboBox_6.currentText() == "Loudly speaking or singing/resting" ) and ( self.comboBox_7.currentText() == "Low" )):
                self.r = R[2][0]     
            
        elif ((self.comboBox_6.currentText() == "Loudly speaking or singing/resting" ) and ( self.comboBox_7.currentText() == "Medium" )):
                self.r = R[2][1]    
            
        elif ((self.comboBox_6.currentText() == "Loudly speaking or singing/resting" ) and ( self.comboBox_7.currentText() == "High" )):
                self.r = R[2][2]    

        elif ((self.comboBox_6.currentText() == "Loudly speaking or singing/resting" ) and ( self.comboBox_7.currentText() == "Shedder's category" )):
                self.r = R[2][2]
                
#=================================================================================================================    
            # ACTIVITY' : Breathing/light
        elif ((self.comboBox_6.currentText() == "Breathing/light" ) and ( self.comboBox_7.currentText() == "Low" )):
                self.r = R[3][0]
            
        elif ((self.comboBox_6.currentText() == "Breathing/light" ) and ( self.comboBox_7.currentText() == "Medium" )):
                self.r = R[3][1]
               
            
        elif ((self.comboBox_6.currentText() == "Breathing/light" ) and ( self.comboBox_7.currentText() == "High" )):
                self.r = R[3][2]
                
        elif ((self.comboBox_6.currentText() == "Breathing/light" ) and ( self.comboBox_7.currentText() == "Shedder's category" )):
                self.r = R[3][2]        
            
            # ACTIVITY' : Speaking, coughing or sneezing/light
        elif ((self.comboBox_6.currentText() == "Speaking, coughing or sneezing/light" ) and ( self.comboBox_7.currentText() == "Low" )):
                self.r = R[4][0]     
            
        elif ((self.comboBox_6.currentText() == "Speaking, coughing or sneezing/light" ) and ( self.comboBox_7.currentText() == "Medium" )):
                self.r = R[4][1]    
            
        elif ((self.comboBox_6.currentText() == "Speaking, coughing or sneezing/light" ) and ( self.comboBox_7.currentText() == "High" )):
                self.r = R[4][2]    
            
        elif ((self.comboBox_6.currentText() == "Speaking, coughing or sneezing/light" ) and ( self.comboBox_7.currentText() == "Shedder's category" )):
                self.r = R[4][2]
        
             # ACTIVITY' : Loudly speaking or singing/light
        elif ((self.comboBox_6.currentText() == "Loudly speaking or singing/light" ) and ( self.comboBox_7.currentText() == "Low" )):
                self.r = R[5][0]     
            
        elif ((self.comboBox_6.currentText() == "Loudly speaking or singing/light" ) and ( self.comboBox_7.currentText() == "Medium" )):
                self.r = R[5][1]    
            
        elif ((self.comboBox_6.currentText() == "Loudly speaking or singing/light" ) and ( self.comboBox_7.currentText() == "High" )):
                self.r = R[5][2]    
                
        elif ((self.comboBox_6.currentText() == "Loudly speaking or singing/light" ) and ( self.comboBox_7.currentText() == "Shedder's category" )):
                self.r = R[5][2]            
        
            #=================================================================================================================    
            # ACTIVITY' : Breathing/moderate
        elif ((self.comboBox_6.currentText() == "Breathing/moderate" ) and ( self.comboBox_7.currentText() == "Low" )):
                self.r = R[6][0]
            
        elif ((self.comboBox_6.currentText() == "Breathing/moderate" ) and ( self.comboBox_7.currentText() == "Medium" )):
                self.r = R[6][1]
               
            
        elif ((self.comboBox_6.currentText() == "Breathing/moderate" ) and ( self.comboBox_7.currentText() == "High" )):
                self.r = R[6][2]
                
        elif ((self.comboBox_6.currentText() == "Breathing/moderate" ) and ( self.comboBox_7.currentText() == "Shedder's category" )):
                self.r = R[6][2]        
            
            # ACTIVITY' : Speaking, coughing or sneezing/moderate
        elif ((self.comboBox_6.currentText() == "Speaking, coughing or sneezing/moderate" ) and ( self.comboBox_7.currentText() == "Low" )):
                self.r = R[7][0]     
            
        elif ((self.comboBox_6.currentText() == "Speaking, coughing or sneezing/moderate" ) and ( self.comboBox_7.currentText() == "Medium" )):
                self.r = R[7][1]    
            
        elif ((self.comboBox_6.currentText() == "Speaking, coughing or sneezing/moderate" ) and ( self.comboBox_7.currentText() == "High" )):
                self.r = R[7][2]
                
        elif ((self.comboBox_6.currentText() == "Speaking, coughing or sneezing/moderate" ) and ( self.comboBox_7.currentText() == "Shedder's category" )):
                self.r = R[7][2]        
            
           # ACTIVITY' : Loudly speaking or singing/moderate
        elif ((self.comboBox_6.currentText() == "Loudly speaking or singing/moderate" ) and ( self.comboBox_7.currentText() == "Low" )):
                self.r = R[8][0]     
            
        elif ((self.comboBox_6.currentText() == "Loudly speaking or singing/moderate" ) and ( self.comboBox_7.currentText() == "Medium" )):
                self.r = R[8][1]    
            
        elif ((self.comboBox_6.currentText() == "Loudly speaking or singing/moderate" ) and ( self.comboBox_7.currentText() == "High" )):
                self.r = R[8][2]    
                
        elif ((self.comboBox_6.currentText() == "Loudly speaking or singing/moderate" ) and ( self.comboBox_7.currentText() == "Shedder's category" )):
                self.r = R[8][2]    
        
            #=================================================================================================================    
            # ACTIVITY' : Breathing/heavy
        elif ((self.comboBox_6.currentText() == "Breathing/heavy" ) and ( self.comboBox_7.currentText() == "Low" )):
                self.r = R[9][0]
            
        elif ((self.comboBox_6.currentText() == "Breathing/heavy" ) and ( self.comboBox_7.currentText() == "Medium" )):
                self.r = R[9][1]
               
            
        elif ((self.comboBox_6.currentText() == "Breathing/heavy" ) and ( self.comboBox_7.currentText() == "High" )):
                self.r = R[9][2]
            
        elif ((self.comboBox_6.currentText() == "Breathing/heavy" ) and ( self.comboBox_7.currentText() == "Shedder's category" )):
                self.r = R[9][2]    
            
           # ACTIVITY' : Speaking, coughing or sneezing/heavy
        elif ((self.comboBox_6.currentText() == "Speaking, coughing or sneezing/heavy" ) and ( self.comboBox_7.currentText() == "Low" )):
                self.r = R[10][0]     
            
        elif ((self.comboBox_6.currentText() == "Speaking, coughing or sneezing/heavy" ) and ( self.comboBox_7.currentText() == "Medium" )):
                self.r = R[10][1]    
           
        elif ((self.comboBox_6.currentText() == "Speaking, coughing or sneezing/heavy" ) and ( self.comboBox_7.currentText() == "High" )):
                self.r = R[10][2]    
                
        elif ((self.comboBox_6.currentText() == "Speaking, coughing or sneezing/heavy" ) and ( self.comboBox_7.currentText() == "Shedder's category" )):
                self.r = R[10][2]        
            
            # ACTIVITY' : Loudly speaking or singing/heavy
        elif ((self.comboBox_6.currentText() == "Loudly speaking or singing/heavy" ) and ( self.comboBox_7.currentText() == "Low" )):
                self.r = R[11][0]     
            
        elif ((self.comboBox_6.currentText() == "Loudly speaking or singing/heavy" ) and ( self.comboBox_7.currentText() == "Medium" )):
                self.r = R[11][1]    
            
        elif ((self.comboBox_6.currentText() == "Loudly speaking or singing/heavy" ) and ( self.comboBox_7.currentText() == "High" )):
                self.r = R[11][2]    
        
        elif ((self.comboBox_6.currentText() == "Loudly speaking or singing/heavy" ) and ( self.comboBox_7.currentText() == "Shedder's category" )):
                self.r = R[11][2]    
                
        else:
                self.r =  2856.0
            
       # print(self.r)    
        

#function to select the mask worn by the occupants        
    def getProtection(self):
    
       
        if ( self.checkBox.isChecked() == False):
                 self.alpha = 0
                 self.beta = 0
      
        elif ( self.checkBox.isChecked() == True):
            
            if (self.comboBox_8.currentText() == "I = no, S = surgical"):
                self.alpha = 0
                self.beta  = 0.49
            
            elif (self.comboBox_8.currentText() == "I = no, S = FFP2"):
                self.alpha = 0
                self.beta  = 0.9
            
            elif (self.comboBox_8.currentText() == "I = surgical, S = no"):
                self.alpha = 0.53
                self.beta  = 0
            
            elif (self.comboBox_8.currentText() == "I = FFP2, S = no"):
                self.alpha = 0.9
                self.beta  = 0          
            
            elif (self.comboBox_8.currentText() == "I = surgical, S = surgical "):
                self.alpha = 0.53
                self.beta  = 0.49
            
            elif (self.comboBox_8.currentText() == "I = FFP2, S = surgical"):
                self.alpha = 0.9
                self.beta  = 0.49
            
            elif (self.comboBox_8.currentText() == "I = surgical, S = FFP2"):
                self.alpha = 0.53
                self.beta  = 0.9
            
            else:
                self.alpha = 0.9
                self.beta  = 0.9
            
           # print(self.alpha)
           # return self.alpha, self.beta

#function to get the room relative humidity                        
    def getUmidity(self):
        self.l_rh = 0
        if self.rh == 0.21:
            self.l_rh = 3.67323*10**(-3)
        elif self.rh == 0.40:
            self.l_rh = 1.5772872*10**(-1)
        else :
            self.l_rh = 4.016*10**(-1)
       
        return self.l_rh

    
#function to compute viral concentration
    def calculation(self):
        
        self.loadData()
        self.getProtection()
        self.getActivity()
        self.getUmidity()
        
        for i in range(self.n_step+1): 
            
           
            self.T[i] = i*self.h
            self.X[i] = concentration(0,self.alpha,self.l_vent,self.l_rh,self.l_hepa,self.l_UV,self.V,self.r,self.n_i,self.T[i])
       
        self.c = self.X[self.n_step]
        return self.T,self.X,self.c

#function to plot the graph of the concentration
    def plot(self):
        
        self.calculation() 
        
        self.PlotWidget.setLabel('bottom',"<span style=\"color:rgb(0, 0, 0);font-size:40px\">Time t [h]</span>")
        self.PlotWidget.setLabel('left',"<span style=\"color:rgb(0,0, 0);font-size:40px\">Viral concentration [quanta/m<sup>3]</span>")
        
        self.PlotWidget.plot(self.T,self.X,pen=pg.mkPen(color = (157, 172, 255), width=7))
    
#funcion for risk evaluation    
    def riskEvaluation(self):
       
        self.getProtection()
        self.loadData()
        self.getUmidity()

        
        
        self.ceq   = (1-self.alpha)*self.r*self.n_i/((self.l_rh+self.l_vent+self.l_hepa+self.l_UV)*self.V)    #equilibrium viral concentration
        
        T = np.zeros(int(self.time*1./0.01 + 1))
        Prob = np.zeros(int(self.time*1./0.01 + 1))
        
        
        if (self.n_h != 0):
           
            #nr. of people allowed to keep the probability of at least one infection < 10%
            self.nh_max = -np.log(0.9)*((self.l_rh+self.l_vent+self.l_hepa+self.l_UV)*self.V)/((1-self.alpha)*(1-self.beta)*self.r*self.b*self.n_i*self.time)                                                                  
            
            #probability of no infections 
            self.P0    = (exp(-((1-self.alpha)*(1-self.beta)*self.r*self.b*self.n_i*self.n_h*self.time)/((self.l_rh+self.l_vent+self.l_hepa+self.l_UV)*self.V)))*100  
        
        
        

            self.P     = (100 - self.P0)                                                 #infection probability for at least one individual     
            self.g     = (self.n_h) * self.P*1./100                                      #number of new infectious individuals        
          
            for i in range(int(self.time*1./0.01 + 1)): 
            
                T[i] = i*0.01
                Prob[i] = 100 - (exp(-((1-self.alpha)*(1-self.beta)*self.r*self.b*self.n_i*self.n_h*T[i])/((self.l_rh+self.l_vent+self.l_hepa+self.l_UV)*self.V)))*100
   
            p1 = plt.figure()
            plt.plot(T,Prob,"b--")
            plt.title("Infection probability")
            plt.xlabel('Time [h]',fontsize=14)            
            plt.ylabel('Infection probability [%]',fontsize=14) 
        
        
        
        if (self.n_h == 0):
            
            #nr. of people allowed to keep the probability of at least one infection < 10%
            self.nh_max = -np.log(0.9)*((self.l_rh+self.l_vent+self.l_hepa+self.l_UV)*self.V)/((1-self.alpha)*(1-self.beta)*self.r*self.b*self.n_i*self.time)                                                           
     
            #probability of no infections 
            self.P0    = (exp(-((1-self.alpha)*(1-self.beta)*self.r*self.b*self.n_i*self.nh_max*self.time)/((self.l_rh+self.l_vent+self.l_hepa+self.l_UV)*self.V)))*100 
        
        
            self.P     = (100 - self.P0)                                                  #infection probability for at least one individual   
            self.g     = (self.nh_max) * self.P*1./100                                    #number of new infectious individuals       

            for i in range(int(self.time*1./0.01 + 1)): 
                
                
                T[i] = i*0.01
                Prob[i] = 100 - (exp(-((1-self.alpha)*(1-self.beta)*self.r*self.b*self.n_i*self.nh_max*T[i])/((self.l_rh+self.l_vent+self.l_hepa+self.l_UV)*self.V)))*100
            
            p1 = plt.figure()
            plt.plot(T,Prob,"b--")
            plt.title("Infection probability")
            plt.xlabel('Time [h]',fontsize=14)            
            plt.ylabel('Infection probability [%]',fontsize=14) 
        
        
        
        
        
        
        
        
        
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")            
        
        path = './RESULTS/'
           
        isFile = os.path.exists(path)
        
        if (isFile == True):            
            # os.mkdir(path)
            plt.savefig(path+ "infection-" + dt_string + '-' +f'{self.username}' + ' .pdf')
            
        if (isFile == False):            
            os.mkdir(path)
            plt.savefig(path+ "infection-" + dt_string + '-' +f'{self.username}' + ' .pdf')    
        
        
        
    #    outfile2.write("========================================================================================" + "\n")
    #    outfile2.write("========================================================================================" + "\n")
    #    outfile2.write("========================================================================================" + "\n")
    #    outfile2.close()    
            
        return self.P0, self.P, self.g, self.ceq, self.nh_max

#function to save the results of the evaluation in a text file
    def saveFile(self):
       
        self.calculation()   
        self.riskEvaluation()
        #print(self.P)
     #   c = self.X[self.n_step]
        name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File',"","*.txt")             #file with the results
        if name:
            with open(name[0],'a') as outfile:
                
                now = datetime.now()
                self.dt_string = now.strftime("%d/%m/%Y %H:%M:%S")                        
                outfile.write(self.dt_string +'\n')
                outfile.write(f'===========================USER==========================='+'\n')
                outfile.write(f'The evaluation has been carried out by: {self.username}' + " " f'{self.usersurname}' +"\n")
                outfile.write(f'Structure: {self.pres}'+"\n")
                outfile.write(f'Department: {self.ssd}'+"\n") 
                outfile.write(f'Room: {self.room}'+"\n")               
                
                
                
                
                outfile.write(f'===========================INPUT PARAMETERS==========================='+'\n')
                outfile.write(f'Room volume: {self.V:.1f} m3' +'\n')
                
                if (self.n_h != 0):
                    outfile.write(f'Number of occupants: {self.n_h + self.n_i}' +'\n')
                outfile.write(f'Number of infectious individuals: {self.n_i}' +'\n')
                
                if (self.m != ""):
                    outfile.write(f'Category of susceptibles: {self.m}' +'\n')
                
                outfile.write(f'Resident time: {self.time} h' +'\n')
                
                outfile.write(f'Air exchange per hour:  {self.l_vent} h-1' + "\n")
                
                outfile.write(f'The RH and the corresponding virus decay constant: {self.rh*100}% and {self.l_rh:.3f} h-1 ' +'\n')
                
                if (self.checkBox_4.isChecked() == True):
                    outfile.write("The room is equipped with HEPA filters" + "\n")
                
                if (self.checkBox.isChecked() == False):
                    outfile.write(f'No masks have been used' +'\n')
                else:
                    outfile.write(f'The occupants wore the following masks:'+ self.comboBox_8.currentText() +'\n')
                    
                if (self.comboBox_6.currentText() != "Select infectious individuals' activity"):    
                    outfile.write(f'The infectious individuals do the following activity: {self.comboBox_6.currentText()}' +'\n')
                
                if (self.comboBox_7.currentText() != "Shedder's category"):
                    outfile.write(f'The shedder category: {self.comboBox_7.currentText()}' +'\n')
                
                
                    
                outfile.write(f'===========================RISK EVALUATION===========================' + "\n")
                outfile.write(f'The probability of no infection: {self.P0:.1f}% ' +'\n')
                outfile.write(f'The probability that at least one individual is infected: {self.P:.1f}%' +'\n')
                
                if (self.g > self.n_i) and (self.P != 100) and (self.n_h !=0):
                    
                    #minimum ventilation
                    lmin = -self.l_rh  - self.l_hepa - self.l_UV + (1-self.alpha)*(1-self.beta)*self.r*self.b*self.n_i*(self.n_h)*self.time/(self.V*np.log((self.n_h)/(self.n_h-self.n_i)))
                    
                    #maximum resident time
                    tmax = np.log((self.n_h)/(self.n_h-self.n_i))*((self.l_rh+self.l_vent+self.l_hepa+self.l_UV)*self.V)/((1-self.alpha)*(1-self.beta)*self.r*self.b*self.n_i*(self.n_h))
                    
                    if (tmax > 0.0003):
                        outfile.write(f'Keeping the same air ventilation, the maximum resident time allowed is: {tmax:.1f} h' +'\n') 
                    if (lmin <= 20) :
                        outfile.write(f'Keeping the same resident time, the recommended ventilation is: {lmin:.0f} h-1' +'\n')
                     
                elif (self.g > self.n_i) and (self.P != 100) and (self.n_h == 0):
                    
                    #minimum ventilation
                    lmin = -self.l_rh  - self.l_hepa - self.l_UV + (1-self.alpha)*(1-self.beta)*self.r*self.b*self.n_i*(self.nh_max)*self.time/(self.V*np.log((self.nh_max)/(self.nh_max-self.n_i)))
                    
                    #maximum resident time
                    tmax = np.log((self.nh_max)/(self.nh_max-self.n_i))*((self.l_rh+self.l_vent+self.l_hepa+self.l_UV)*self.V)/((1-self.alpha)*(1-self.beta)*self.r*self.b*self.n_i*(self.nh_max))
                    
                    if (tmax > 0.0003):
                        outfile.write(f'Keeping the same air ventilation, the maximum resident time allowed is: {tmax:.1f} h' +'\n') 
                    if (lmin <= 20) :
                        outfile.write(f'Keeping the same resident time, the recommended ventilation is: {lmin:.0f} h-1' +'\n')    
                    
                    
               # outfile.write(f'Equilibrium viral concentration: {self.ceq:.3f} quanta/m3'+'\n')  
                outfile.write(f'Viral concentration in the room: {self.c:.3f} quanta/m3'+'\n')
                
                
                if (self.c == self.ceq):
                    outfile.write(f'The maximum viral concentration has been reached' + '\n')
                    
                if (self.c != self.ceq):
                    outfile.write(f'The maximum viral concentration has not been reached' + '\n')    
                    
                #time to let the concentration decay till 1% of that reached during the room occupation 
                tmin = -np.log(0.01)/((self.l_rh+self.l_vent+self.l_hepa+self.l_UV))  
                outfile.write(f'The time after which the room might be occupied again: {tmin:.1f} h' +"\n")
                
                if (self.nh_max < self.n_h) and (self.n_h != 0):    
                    outfile.write(f'The number of susceptible individuals allowed to keep the infection probability under 10% is: {self.nh_max:.0f}'+"\n")
                elif (self.n_h == 0 and self.nh_max !=0):
                    outfile.write(f'The number of susceptible individuals allowed in the room is: {self.nh_max:.0f}'+"\n")
                    outfile.write(f'Number of potential infected: {self.g:.1f}' + '\n')
            
            
                outfile.write(f'===========================CO2 CONCENTRATION ESTIMATE===========================' + "\n")
                if (self.n_h != 0):
                    outfile.write(f'The CO2 concentration in the room is: {410*(1 - exp(-self.l_vent*self.time)) + ((1-self.alpha)*self.n_i+(1-self.beta)*self.n_h)*18216*(1-exp(-self.l_vent*self.time))/(self.V*self.l_vent):.1f} ppm' + "\n")
                    outfile.write(f'The CO2 equilibrium concentration in the room is: {(self.n_i+self.n_h)*18216/(self.l_vent*self.V) + 410:.1f} ppm' + "\n")
                if (self.n_h == 0):
                    outfile.write(f'The CO2 concentration in the room is: {410*(1 - exp(-self.l_vent*self.time)) + ((1-self.alpha)*self.n_i)*18216*(1-exp(-self.l_vent*self.time))/(self.V*self.l_vent):.1f} ppm' + "\n")
                    outfile.write(f'The CO2 equilibrium concentration in the room is: {(self.n_i)*18216/(self.l_vent*self.V) + 410:.1f} ppm' + "\n")
                outfile.write("========================================================================================" + "\n")
                outfile.write("========================================================================================" + "\n")
                outfile.write("========================================================================================" + "\n")
                
             
                
                
                
                
                outfile.close()    
                
                
                
        outfile1 = open("logbook.txt", 'a')
        now1 = datetime.now()
        dt_string1 = now1.strftime("%d/%m/%Y %H:%M:%S")
        outfile1.write("The GUI version is that of 21/10/2022, quanta emission rates are collected in: https://doi.org/10.1177/1420326X211039544" + "\n")
        outfile1.write(dt_string1 + "--" + self.usersurname + ": "+ self.pres + " -- " + self.room + " " + name[0] + "\n")
        outfile1.write("============================================================================================================================================" + "\n")
        
        outfile1.close()                    

#function to open the pop-up window with the table of quanta emission rate                              
    def infobox(self):
        self.w = Dialog()
        self.w.setWindowIcon(QtGui.QIcon(':/img/corona-virus.jpg'))
        self.w.show()                              
                              
#function to clear the graph
    def reset(self):
        self.PlotWidget.clear()
                               
                              
                              
                              
                              
app = QtWidgets.QApplication(sys.argv)
w = MainWindow()    
w.showMaximized()

app.exec()
