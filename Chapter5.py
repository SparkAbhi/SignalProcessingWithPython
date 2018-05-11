#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: A K Agrawal
Email: kumarabhishekbh8@gmail.com
"""
"""
Description:
    In this tutorial we will a noisy signal using FFT technique 
    signal is noisy sin wave for which we have some idea of it's original frequency. similar to
    chapter 2. the we will create a filter, multiply filter frequency response with signal response and take 
    inverse FFT of result, pass through DAC
"""

from signalUtility import functionGenerator
from signalUtility import oscilloscope
from signalUtility import sampler
from signalUtility import reconstructor
from scipy import signal as scipySignal
from copy import copy
import sys
import numpy as np
import scipy.fftpack as scipyFFT
from signalUtility import signalType


# Create three different types waveform 
f1 = functionGenerator()
s1= copy(f1.sinWaveformGenerate(frequency = 100, noOfCycle=20, phase = 0))
# Add gaussian noise to signal 1
s2 = copy(f1.addNoise(s1,noiseType='gaussian', parameter1=0,parameter2=0.1))
# sample noisy signal, sampling frequency is 10 times of original signal about original signal
# this is s2 signal which we will be getting in real scenario, we assume that we have some idea
# (like it's frequency, if we don't have any previous information we can visualise the signal and try to extract some info) so we will be able to design filter.
adc = sampler()
Fs=10000
s3 =  copy(adc.sampleSignal(s2,samplingFrequency=Fs))

o1=oscilloscope(title='Signal Visualisation')
o1.addWaveform(s1,plotColor='C0', plotLabel='Original Signal')
o1.addWaveform(s2,plotColor='C1', plotLabel='Noisy signal')
o1.addWaveform(s3,plotType='discrete',plotColor='C2', plotLabel='sampled discrete signal')

#FFT calculation  for Signal
signalLen = len(s3.time)
fftLen=(int)(pow(2,np.ceil(np.log2(signalLen))))

fftPoints = copy(scipyFFT.fft(s3.value,n=fftLen))
freq = np.linspace(0,Fs,fftLen,endpoint=False)

o2 = oscilloscope(title="Frequency Response (FFT)",isFreqResponsePlotAlso='yes')
o2.addFrequencyResponse(freq,fftPoints,wc=Fs/2,freqView='linear',ampView='log',label="signal FFT, analog freq vs amplitude")

# filters
lowPassFilterCutoff = 200
fc = lowPassFilterCutoff/Fs
wc = fc *(2*np.pi) 
nyquistFrequency = np.pi
wc_normalized = wc/nyquistFrequency

b,a = scipySignal.butter(4,wc_normalized,btype='low',output='ba',analog=False)

# plot frequency response of filter
w,h =  scipySignal.freqz(b,a,worN=fftLen,whole=True)
w = copy(w*(Fs/(2*np.pi)))
o2.addFrequencyResponse(w,h,wc=lowPassFilterCutoff ,freqView='linear',ampView='log',frequencyResponseColor='C1',label="filter response, analog freq vs amplitude in db")

# filtering
filteredFFTAmplitude = np.multiply(fftPoints,h)
ifftSignal = copy(np.real(scipyFFT.ifft(filteredFFTAmplitude ,fftLen)))
ifftSignal = copy(ifftSignal[np.arange(0,len(s3.time))])

filteredDiscreteSignal =  signalType(time =s3.time,value = ifftSignal)

# reconstruction
dac = reconstructor()
reconstructedFilteredSignal = copy(dac.reconstructSignal(filteredDiscreteSignal,connectFilter='yes',lowPassCutoff=2000))
o1.addWaveform(reconstructedFilteredSignal,plotType='continious',plotColor='C3', plotLabel='filtered signal')




