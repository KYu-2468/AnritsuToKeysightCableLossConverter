import sys
import os

from tkinter import Tk
from tkinter.filedialog import askdirectory
path = askdirectory(title='Select Folder') # shows dialog box and return the path
#print(path)
#path = "C:/Users/Kevin_Yu_01/Desktop/Python_Test/Loss_Coverter"
dir_list = os.listdir(path)
for file in dir_list:
    if '.cbl' in file:
        input_file = open(path+ '/' + file,"r")
        lines = input_file.readlines()
        new_file = file.replace('.cbl','.xml')
        output_file = open(path + '/' + new_file,'w')
        output_file.write("""<?xml version="1.0" encoding="utf-8"?>
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
  </Header>""")
        output_file.write('\n')
        output_file.write('  <Measures>')
        output_file.write('\n')
        start = False
        for line in lines:
            line = line.replace('\n','')
            if start == True and 'Frequency' not in line:
                output_file.write('    <Measure>')
                output_file.write('\n')
                output_file.write('      <Frequency>')
                output_file.write(line[0:line.find(',')])
                output_file.write('</Frequency>')
                output_file.write('\n')
                output_file.write('      <Gain>')
                output_file.write('-')
                output_file.write(line[line.find(',')+1:])
                output_file.write('</Gain>')
                output_file.write('\n')
                output_file.write('      <Phase>NaN</Phase>')
                output_file.write('\n')
                output_file.write('    </Measure>')
                output_file.write('\n')
            if 'Rx' in line:
                start = True

        input_file.close()
        output_file.write('  </Measures>')
        output_file.write('\n')
        output_file.write('</Calibration>')
        output_file.write('\n')
        output_file.close()
