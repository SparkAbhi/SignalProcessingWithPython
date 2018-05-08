#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: A K Agrawal
Email  : kumarabhishekbh8@gmail.com
"""
"""
Description:
    1. we will use functions developed in signalUtility
    2. Objective is to get familier with signalUtility
    3. Construct sign, square and triangular waveform
    4. add uniform and gaussian noise to sin waveform
    5. sample sin signal using sampler module
    6. reconstruct using reconstructor module 
    7. simulate low pass filter effect at the output of DAC
"""

from signalUtility import functionGenerator
from signalUtility import oscilloscope
from signalUtility import sampler
from signalUtility import reconstructor
from copy import copy
import sys

# Task 1, create three different types waveform 
f1 = functionGenerator()
s1= copy(f1.sinWaveformGenerate(frequency = 100, noOfCycle=10, phase = 0))
s2= copy(f1.pulseWaveformGenerate(frequency=50,phase=180,noOfCycle=5,dutyCycle=0.5, offset=0, amplitude=0.5))
s3= copy(f1.triangularWaveformGenerate(frequency=50,phase=90,noOfCycle=10,dutyCycle=0.5, offset=0, amplitude=0.5))

o1=oscilloscope(title='Signal Visualisation')
o1.addWaveform(s1,plotColor='C0', plotLabel='S1')
o1.addWaveform(s2,plotColor='C1', plotLabel='S2')
o1.addWaveform(s3,plotColor='C2', plotLabel='S3')


# task 2, add noise to signal 1
s4 = copy(f1.addNoise(s1,noiseType='gaussian', parameter1=0,parameter2=0.1))
s5 = copy(f1.addNoise(s1,noiseType='uniform', parameter1=-0.1,parameter2=0.1))

o2=oscilloscope(title='Noisy Signal Visualisation')
o2.addWaveform(s1,plotColor='C0', plotLabel='S1')
o2.addWaveform(s4,plotColor='C1', plotLabel='gaussian noise added with signal')
o2.addWaveform(s5,plotColor='C2', plotLabel='uniform noise added with signal')


# Task 3, sampling and reconstruction

adc = sampler()
s6 =  copy(adc.sampleSignal(s1,samplingFrequency=1000))

o3=oscilloscope(title='Signal sampling and reconstruction Visualisation')
o3.addWaveform(s1,plotType='continious',plotColor='C0', plotLabel='original signal')
o3.addWaveform(s6,plotType='discrete',plotColor='C2',plotLabel='sampled signal')


dac  =  reconstructor()
s7= copy(dac.reconstructSignal(s6))
s8 = copy(dac.reconstructSignal(s6,connectFilter='yes',lowPassCutoff=200))

o3.addWaveform(s7,plotType='continious',plotColor='C3', plotLabel='reconstructed signal without filter')


o3.addWaveform(s8,plotType='continious',plotColor='C4', plotLabel='reconstructed signal with low pass filter')

sys.exit('Break program here')
