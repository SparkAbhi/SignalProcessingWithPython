#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author : A K Agrawal
Email: kumarabhishekbh8@gmail.com
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as scipySignal

"""
*******************************************
Signal Defination
Class: signalType
variables: time, value
time is in seconds and value in Volts.
Ex. 
s.time = [0,1,2,3,4,5]sec
s.value = [0.4,0.5,0.2,-0.4,2]volts
*******************************************
"""

#  signalType class defination

class signalType(object):
    def __init__(self, time=[],value=[]):
        self.time = time
        self.value = value

#*******************************************************************************************************
        
"""
Function generator class, which generates some predefined functions for 
specific duration.
input:
    frequency: frequency in Hz
    amplitude: amplitude in V
    offset: offset in volt
    phase: phase in degree
    numberOfCycle: number of cycle to generate
    

triangular wavefor mis integration of square ( when there is no offset for both)
    
"""

#define function generator class
class functionGenerator(object):
    
    # generate 'dataPerSecond' data in 1 sec for Analog signal, generating data will be always descrete, high dataPerSecong make it near to Analog
    def __init__(self,dataPerCycle=100):  
        self.__dataPerCycle = dataPerCycle
        self.signal=signalType()
    def __clearStoredSignal(self):
        self.signal.time=[]
        self.signal.value=[]
        
    def __phaseShifter  (self,frequency = 50 ,phase = 0):
        self.numberOfshiftPoint = np.floor((phase/360)*(self.__dataPerCycle)).astype(int)
        self.signal.value = np.roll(self.signal.value, -1*self.numberOfshiftPoint)
        
    def sinWaveformGenerate(self,frequency = 50,  amplitude = 1, phase = 0, offset = 0, noOfCycle = 10 ):
        self.__clearStoredSignal()
        duration = noOfCycle/frequency
        self.signal.time = np.linspace(0,duration,num=np.floor(self.__dataPerCycle*noOfCycle).astype(int),endpoint=True,dtype=float)
        self.signal.value =amplitude * (np.sin((2*np.pi*frequency)*self.signal.time,dtype=float)) + offset;
        self.__phaseShifter(frequency,phase);
        return self.signal
    
    def pulseWaveformGenerate(self,  frequency=50, amplitude = 1, dutyCycle=0.5, phase = 0, offset=0, noOfCycle=10):
        self.__clearStoredSignal()
        duration = noOfCycle/frequency
        self.signal.time = np.linspace(0,duration,num=np.floor(self.__dataPerCycle*noOfCycle).astype(int),endpoint=True,dtype=float)
        
        primeLength = self.__dataPerCycle
        onLength = np.floor(primeLength*dutyCycle).astype(int)
        primeSignal = np.append(np.ones(onLength), -1*np.ones(primeLength-onLength))
    
        self.signal.value = amplitude*(np.tile(primeSignal,noOfCycle)) + offset
        self.__phaseShifter(frequency,phase);
        
        return(self.signal)
        
    def triangularWaveformGenerate(self,  frequency=50, amplitude = 1, dutyCycle=0.5, phase = 0, offset=0, noOfCycle=10):
        self.__clearStoredSignal()
        duration = noOfCycle/frequency
        self.signal.time = np.linspace(0,duration,num=np.floor(self.__dataPerCycle*noOfCycle).astype(int),endpoint=True,dtype=float)
        
        primeLength = self.__dataPerCycle
        onLength = np.floor(primeLength*dutyCycle).astype(int)
        primeSignal = np.append(np.linspace(-1,1,onLength,endpoint=False), np.linspace(1,-1,(primeLength-onLength),endpoint=False))
    
        self.signal.value = amplitude*(np.tile(primeSignal,noOfCycle)) + offset
        self.__phaseShifter(frequency,phase);
        
        return(self.signal)
        
    def addNoise(self, signal, noiseType='gaussian', parameter1=0, parameter2=1):
        # there are two options for noise type 1) gaussian and 2) uniform
        # for gaussian noise parameter1 is mean  and parameter2 ia standatrd deviation of noise
        # for uniform noise parameter1 is  lowerlimit and parameter2 is upper limit
        # default noiseType is gaussian. if something other than gaussian and uniform is passed in function gaussian noise will be added
        self.__clearStoredSignal()
        self.signal.time=signal.time
        if(noiseType == 'uniform'):
            self.signal.value = signal.value + np.random.uniform(low=parameter1, high=parameter2, size=len(signal.value))
        else:
            self.signal.value = signal.value + np.random.normal(loc=parameter1, scale=parameter2, size=len(signal.value))
        return (self.signal)
            
    
"""
Oscilloscope class display waveform in  a figure
input: 
    signal: signal from functionGenerator of signalType
    plotType: continious or discrete
    plotColor: plot color from colorcyle like C0,C1 
    plotLabel: label for legend
"""

class oscilloscope(object):
    def __init__(self, title="",isFreqResponsePlotAlso='no',isSubPlot='no'):
        if((isSubPlot=='no')and(isFreqResponsePlotAlso=='no')):
            self.__fig1 = plt.figure(figsize=(10,4))
            self.__fig1.canvas.set_window_title(title)
            self.__axes1 = self.__fig1.add_axes([0.1,0.1,0.8,0.8])
            self.__axes1.set_xlabel('time(s)')
            self.__axes1.set_ylabel('Amplitude')
        
        if((isSubPlot=='no')and(isFreqResponsePlotAlso=='yes')):
            self.__createFrequencyResponseFigure()
       
        
    def __createFrequencyResponseFigure(self):
        self.__frequencyResponse = plt.figure(figsize=(10,4))
        self.__frequencyResponse.canvas.set_window_title('frequency response')
        self.__axesf = self.__frequencyResponse.add_axes([0.1,0.1,0.8,0.8])
        self.__axesf.set_xlabel('Frequency')
        self.__axesf.set_ylabel('Amplitude')
        self.__axesf.grid(which='both',axis='both')
        self.__axesf.margins(0,0.1)
        self.__xticks=[]
        self.__xtickLabels=[]
        
    
    def addWaveform(self, signal, plotType='continious', plotColor='C1', plotLabel='Signal'):
        
        if(plotType  == 'continious'):
            self.__axes1.plot(signal.time, signal.value, color=plotColor, label = plotLabel)
        else:
            self.__axes1.stem(signal.time, signal.value, linefmt=plotColor, markerfmt=plotColor+'o',basefmt='black',label=plotLabel)
        
        self.__axes1.grid(True)
        self.__fig1.legend(loc='best')
        self.__fig1.show()
        
        
    def addFrequencyResponse(self,w,h,wc,frequencyResponseColor='C0',freqView='log',ampView='log',label='frequencyResponse'):
        if(freqView =='linear' and ampView =='log'):
            self.__axesf.plot(w,20*np.log10(abs(h)),color=frequencyResponseColor,label=label)
        elif(freqView =='linear' and ampView =='linear'):
            self.__axesf.plot(w,abs(h),color=frequencyResponseColor,label=label)
        elif(freqView =='log' and ampView =='linear'):
            self.__axesf.semilogx(w,abs(h),color=frequencyResponseColor,label=label)
        else:
            self.__axesf.semilogx(w,20*np.log10(abs(h)),color=frequencyResponseColor,label=label)
        
        if(isinstance(wc,list)):
            for wci in wc:
                self.__axesf.axvline(x=wci,color=frequencyResponseColor)
                self.__xticks.append(wci)
                self.__xtickLabels.append(str(round(wci,2)))
        else:
            self.__axesf.axvline(x=wc,color=frequencyResponseColor)
            self.__xticks.append(wc)
            self.__xtickLabels.append(str(round(wc,2)) )     
        
        self.__axesf.set_xticks(self.__xticks)
        self.__axesf.set_xticklabels(self.__xtickLabels)
        self.__frequencyResponse.legend(loc='best')
        self.__frequencyResponse.show()
        
    def createSubplots(self,noOfRows=1,noOfColumns=1):
        self.__subPlotFig, self.__subPlotAxes = plt.subplots(noOfRows,noOfColumns)
        self.__subPlotFig.subplots_adjust(hspace=0.4)
        #self.__subplotFig = plt.figure(figsize=(10,4))
        #self.__subplotFig.canvas.set_window_title(title)
    def addToSubplot(self,signal,addToRows=0,addToColumns=0,plotType='continious',plotColor='C0',plotTitle="plot",xlabel="time",ylabel="value"):
         if(plotType  == 'continious'):
            self.__subPlotAxes[addToRows,addToColumns].plot(signal.time, signal.value, color=plotColor)
         else:
             self.__subPlotAxes[addToRows,addToColumns].stem(signal.time, signal.value, linefmt=plotColor, markerfmt=plotColor+'o',basefmt='black')
        
         self.__subPlotAxes[addToRows,addToColumns].set_title(plotTitle)
         self.__subPlotAxes[addToRows,addToColumns].set_xlabel(xlabel)
         self.__subPlotAxes[addToRows,addToColumns].set_ylabel(ylabel)

"""
class sampler
sample given signal at given sampling frequency
sampleSignal:
    signal-> signal to be sampled
    samplingFrequency -> sampling frequency
    return samples version of signal
"""
class sampler(object):
    def __init__(self):
        self.sampledSignal=signalType()
        
    def sampleSignal(self,signal,samplingFrequency=1000):
        signalDuration=signal.time[-1]-signal.time[0]
        signalLength=len(signal.time)
        # find sampling period in index, signalLength points in samplingDuration so how many points in sampling time? 
        #then for sampling pick 1 data from points coming in sampling duration
        samplingIndexPeriod = np.floor(signalLength/(signalDuration*samplingFrequency)).astype(int)
        sampledDataIndex = np.arange(0,signalLength,samplingIndexPeriod,dtype=int)
        
        self.sampledSignal.time=signal.time[sampledDataIndex]
        self.sampledSignal.value=signal.value[sampledDataIndex]
            
        return self.sampledSignal
    
"""
Clas reconstructtor:
    reconstruct signal based on zero order hold
    filter reconstructed signal to simulate filter after DAC
    we generaly use filter after DAC to filter high frequency  transients.
    DAC pins, wires, connections also act as low pass filter hence zero order reconstructed signal looks smooth.
    
    in this code there is option to connect filter or not, if yes then we can give low pass cutoff,
    by default filtering frequency is 10kHz to simulate pins, wire connections low pass response

   reconstructSignal(self, descreteSignal, connectFilter='yes', lowPassCutoff=10000):
       if we want low pass filtering effect then connectFilter = yes otherwise no.
       if we connect filter then low pass cutoff in Hz, default frequency is 10000 ( 10kHz)
"""
class reconstructor(object):
    def __init__(self):
        self.reconstructedSignal=signalType()
        self.__dataPerSecond = 100000 # a random choice 100k
        
    def __clearStoredSignal(self):
        self.reconstructedSignal.time=[]
        self.reconstructedSignal.value=[]
    
    def reconstructSignal(self, discreteSignal, connectFilter='no', lowPassCutoff=10000):
        self.__clearStoredSignal()             # clear reconstructed signal data before new signal get accumulated. in this case
                                              # it is required because we are using append function hence previous reconstruction data need to be cleared
        noOfDataBetweenConsecutiveSamples = np.floor((discreteSignal.time[1]-discreteSignal.time[0])*self.__dataPerSecond).astype(int)
        timeInterpolationbase=np.linspace(discreteSignal.time[0],discreteSignal.time[1],noOfDataBetweenConsecutiveSamples, endpoint=False) - discreteSignal.time[0]
        
        for index in range(len(discreteSignal.value)):
            interpolatedTime=(timeInterpolationbase + discreteSignal.time[index])
            interpolatedValues=discreteSignal.value[index]*(np.ones(noOfDataBetweenConsecutiveSamples, dtype=float))
            self.reconstructedSignal.time = np.append(self.reconstructedSignal.time, interpolatedTime)
            self.reconstructedSignal.value = np.append(self.reconstructedSignal.value, interpolatedValues)
        
        if(connectFilter == 'yes'):
            self.filterReconstructedSignal(lowPassCutoff)
        
        return self.reconstructedSignal
            
    def filterReconstructedSignal(self,lowPassCutoff):
        fc = (lowPassCutoff*2)/(self.__dataPerSecond)
        b, a = scipySignal.butter(4,fc,btype='low',analog=False,output='ba')
        self.reconstructedSignal.value= scipySignal.filtfilt(b,a, self.reconstructedSignal.value,method='pad')
