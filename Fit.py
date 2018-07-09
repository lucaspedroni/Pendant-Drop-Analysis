
# -*- coding: utf-8 -*-
#Author:          Dominik Feucht
#Date of creation:
#Description:        
#
#Gehoert zum Programm MultiFit_Gui.py
#
#encoding:

import sys
import os
import threading
import scipy.optimize as spop
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

import time
import tkinter as tk

global Formel_file
global Data_file
Formel_file = "Formeln.txt"
Data_file = "DatenListe.txt"
global Thread_Count
Thread_Count = 0


def Read_Data():
    global Formel_File
    global Data_file
    Formel_List = []
    Data_List = []
    Parameter_List = []
    Start_List = []
    Ende_List = []

    f = open(Formel_file, "r")
    for line in f:
        Formel_List.append(line.split("___")[0])
        Parameter_List.append(line.split("___")[1])
        Start_List.append(float(line.split("___")[2]))
        Ende_List.append(float(line.split("___")[3]))
    f.close()
    
    f = open(Data_file, "r")
    for line in f:
        Data_List.append(line.split("\n")[0])
    f.close()

    return Formel_List, Parameter_List, Start_List, Ende_List, Data_List
    pass

def LeseWerteEin(data, start, ende):
    f = open("%s"%data, "r")
    zeilen = f.readlines()
    f.close()
    index_start_read = 0
    for zeile in zeilen:
        if zeile[0] == ";":
      #      print(zeile)
            index_start_read=zeilen.index(zeile)
        else:
            pass
    
    for i in range(0, index_start_read+1):
        zeilen.pop(0)
        
    tmp_x = []
    tmp_y = []
    for i in range(0, len(zeilen)):
        x = float(zeilen[i].split("\t")[1])
        y = float(zeilen[i].split("\t")[3])
        if x < start:
            continue
        elif x > ende:
            continue
        else:
            tmp_x.append(x)
            tmp_y.append(y)
            
    return tmp_x, tmp_y
        
    pass

def Fit_Funktion(formel, parameter, Werte_Params, x):
    tmp_parameter = parameter.replace(" ","").split(",")
    for i in range(0, len(tmp_parameter)):
        exec("%s = %s"%(tmp_parameter[i], Werte_Params[i]))
    return eval(formel)

def FitKurve(formel, parameter, start, ende, tmp_x, tmp_y, Iterations):
    Werte_X_Fit = []
    Werte_Y_Fit = []
    try:
        Werte_Params, Covariance = spop.curve_fit(eval("lambda x, %s: %s"%(parameter, formel)), tmp_x, tmp_y, maxfev=Iterations)
    except RuntimeError:
        return "RuntimeError", "", ""
    except ValueError:
        return "ValueError", "", ""
    except TypeError:
        return "TypeError", "", ""
    except:
        return "OtherError", "", ""

    for Iterate in tmp_x:
        Werte_X_Fit.append(Iterate)
        Werte_Y_Fit.append(Fit_Funktion(formel, parameter, Werte_Params, Iterate))

    return Werte_Params, Werte_X_Fit, Werte_Y_Fit
    pass
    
def Bericht(formel, start, ende, parameter, Werte_Params, X_Real, Y_Real, X_Fit, Y_Fit, data, ErrorString = None):
    Name_Bericht = "%s"%(data.replace(".dpa","_FIT_%s_%s_%s.txt"%(formel, start, ende)))
    Name_Bild = "%s"%(data.replace(".dpa","_FIT_%s_%s_%s.pdf"%(formel, start, ende)))
    f = open(Name_Bericht, "w")
    f.write("#Formel: %s\n"%formel)
    f.write("#Parameter \t Werte \n")
    if ErrorString != None:
        f.write("\n\n%s"%ErrorString)
        f.close()

    else:
        tmp_param = parameter.replace(" ","").split(",")
        for i in range(0, len(tmp_param)):
            f.write("#%s\t%s\n"%(tmp_param[i],Werte_Params[i]))
            
        f.write("#X_Fit \t Y_Fit \t X_Real \t Y_Real \n")
        for i in range(0, len(X_Real)):
            f.write("%s \t %s \t %s \t %s"%(X_Fit[i],Y_Fit[i],X_Real[i],Y_Real[i]))
            
        f.close()
        plt.plot(X_Fit, Y_Fit, label="FIT")
        plt.plot(X_Real, Y_Real, label="%s"%data.split("/")[-1].replace(".dpa",""))
        plt.grid(True)
        plt.legend()
        plt.savefig(Name_Bild, format="pdf")
        plt.close()
    
    pass
def Fit(formel, parameter, start, ende, data, Iterations):
    global Thread_Count
    Thread_Count = Thread_Count + 1
    X_Real = []
    Y_Real = []
    X_Fit = []
    Y_Fit = []
    X_Real, Y_Real = LeseWerteEin(data, start, ende)
    
    Werte_Params, X_Fit, Y_Fit = FitKurve(formel, parameter, start, ende, X_Real, Y_Real, Iterations)
    if Werte_Params[-5:0] == "Error":
        Error = Werte_Params
    else:
        Error = None
        
    Bericht(formel, start, ende, parameter, Werte_Params, X_Real, Y_Real, X_Fit, Y_Fit, data, Error)
    Thread_Count = Thread_Count - 1
    pass

class FitGUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.Label = tk.Label(self, text="Fits abgeschlossen", width=25)
        self.Button = tk.Button(self, text="Beenden", width=20, command=self.Beenden)
        self.Label.grid(row=0, column=1, sticky=tk.W)
        self.Button.grid(row=1, column=1, sticky=tk.W)
    def Beenden(self):
        self.destroy()
        

def main(Max_Threads = 1, Iterations = 1000):    
    f = open("Start.txt", "w")
    f.write("ok")
    f.close()
    Formeln = []
    Parameter = []
    Start = []
    Ende = []
    Data = []
    Formeln, Parameter, Start, Ende, Data = Read_Data()
#    print(Formeln)
    for count in range(0,len(Formeln)):
        for file in Data:
#            while Thread_Count > Max_Threads:
#                time.sleep(0.5)    
#            threading.Thread(target=Fit, args=(Formeln[count], Parameter[count], Start[count], Ende[count], file, Iterations))
            Fit(Formeln[count], Parameter[count], Start[count], Ende[count], file, Iterations)
#            time.sleep(0.1)
    os.remove(Formel_file)
    os.remove(Data_file)
#    root = FitGUI()
#    root.mainloop()
    

    pass


if __name__ == "__main__":
    main()
            