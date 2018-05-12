#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: A K Agrawal
Email: kumarabhishekbh8@gmail.com
"""
"""
Description:
    In this file tutorial we will seperate 3 sinosoidal wave from a mixture using frequency domain technique
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
import scipy.fftpack as scipyFFT

# create analog signals.
"""
time duration of each signal = 0.3 sec
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

o1 = oscilloscope(title="plots",isSubPlot='yes')
o1.createSubplots(noOfRows=2,noOfColumns=2)
o1.addToSubplot(s,addToRows=0,addToColumns=0,plotTitle="analog signal to be analysed")

#FFT calculation  for Signal
signalLen = len(s_sampled.time)
fftLen=(int)(pow(2,np.ceil(np.log2(signalLen))))

fftPoints = copy(scipyFFT.fft(s_sampled.value,n=fftLen))
freq = np.linspace(0,Fs,fftLen,endpoint=False)

o2 = oscilloscope(title="Frequency Response (FFT)",isFreqResponsePlotAlso='yes')
o2.addFrequencyResponse(freq,fftPoints,wc=Fs/2,freqView='linear',ampView='linear',label="signal FFT, analog freq vs amplitude")

# filter design
"""
filter 1: cutoff of filter is 30 hz ( low pass filter ) 
filter 2: cutoff is 70 and 130  (band pass filter )
filter 3: cutoff is 900hz and 1100hz( band pass , highpass filter for 1000hz and low pass for noises)
"""
nyquistFrequency = np.pi
df2afratio= Fs/(2*np.pi) #digital frequency to analog frequency conversion ratio
# filter1
fc11=30
wc11 = (fc11/Fs)*(2*np.pi)
wc11_normalised = wc11/nyquistFrequency;

b1,a1 = scipySignal.butter(4,wc11_normalised,btype='low')
w1,h1 = scipySignal.freqz(b1,a1,worN=fftLen,whole=True)

w1_analog = w1*df2afratio
o2.addFrequencyResponse(w1_analog,h1,wc=fc11 ,freqView='linear',ampView='log',frequencyResponseColor='C1',label="filter1 response, analog freq vs amplitude in db")

# filter2
fc21=70
fc22=130
wc21 = (fc21/Fs)*(2*np.pi)
wc22 = (fc22/Fs)*(2*np.pi)
wc21_normalised = wc21/nyquistFrequency
wc22_normalised = wc22/nyquistFrequency

b2,a2 = scipySignal.butter(4,[wc21_normalised,wc22_normalised],btype='bandpass')
w2,h2 = scipySignal.freqz(b2,a2,worN=fftLen,whole=True)

w2_analog = w1*df2afratio
o2.addFrequencyResponse(w2_analog,h2,wc=[fc21,fc22] ,freqView='linear',ampView='log',frequencyResponseColor='C2',label="filter2 response, analog freq vs amplitude in db")

# filter3
fc31=900
fc32=1100
wc31 = (fc31/Fs)*(2*np.pi)
wc32 = (fc32/Fs)*(2*np.pi)
wc31_normalised = wc31/nyquistFrequency
wc32_normalised = wc32/nyquistFrequency

b3,a3 = scipySignal.butter(4,[wc31_normalised,wc32_normalised],btype='bandpass')
w3,h3 = scipySignal.freqz(b3,a3,worN=fftLen,whole=True)

w3_analog = w1*df2afratio
o2.addFrequencyResponse(w3_analog,h3,wc=[fc31,fc32] ,freqView='linear',ampView='log',frequencyResponseColor='C3',label="filter3 response, analog freq vs amplitude in db")


#filtering   of signal1
filtered_10Hz_FFTAmplitude = np.multiply(fftPoints,h1)
ifft_10Hz_Signal = copy(np.real(scipyFFT.ifft(filtered_10Hz_FFTAmplitude ,fftLen)))
ifft_10Hz_Signal = copy(ifft_10Hz_Signal[np.arange(0,len(s_sampled.time))])

filtered_10Hz_DiscreteSignal =  signalType(time =s_sampled.time,value = ifft_10Hz_Signal)

#filtering   of signal2
filtered_100Hz_FFTAmplitude = np.multiply(fftPoints,h2)
ifft_100Hz_Signal = copy(np.real(scipyFFT.ifft(filtered_100Hz_FFTAmplitude ,fftLen)))
ifft_100Hz_Signal = copy(ifft_100Hz_Signal[np.arange(0,len(s_sampled.time))])

filtered_100Hz_DiscreteSignal =  signalType(time =s_sampled.time,value = ifft_100Hz_Signal)


#filtering   of signal3
filtered_1000Hz_FFTAmplitude = np.multiply(fftPoints,h3)
ifft_1000Hz_Signal = copy(np.real(scipyFFT.ifft(filtered_1000Hz_FFTAmplitude ,fftLen)))
ifft_1000Hz_Signal = copy(ifft_1000Hz_Signal[np.arange(0,len(s_sampled.time))])

filtered_1000Hz_DiscreteSignal =  signalType(time =s_sampled.time,value = ifft_1000Hz_Signal)

# reconstruction
dac = reconstructor()
estimatedSignal1 = copy(dac.reconstructSignal(filtered_10Hz_DiscreteSignal,connectFilter='yes',lowPassCutoff=2000))
estimatedSignal2 = copy(dac.reconstructSignal(filtered_100Hz_DiscreteSignal,connectFilter='yes',lowPassCutoff=2000))
estimatedSignal3 = copy(dac.reconstructSignal(filtered_1000Hz_DiscreteSignal,connectFilter='yes',lowPassCutoff=2000))


# plots filtered signal
o1.addToSubplot(estimatedSignal1,addToRows=0,addToColumns=1,plotTitle="filtered 10 Hz signal")
o1.addToSubplot(estimatedSignal2,addToRows=1,addToColumns=0,plotTitle="filtered 100 Hz signal")
o1.addToSubplot(estimatedSignal3,addToRows=1,addToColumns=1,plotTitle="filtered 1000 Hz signal")




