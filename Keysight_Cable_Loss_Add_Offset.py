import sys
import os
from tkinter import *
from tkinter import ttk
from tkinter import Tk
from tkinter import messagebox
import tkinter as tk
import tkinter.filedialog as fd

#global values
files = []
new_cable_loss_name = "new_loss.xml"
xml_header = """<?xml version="1.0" encoding="utf-8"?>
<Calibration xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" Version="2.1.1">
  <Header>
    <Date>2022/12/2</Date>
    <Time>00:17:15.0000000-08:00</Time>
    <Source>Keysight Technologies,E7515B,localhost,</Source>
    <Meter>Keysight Technologies,N9040B,US57210121,A.19.55</Meter>
    <Verdict>Pass</Verdict>
    <Temperature>NaN</Temperature>
    <Humidity>NaN</Humidity>
    <Instruments />
  </Header>"""

def select_files():
    filez = fd.askopenfilenames(parent=win, title='Choose a file')
    messagebox.showinfo("Files added", filez)
    files.extend(filez)

def add_offset():
    cable_loss = {0:0}
    i = 0
    path = ''
    for file in files:
        if i == 0:
            cable_loss = keysight_xml_to_dict(file)
            i = 1
            path = file[0:file.rindex('/')+1]
            continue
        else:
            extra_loss = keysight_xml_to_dict(file)
        cable_loss = add_offset_2(cable_loss,extra_loss)
        
    output_file = open(path + new_cable_loss_name, 'w')
    output_file.write(xml_header)
    output_file.write('\n  <Measures>\n')
    for freq in cable_loss:
        output_file.write('    <Measure>\n      <Frequency>')
        output_file.write(str(freq))
        output_file.write('</Frequency>\n      <Gain>-')
        output_file.write(str(round(cable_loss[freq],2)))
        output_file.write('</Gain>\n      <Phase>NaN</Phase>\n    </Measure>\n')

    output_file.write('  </Measures>\n</Calibration>\n')
    output_file.close()
    messagebox.showinfo("Offset Added", path + new_cable_loss_name)

def add_offset_2(cable_loss,extra_loss):
    #adds 2 dict and return final dict
    cable_loss_keys = list(cable_loss.keys())
    extra_loss_keys = list(extra_loss.keys())
    cable_loss_missing = [item for item in extra_loss_keys if item not in cable_loss_keys]
    extra_loss_missing = [item for item in cable_loss_keys if item not in extra_loss_keys]
    cable_loss = standardize_cable_loss(cable_loss, cable_loss_missing)
    extra_loss = standardize_cable_loss(extra_loss, extra_loss_missing)
    for freq in cable_loss:
        cable_loss[freq] += extra_loss[freq]
    
    return cable_loss
    
def standardize_cable_loss(cable_loss, missing_points):
    cable_loss_keys = list(cable_loss.keys())
    for point in missing_points:
        if point < cable_loss_keys[0]:
            # add point freq and gain is same as first
            cable_loss[point] = cable_loss[cable_loss_keys[0]]
            continue
        if point > cable_loss_keys[len(cable_loss_keys)-1]:
            # add point freq and gain is same as last
            cable_loss[point] = cable_loss[cable_loss_keys[len(cable_loss_keys)-1]]
            continue
        past_freq = cable_loss_keys[0]
        for key in cable_loss_keys:
            if point < key:
                cable_loss[point] = calculate_loss(
                    cable_loss, point, past_freq, key)
                break
            past_freq = key
    return dict(sorted(cable_loss.items()))

def calculate_loss(cable_loss, missing, freq1, freq2):
    loss1 = cable_loss[freq1]
    loss2 = cable_loss[freq2]
    result = ((missing-freq1)*(loss2 - loss1) / (freq2 - freq1) + loss1)
    return result

def keysight_xml_to_dict(file):
    cable_loss = {}
    input_file = open(file, "r")
    lines = input_file.readlines()
    frequency = 0
    gain = 0
    for line in lines:
        line = line.replace('\n', '')
        if '<Frequency>' in line:
            frequency = line.replace('<Frequency>', '')\
                        .replace('</Frequency>', '').replace(' ','')
        if '<Gain>' in line:
            gain = line.replace('<Gain>', '').replace('-', '')\
                        .replace('</Gain>', '').replace(' ', '')
            cable_loss[int(frequency)] = float(gain)
    return cable_loss

def clear_files():
    messagebox.showinfo("Files cleared", files)
    files.clear()

#Create an instance of Tkinter frame
win= Tk()

#Set the geometry of Tkinter frame
win.geometry("250x250")

#Create a Button to validate Entry Widget
ttk.Button(win, text= "Select/Add files",width= 20,command= select_files).pack(pady=20)
ttk.Button(win, text= "Add offset",width= 20, command= add_offset).pack(pady=20)
ttk.Button(win, text= "Clear files",width= 20,command= clear_files).pack(pady=20)

win.mainloop()
