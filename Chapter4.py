#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: A K Agrawal
Email: kumarabhishekbh8@gmail.com
"""
"""
Description:
    In this tutorial we will calculate fourier transform of discrete signal using FFT
    we will create a analog signal(discrete signal with very high data rate), sample and 
    then compute FFT 
"""

from signalUtility import functionGenerator
from signalUtility import oscilloscope
from signalUtility import sampler
from signalUtility import reconstructor
from signalUtility import signalType
from scipy import signal as scipySignal
from copy import copy
import sys
import numpy as np
import scipy.fftpack as scipyFFT


# create analog signals.
"""
time duration of each signal = 1 sec
to maintain same data length for each signal in 1 sec time duration dataPerCycle has been changed, 
because for addition each should have same length
"""
f_10 = functionGenerator(dataPerCycle=1000)
f_100= functionGenerator(dataPerCycle=100)
f_1000= functionGenerator(dataPerCycle=10)

s_10 = copy(f_10.sinWaveformGenerate(frequency=10,noOfCycle=3))
s_100 =  copy(f_100.sinWaveformGenerate(frequency=100,noOfCycle=30))
s_1000 =  copy(f_1000.sinWaveformGenerate(frequency=1000,noOfCycle=300))

s_add = signalType()
s_add.time = copy(s_10.time)
s_add.value = copy(s_10.value + s_100.value +s_1000.value)

s = copy(f_10.addNoise(s_add,noiseType='gaussian',parameter1=0, parameter2=0.3))

Fs = 10000
adc = sampler()
s_sampled = adc.sampleSignal(s_add,samplingFrequency=Fs)

o1 = oscilloscope(title="Fourier analysis ",isSubPlot='yes')
o1.createSubplots(noOfRows=2,noOfColumns=2)
o1.addToSubplot(s_add,addToRows=0,addToColumns=0,plotTitle='Signals', plotColor='C0')
o1.addToSubplot(s_add,addToRows=0,addToColumns=1,plotTitle='Sampled Signals', plotType='discrete', plotColor='C0')
#FFT calculation
signalLen = len(s_sampled.time)
fftLen=(int)(pow(2,np.ceil(np.log2(signalLen))))

fftPoints = copy(scipyFFT.fft(s_sampled.value,n=fftLen))

freq = np.linspace(0,Fs,fftLen,endpoint=True);
fftSignal = signalType(freq[np.arange(0,fftLen/2,1,dtype=int)],20*np.log10(abs(fftPoints[np.arange(0,fftLen/2,1,dtype=int)])))
o1.addToSubplot(fftSignal,addToRows=1,addToColumns=0,plotTitle='signal FFT', plotColor='C0',xlabel="frequency(Hz)",ylabel="FFT values")

ifftSignalvalue = copy(scipyFFT.ifft(fftPoints,n=fftLen))
ifftSignalvalue = copy(ifftSignalvalue[np.arange(0,signalLen,1,dtype=int)])
ifftSignalTime=(np.arange(0,signalLen,1))/Fs

ifftSignal = signalType(np.abs(ifftSignalTime),ifftSignalvalue)

dac = reconstructor()
reconstructedIfftSignal = copy(dac.reconstructSignal(ifftSignal,connectFilter='yes',lowPassCutoff=2000))

#o1.addToSubplot(ifftSignal,addToRows=1,addToColumns=1,plotType='discrete',plotTitle='inverse FFT', plotColor='C0',xlabel="time")
o1.addToSubplot(reconstructedIfftSignal,addToRows=1,addToColumns=1,plotTitle='inverse FFT reconstructed signal', plotColor='C0')



















