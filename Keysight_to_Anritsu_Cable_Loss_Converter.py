import sys
import os

from tkinter import Tk
from tkinter.filedialog import askdirectory
path = askdirectory(title='Select Folder') # shows dialog box and return the path
#print(path)
#path = "C:/Users/Kevin_Yu_01/Desktop/Python_Test/Loss_Coverter"
dir_list = os.listdir(path)
for file in dir_list:
    if '.xml' in file:
        input_file = open(path+ '/' + file,"r")
        lines = input_file.readlines()
        new_file = file.replace('.xml','.cbl')
        output_file = open(path + '/' + new_file,'w')
        output_file.write("""[Header]
Version,1.1.0.1
Name,3dB_Combiner
Comment,
Date,2/12/2022 2:29:15 PM
Author,

[Tx]
Frequency[MHz],Level[dB]""")
        output_file.write('\n')
        for line in lines:
            line = line.replace('\n','')
            if '<Frequency>' in line:
                output_file.write(line[line.find('<Frequency>') + 11:line.find('</Frequency>')])
            if '<Gain>' in line:
                output_file.write(',')
                output_file.write(line[line.find('<Gain>') + 7:line.find('</Gain>')])
                output_file.write('\n')
        input_file.close()
        output_file.close()
