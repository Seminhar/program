# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 13:16:28 2018

@author: V
"""

import librosa
import numpy as np
import matplotlib.pyplot as plt

#基于静音获得初次检测转变点
def silence_point(path):
    y,fs=librosa.load(path,sr=None)
    ste=[]
    zcc=[]
    detect=[]
    frame_point=[]
    t=20
    frameL=int(fs*t/1000);
    for i in range(0,int(len(y)/frameL)):
        tmp = y[i*frameL:(i+1)*frameL]
        ste.append(sum([k*k for k in tmp]))
        tmp1 = np.multiply(tmp[:-1],tmp[1:])
        zcc.append(sum([1 if i<0  else 0 for i in tmp1]))
#    plt.figure(1)
#    plt.subplot(311)
#    plt.plot(y)
#    plt.title('Speech Signal')
#    plt.xlabel('Sample')   
#    plt.subplot(312)
#    plt.plot(ste)
#    plt.title('Short time energy')
#    plt.xlabel('Frame')
#    plt.subplot(313)
#    plt.plot(zcc)
#    plt.title('Zerocrossing counter')
#    plt.xlabel('Frame')
    t_e=sum(ste)/(len(ste)*0.8)
    vad=[1 if i>t_e else 0 for i in ste]
    for i in range(0,len(ste)):
        detect+=[vad[i]]*frameL
    with_voice=list(np.where(np.array(detect)==1)[0])
    for i in range(len(with_voice)-1):
        if with_voice[i+1]-with_voice[i]>32000:
            frame_point.append(with_voice[i])
    return frame_point,y,fs
    
#基于BIC转变点二次检测
def BIC(ccc):
    y1,x1=ccc.shape[0],ccc.shape[1]
    cc1 = np.cov(ccc)
    value1 = np.linalg.det(cc1)
    
    ccc2=ccc[:,:int(x1/2)]
    ccc3=ccc[:,int(x1/2):]
    
    y2,x2=ccc2.shape[0],ccc2.shape[1]
    cc2 = np.cov(ccc2)
    value2 = np.linalg.det(cc2)
    
    y3,x3=ccc3.shape[0],ccc3.shape[1]
    cc3 = np.cov(ccc3)
    value3 = np.linalg.det(cc3)
    
    R=0.5*(x1*np.log10(value1)-x2*np.log10(value2)-x3*np.log10(value3))
    a=1.2
    p=0.5*a*(y1+0.5*y1*(y1+1))*np.log10(x1)
    ismax=R-a*p
    is_change_point = 1 if ismax>0 else 0
    return is_change_point

    
def BIC_basded_check(point,y,fs):
    detected_point = []
    len_of_check = 16000*10
    for i in point:
        start_point = 0 if i-len_of_check<0 else i-len_of_check
        end_point = len(y)-1 if i+len_of_check>len(y)-1 else i+len_of_check
        check_voice=y[start_point:end_point+1]
        mfcc = librosa.feature.mfcc(y=check_voice,sr=fs,n_mfcc=30,hop_length=80,n_fft=256)
        is_true_change_point=BIC(mfcc)
        if is_true_change_point==1:
            detected_point.append(i/16000)
    return detected_point

if __name__=='__main__':
    path='D:/新闻视频分割/VideoToVoice/wav/201710162100_origin_16000.wav'
    frame_point,y,fs=silence_point(path)
    detected_point=BIC_basded_check(frame_point,y,fs)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    