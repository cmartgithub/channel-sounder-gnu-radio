#!/usr/bin/python3
#Program that takes in a complex binary file (fc32) of channel impulse response
#and outputs a single pdp plot as png
#comment

import numpy as np
from mpl_toolkits import mplot3d
import scipy
import os
import matplotlib.pyplot as plt
import math
from decimal import *
import argparse
import matplotlib.pyplot as plt
import scipy.fftpack
from scipy.signal import find_peaks
from mpl_toolkits.mplot3d.axes3d import Axes3D
import plotly.graph_objects as go
import pandas as pd
import cmath

#Takes in complex binary file and returns binary data array
def readBin(file_path):
	return np.fromfile(file_path, dtype=np.complex64)

def zero_to_nan(values):
    """Replace every 0 with 'nan' and return a copy."""
    return [float('nan') if x==0 else x for x in values]
#Takes in complex vector and returns magnitude squared
def complexToMagS(c):
    return np.abs(c)**2
#input complex cir data. Discards first and last 20000 samples and averages pdp's
#together
def avg_pdp(data,window,degree):
    pn_len = 2**degree-1
    pdp_mag = complexToMagS(data)
    indices = find_peaks(pdp_mag,distance=2**degree-3)[0]

    #return indices of first peak after 20000
    indices = indices[indices > 20000]
    indices = indices[indices < len(pdp_mag) - 20000]
    start = indices[0]

    avg_pdp = np.zeros(len(pdp_mag))

    count = 0
    temp = np.zeros(pn_len)
    avg_pdp_index = 0
    for i in indices:
        if count < window:
            temp = temp + pdp_mag[i:i+pn_len]
            count = count + 1
        else:
            temp = temp/window
            avg_pdp[avg_pdp_index:avg_pdp_index+pn_len] = temp
            temp = np.zeros(pn_len)
            count = 0
            avg_pdp_index = avg_pdp_index + pn_len

    return avg_pdp[avg_pdp != 0]

#input linear linear measurements to get power in dB
def linearPowerToDecibel(lin_power):
    db_power = []
    for i in range(0,len(lin_power)):
        db_power.append(10*np.log10(lin_power[i]) if lin_power[i] != 0 else np.NaN)
    return db_power

#given a set of pdps, save a png of a single pdp
def makeFig(pdp,degree,name):
    indices = find_peaks(pdp,distance=2**degree-3)[0]
    plt.plot(pdp[indices[20]:indices[20]+2**degree-60])
    plt.xlabel('Delay (\u03BCs)')
    plt.ylabel('Power (dB)')
    plt.title('Sample Power Delay Profile')
    plt.xticks(np.arange(0,260,step=50),['0','2', '4', '6', '8'])
    plt.savefig(name+".png")

def find_multi_peaks(pdp,samp_rate):
    indices = find_peaks(pdp)[0]
    noise = noiseFloor(pdp)
    for i in range(len(indices)):
        if pdp[indices[i]] < noise:
                indices[i] = 0
    indices = [i for i in indices if i !=0]
    time_delays = [float(i)/float(samp_rate)-float(indices[0])/float(samp_rate) for i in indices]
    magnitudes = [pdp[i] for i in indices]
    #remove first path
    time_delays.pop(0)
    magnitudes.pop(0)
    indices.pop(0)
    return time_delays, magnitudes, indices

#Function to find noise floor
def noiseFloor(data):
    return np.average(data)

#input power delay profiles, output mean delay spread, rms delay spread
def delaySpread(pdp,degree,samp_rate):
    indices = find_peaks(pdp,distance=2**degree-3)[0]
    pdp = pdp[indices[0]:indices[-1]]
    mean_delay = 0
    rms_delay = 0
    for i in indices[0:-2]:
        single_pdp = pdp[i:i+2**degree-60]
        time_delays, magnitudes, index = find_multi_peaks(single_pdp,samp_rate)
        mean_delay = mean_delay + np.dot(magnitudes,time_delays)/sum(magnitudes)
    mean_delay = mean_delay/len(indices[0:-2])
    for i in indices[0:-2]:
        single_pdp = pdp[i:i+2**degree-60]
        time_delays, magnitudes, index = find_multi_peaks(single_pdp,samp_rate)
        delays = [(i - mean_delay)**2 for i in time_delays]
        rms_delay = rms_delay + math.sqrt(np.dot(magnitudes,delays)/sum(magnitudes))
    rms_delay = rms_delay/len(indices[0:-2])
    print('mean delay: ' + str(mean_delay) + 's')
    print('rms delay: ' + str(rms_delay) + 's')

def toCSV(array,filename):
	np.savetxt(filename,[array], delimiter=',')

def main():
	#get user input
	parser = argparse.ArgumentParser(description='Binary I/Q channel impulse response to png/CSv')
	parser.add_argument('-p', '--path', type=str,
	help='Directory path to data file')
	parser.add_argument('-w', '--window_size', type=int, default = 100, required = False,
	help='Size of averaging window, default: 100')
	parser.add_argument('-d', '--degree', type=int, default = 8, required = False,
	help='Degree of PN sequence, default: 8')
	parser.add_argument('-s', '--samp_rate', type=int, default = 25*10**6, required = False,
	help='Samp rate default = 25M')
	parser.add_argument('-n', '--name', type=str,  default = 'pdp',
	help='Name your png file, default: pdp')
	parser.add_argument('-c', '--csv', type=str,  default = 'pdp',
	help='Name your CSV file, default: pdp')
	args = parser.parse_args()
	#initialize variableshome
	file_path = args.path
	N = args.window_size
	file_name = args.name
	csv_name = args.csv
	samp_rate = args.samp_rate
	degree = args.degree
	#do work
	data = readBin(file_path)
	avg_cir = avg_pdp(data,N,8)
	pdp = linearPowerToDecibel(avg_cir)
	makeFig(pdp,degree,file_name)
	toCSV(pdp,csv_name+".csv")
	delaySpread(pdp,degree,samp_rate)
if __name__ == "__main__":
    main()
