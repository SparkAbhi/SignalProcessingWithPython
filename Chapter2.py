#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: A K Agrawal
Email : kumarabhishekbh8@gmail.com
"""
"""
Description: 
    1. create sin signal
    2. add noise to this signal
    3. sample noisy signal
    4. create a digital filter using scipy 
    5. filter using created filter
    6. reconstruct using DAC and simulate analog filter after dac output
"""

from signalUtility import functionGenerator
from signalUtility import oscilloscope
from signalUtility import sampler
from signalUtility import reconstructor
from scipy import signal as scipySignal
from copy import copy
import sys
import numpy as np

# Create three different types waveform 
f1 = functionGenerator()
s1= copy(f1.sinWaveformGenerate(frequency = 100, noOfCycle=20, phase = 0))
# Add gaussian noise to signal 1
s2 = copy(f1.addNoise(s1,noiseType='gaussian', parameter1=0,parameter2=0.1))
# sample noisy signal, sampling frequency is 10 times of original signal about original signal
# this is s2 signal which we will be getting in real scenario, we assume that we have some idea
# (like it's frequency, if we don't have any previous information we can visualise the signal and try to extract some info) so we will be able to design filter.
adc = sampler()
samplingFrequency=1000
s3 =  copy(adc.sampleSignal(s2,samplingFrequency=samplingFrequency))

o1=oscilloscope(title='Signal Visualisation')
o1.addWaveform(s1,plotColor='C0', plotLabel='Original Signal')
o1.addWaveform(s2,plotColor='C1', plotLabel='Noisy signal')
o1.addWaveform(s3,plotType='discrete',plotColor='C2', plotLabel='sampled discrete signal')

#******************************************************************************
"""
Digital filter design:
    we will use 4th order butter worth  low pass filter with cutoff at 200hz
"""
# filter design
 
lowPassFilterCutoff = 200
fc = lowPassFilterCutoff/samplingFrequency;
wc = fc *(2*np.pi) 
nyquistFrequency = np.pi
wc_normalized = wc/nyquistFrequency

b,a = scipySignal.butter(4,wc_normalized,btype='low',output='ba',analog=False)

# plot frequency response of filter
w,h =  scipySignal.freqz(b,a)
o2 = oscilloscope(title='frequencyresponse',isFreqResponsePlotAlso='yes')
o2.addFrequencyResponse(w,h,wc)

#******************************************************************************
# filtering of sampled data, filter will filter only values
s4 = copy(s3)
s4.value = copy(scipySignal.filtfilt(b,a,s3.value,method='pad'))

o1.addWaveform(s4,plotType='discrete',plotColor='C3', plotLabel='filtered discrete signal')

dac = reconstructor()

s5 = copy(dac.reconstructSignal(s4,connectFilter='no'))
s6 = copy(dac.reconstructSignal(s4,connectFilter='yes',lowPassCutoff=500))

o1.addWaveform(s5,plotColor='C4', plotLabel='reconstructed signal')
o1.addWaveform(s6,plotColor='C5', plotLabel='analog filtered reconstructed signal')

# filter performance view
o3 = oscilloscope('filter performance')
o3.addWaveform(s1,plotColor='C0', plotLabel='Original Signal')
o3.addWaveform(s2,plotColor='C1', plotLabel='Noisy signal')
o3.addWaveform(s6,plotColor='C5', plotLabel='analog filtered reconstructed signal')

sys.exit('Break program here')


