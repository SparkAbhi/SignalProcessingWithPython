#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: A K Agrawal
Email: kumarabhishekbh8@gmail.com
"""
"""
Description:
    In this file tutorial we will seperate 3 sinosoidal wave from a mixture.
    input is addition of 3 sinosoidal wave of 10Hz, 100hz and 1000hz and noise.
    we have idea about there frequencies so by constructing 3 filters  we will seperate signals of known frquencies
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
s_sampled = adc.sampleSignal(s,samplingFrequency=Fs)

"""
o1 = oscilloscope(title = 'individual signals')
o1.addWaveform(s_10,plotColor='C0',plotLabel='10Hz signal')
o1.addWaveform(s_100,plotColor='C1',plotLabel='100Hz signal')
o1.addWaveform(s_1000,plotColor='C2',plotLabel='1000Hz signal')

o2 = oscilloscope(title = 'mixed and noisy signal')
o2.addWaveform(s_add,plotColor='C0',plotLabel='mix signal')
o2.addWaveform(s,plotColor='C1',plotLabel='noisy mix signal')
o2.addWaveform(s_sampled,plotType='discrete',plotColor='C2',plotLabel='sampled noisy mix signal')
"""

# filter design
"""
filter 1: for 10 hz, cutoff of filter is 30 hz ( low pass filter ) 
filter 2: for 100 hz cutoff is 70 and 130  (band pass filter )
filter 3: for  1000 hz cutoff is 900hz and 1100hz( band pass , highpass filter for 1000hz and low pass for noises)
"""
nyquistFrequency = np.pi
# filter1
fc11=30
wc11 = (fc11/Fs)*(2*np.pi)
wc11_normalised = wc11/nyquistFrequency;

b1,a1 = scipySignal.butter(4,wc11_normalised,btype='low')
w1,h1 = scipySignal.freqz(b1,a1)

# filter2
fc21=70
fc22=130
wc21 = (fc21/Fs)*(2*np.pi)
wc22 = (fc22/Fs)*(2*np.pi)
wc21_normalised = wc21/nyquistFrequency
wc22_normalised = wc22/nyquistFrequency

b2,a2 = scipySignal.butter(4,[wc21_normalised,wc22_normalised],btype='bandpass')
w2,h2 = scipySignal.freqz(b2,a2)

# filter3
fc31=900
fc32=1100
wc31 = (fc31/Fs)*(2*np.pi)
wc32 = (fc32/Fs)*(2*np.pi)
wc31_normalised = wc31/nyquistFrequency
wc32_normalised = wc32/nyquistFrequency

b3,a3 = scipySignal.butter(4,[wc31_normalised,wc32_normalised],btype='bandpass')
w3,h3 = scipySignal.freqz(b3,a3)


o3 = oscilloscope(title='filter response',isFreqResponsePlotAlso="yes")
o3.addFrequencyResponse(w1,h1,wc=wc11,frequencyResponseColor='C0',label='filter 1')
o3.addFrequencyResponse(w2,h2,wc=[wc21,wc22],frequencyResponseColor='C1',label='filter2')
o3.addFrequencyResponse(w3,h3,wc=[wc31,wc32],frequencyResponseColor='C2',label='filter3')

# filter noisy data s_sampled
s_filter1 = copy(s_sampled)
s_filter1.value = copy(scipySignal.filtfilt(b1,a1,s_sampled.value))

s_filter2 = copy(s_sampled)
s_filter2.value = copy(scipySignal.filtfilt(b2,a2,s_sampled.value))

s_filter3 = copy(s_sampled)
s_filter3.value = copy(scipySignal.filtfilt(b3,a3,s_sampled.value))

dac = reconstructor()
estimatedSignal1 = copy(dac.reconstructSignal(s_filter1,connectFilter='yes',lowPassCutoff=2000))
estimatedSignal2 = copy(dac.reconstructSignal(s_filter2,connectFilter='yes',lowPassCutoff=2000))
estimatedSignal3 = copy(dac.reconstructSignal(s_filter3,connectFilter='yes',lowPassCutoff=2000))

o4 = oscilloscope(title="final estimated signals",isSubPlot='yes')
o4.createSubplots(noOfRows=2,noOfColumns=2)
o4.addToSubplot(s,addToRows=0,addToColumns=0,plotTitle='original signal')
o4.addToSubplot(estimatedSignal1,addToRows=0,addToColumns=1,plotTitle='estimated 10Hz signal')
o4.addToSubplot(estimatedSignal2,addToRows=1,addToColumns=0,plotTitle='estimated 100Hz signal')
o4.addToSubplot(estimatedSignal3,addToRows=1,addToColumns=1,plotTitle='estimated 1000Hz signal')





