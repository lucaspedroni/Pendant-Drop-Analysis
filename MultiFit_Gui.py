#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author:        Dominik Feucht
#Date of creation:
#Description:



import tkinter as tk
import tkinter.filedialog as fdiag
from numpy import *
import scipy.optimize as spop
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from matplotlib import figure as fig
from matplotlib import widgets as mpwdgt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2TkAgg)
import time
import subprocess
import os
import sys
#import Fit
#import threading
#todo:
#
#
# Create Config File for Settings
# Button für Formel Delete
# Commandline Utilityy
#

class PendantDropGui(tk.Tk):
    def __init__(self, System = "Windows"):
        tk.Tk.__init__(self)
        if System == "Windows":
            self.Fit_Programm_Helper = "Fit.bat"
        else:
            self.Fit_Programm_Helper = "Fit.sh"
        self.Iterations = 1000
        self.SizeWindows = "1280x720"
        self.ListSizeWindows = ["1280x720","600x480"]
        self.ListeDateien = []
        self.Formel_Reihe = 3
        self.Formeln = []
        self.StartWerte = []
        self.EndWerte = []
        self.Params = []
        self.Legend = ["Im Diagramm", "Rechts vom Diagramm"]
        self.Legend_Set = 0
        self.FitThreads = 1
        
        self.data_dict = dict()
        #ROW 0: MAX 5 Colums
        self.FileSelect = tk.Button(self, text="Hinzufuegen von Dateien", width=20, bg="green", command=self._FileSelect)
        self.FileSelect.grid(row=0, column=0, sticky=tk.W)
        self.FileReset = tk.Button(self, text="Neue Dateien einlesen", width = 20, bg="green", command=self._FileReset)
        self.FileReset.grid(row=0, column=1, sticky=tk.W)
        #self.Refresh= tk.Button(self, text="Refresh", width = 20, command=self._Refresh)
        #self.Refresh.grid(row=0, column=2, sticky=tk.W)
        self.Plot = tk.Button(self, text="Plot exp. Data", width=20, command=self._Plot)
        self.Plot.grid(row=0, column=3, sticky=tk.W)
        self.Fit = tk.Button(self, text="Fit and Save PDFs", width=20, command=self._Fit)
        self.Fit.grid(row=0,column=4, sticky=tk.W)
        
        #ROW 1: MAX 5 Columns
        
        self.ShowFiles = tk.Button(self, text="Show Files", width = 20, command=self._ShowFiles)
        self.ShowFiles.grid(row=1, column=0, sticky=tk.W)
        self.Help = tk.Button(self, text="Hilfe", bg="red", width=20, command=self._Help)
        self.Help.grid(row=1,column=1, sticky=tk.W)
        self.Settings = tk.Button(self, text="Einstellungen", width=20, command=self._Settings)
        self.Settings.grid(row=1, column=2, sticky=tk.W)

        self.Plot_Fits = tk.Button(self,text="Fit and Plot Fits", width=20, command=self._PlotFits)
        self.Plot_Fits.grid(row=1, column=4, sticky=tk.W)

        #Fit-Einstellungen
        self.Button_AddFormel = tk.Button(self, text="Neue Formel hinzufuegen", width=20, command=self._AddFormel)
        self.Button_AddFormel.grid(row=2, column=0, sticky=tk.W)
       
        
        self.FormelLabel = tk.Label(self, text="Formel f(x)=")
        self.FormelLabel.grid(row=2, column=1, sticky=tk.W)
        self.StartBereich = tk.Label(self, text="Startwert")
        self.StartBereich.grid(row=2, column=2, sticky=tk.W)
        self.EndBereich = tk.Label(self, text="Endwert")
        self.EndBereich.grid(row=2, column=3, sticky=tk.W)
        self.ParamLabel = tk.Label(self, text="Parameter")
        self.ParamLabel.grid(row=2, column=4, sticky=tk.W)
        
        self._AddFormel()
    
        
        self.update()  
        
    def _Settings(self):    
        SettingFenster = tk.Toplevel()
        def SaveSettings():
            self.Iterations=Entry_Iterations.get()
            if(Legende.get() == "Im Diagramm"):
                self.Legend_Set = 0
            elif(Legende.get() == "Rechts vom Diagramm"):
                self.Legend_Set = 1
            self.FitThreads = Entry_FitThreads.get()
            pass
        def Close():
            SettingFenster.destroy()
        Label_Settings = tk.Label(SettingFenster, text="Einstellungen")
            
        Label_Iterations = tk.Label(SettingFenster, text="Max. Iterationen")
        Label_Iterations.grid(row=1, column=0, sticky=tk.W)
        Entry_Iterations = tk.Entry(SettingFenster)
        Entry_Iterations.grid(row=1, column=1, sticky=tk.W)
        Entry_Iterations.insert(0, "%s"%self.Iterations)
        
        Legende = tk.StringVar()
        Legende.set(self.Legend[self.Legend_Set])
        Label_Legende = tk.Label(SettingFenster, text="Position der Legende")
        Label_Legende.grid(row=2,column=0, sticky=tk.W)
        Selection_Legende = tk.OptionMenu(SettingFenster, Legende, *self.Legend)
        Selection_Legende.grid(row=2, column=1)
        
        Label_FitThreads = tk.Label(SettingFenster, text="Anzahl Threads beim Fitten (1-4)")
        Label_FitThreads.grid(row=3, column=0, sticky=tk.W)
        Entry_FitThreads = tk.Entry(SettingFenster)
        Entry_FitThreads.grid(row=3, column=1, sticky=tk.W)
        Entry_FitThreads.insert(0, "%s"%self.FitThreads)
        
        
        
#        Label_SizeWindows = tk.Label(SettingFenster, text="Aufloesung Fenster")
#        Label_SizeWindows.grid(row=2, column=0, sticky=tk.W)
#        Selection_SizeWindows= tk.Listbox(SettingFenster)
#        Selection_SizeWindows.grid(row=2,column=1)
        
#        for item in self.ListSizeWindows:
 #           Selection_SizeWindows.insert(END, item)
        
        Button_Save = tk.Button(SettingFenster, text="Save", command=SaveSettings)
        Button_Save.grid(row=20,column=0)
        
        Button_Close = tk.Button(SettingFenster, text="Close", command=Close)
        Button_Close.grid(row=20, column=1)

    def _Help(self):
        #Hilfe fenster einblenden lassne!
        HilfeFenster = tk.Toplevel()
        def Button_OK_Click():
            HilfeFenster.destroy()
        HilfeFenster.title("Hilfe")
        Label = tk.Label(master=HilfeFenster, text="Test")
        Label.grid(row=0, column=0, sticky=tk.W)
        buttonOK = tk.Button(master=HilfeFenster, text="OK", command=Button_OK_Click)
        buttonOK.grid(row=5, column=0, sticky=tk.E)
        
    def _PopUp(self, Titel, Text, Array = False, geometry=None):
        if geometry == None:
            geometry = self.SizeWindows
        Start_x = 5
        Start_y = 5
        PopUpFenster = tk.Toplevel()
        PopUpFenster.geometry(geometry)
        def Button_Ok():
            PopUpFenster.destroy()
        PopUpFenster.title(Titel)
        if(Array == False):
            Label = tk.Label(master=PopUpFenster, text=Text)
            Label.place(x=Start_x, y=Start_y, width=1280, height=40)
        elif(Array == True):
            Label = []
            count = 0
            for i in Text:
                Label.append(tk.Label(master=PopUpFenster, text=i))
                Label[count].place(x=Start_x, y=Start_y, width = 1280, height=20)
                Start_y = Start_y + 25
                count = count + 1
                
            
        ButtonOk = tk.Button(master=PopUpFenster, text="OK", command=Button_Ok)
        ButtonOk.place(x=600, y=Start_y+40, width=150, height=20)
        
    def _AddFormel(self):
        self.Formeln.append(tk.Entry(self))
        self.Formeln[self.Formel_Reihe-3].grid(row=self.Formel_Reihe, column=1,sticky=tk.W)
        self.StartWerte.append(tk.Entry(self))
        self.StartWerte[self.Formel_Reihe-3].grid(row=self.Formel_Reihe, column=2, sticky=tk.W)
        self.EndWerte.append(tk.Entry(self))
        self.EndWerte[self.Formel_Reihe-3].grid(row=self.Formel_Reihe, column=3, sticky=tk.W)
        self.Params.append(tk.Entry(self))
        self.Params[self.Formel_Reihe-3].grid(row=self.Formel_Reihe,column=4, sticky=tk.W)
        self.Formel_Reihe = self.Formel_Reihe + 1
        
    def _FileSelect(self):
        tmp_filenames = fdiag.askopenfilenames(title="Choose raw-data", filetypes = (("dpa files", "*.dpa"), ("text files", "*.txt"),("all files", "*.*"))) # Tupel der Dateinamen
        print(tmp_filenames)
        for i in tmp_filenames:
            self.ListeDateien.append(i)
        self._PopUp("Einlesen abgeschlossen", "Das Einlesen der Dateien ist abgeschlossen!", Array=False)    
        
    def _ShowFiles(self):
        self._PopUp("Eingelesene Files", self.ListeDateien, Array=True)
        
    def _RefreshFiles(self):
        for file in self.ListeDateien:
            self._LeseWerteAus(file)
        
    def _FileReset(self):
        self.ListeDateien = []
        self.data_dict = dict()
        tmp_filenames = fdiag.askopenfilenames(title="Choose raw-data", filetypes = (("dpa files", "*.dpa"), ("text files", "*.txt"),("all files", "*.*"))) # Tupel der Dateinamen
        for i in tmp_filenames:
            self.ListeDateien.append(i)
        self._PopUp("Einlesen abgeschlossen", Text="Alte Dateien wurden aus der Liste geloescht.\n Die neuen Dateien wurden fertig eingelesen", Array=False)
        
        
        
    def _Plot(self):
        self._RefreshFiles()
        fig, ax = plt.subplots(figsize=(11,5))
        ax.set_title('Click on legend line to toggle line on/off')
        plt.ylabel("Surface Tension")
        plt.xlabel("time")
        plt.minorticks_on()
        plt.grid(True, which='both')
        
        def button_click():
            pass
        
        def onpick(event):
            legline = event.artist
            origline = lined[legline]
            vis = not origline.get_visible()
            origline.set_visible(vis)
            
            if vis:
                legline.set_alpha(1.0)
            else:
                legline.set_alpha(0.1)
            fig.canvas.draw()
            pass
        
        
        list_lines = []
        
        for file in self.ListeDateien:
            print(file)
            string_name = os.path.basename(file)
            string_name = string_name.split("/")[-1]
            list_lines.append(ax.plot(self.data_dict[file][0], self.data_dict[file][1], label=string_name[:-4])[0])
            
        if(self.Legend_Set == 0):
            leg=ax.legend()  
        elif(self.Legend_Set == 1):
            box = ax.get_position()
            ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])
            leg=ax.legend(loc='center left', bbox_to_anchor=(1,0.5), fancybox=True, shadow=True)
            leg.get_frame().set_alpha(0.6)
        
        lined = dict()
        for legline, origline in zip(leg.get_lines(), list_lines):
            legline.set_picker(5)
            lined[legline] = origline
            
        fig.canvas.mpl_connect('pick_event', onpick)
        plt.show()
        
        button = mpwdgt.Button(plt.axes([0.8,0.05,0.1,0.08]), 'Refresh!')
        button.on_clicked(button_click)
        plt.close()

    def _LeseWerteAus(self, file):
        print(file)
        datei = open("%s"%file, "r")
        zeilen = datei.readlines()
        datei.close()  
        index_start_read = 0
        for zeile in zeilen:
            if zeile[0] == ";":
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
            tmp_x.append(x)
            tmp_y.append(y)
                 
        self.data_dict[file] = [tmp_x,tmp_y]
        
    def _WriteData(self):
        Formel_file = "Formeln.txt"
        Data_file = "DatenListe.txt"
        
        f = open(Formel_file, "w")
        for count in range(0, len(self.Formeln)):
            tmp_formel = self.Formeln[count].get()
            tmp_param = self.Params[count].get()
            tmp_Start = self.StartWerte[count].get()
            tmp_Ende = self.EndWerte[count].get()
            
            f.write("%s___%s___%s___%s\n"%(tmp_formel,tmp_param, tmp_Start, tmp_Ende))
        f.close()
        
        f = open(Data_file, "w")
        for key in self.ListeDateien:
            f.write("%s\n"%key)
        f.close()
        
        pass
        
                
            
    def _Fit(self):
        self._WriteData()
        #print(os.path.dirname(os.path.realpath(__file__)))
        dirpath = os.path.dirname(os.path.realpath(__file__))
        subprocess.call(["%s/%s"%(dirpath,self.Fit_Programm_Helper), "-t%s"%int(self.FitThreads), "-i%s"%int(self.Iterations)], shell=True)
      #  os.system("%s/Fit.py -t%s -i%s"%(dirpath, self.FitThreads, self.Iterations))
#        threading.Thread(target=Fit.main, args=()).start()
        #self._PopUp("Fit fertig", "Alle Fits abgeschlossen", Array=False)
    
        pass
    
    
    def _PlotFits(self):
        pass
        
        
        
def main(args):
    if len(args) > 1:
        args.pop(0)
    if args[0] == "--without-gui" or args[0] == "-w":
        pass
    else:
        app = PendantDropGui()
        app.mainloop()
        
if __name__ == "__main__":
    main(sys.argv)
