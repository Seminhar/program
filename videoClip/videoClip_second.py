# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 21:29:38 2017

@author: kaisya
"""
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 17:24:47 2017

@author: kaisya
"""
# =============================================================================
# from __future__ import division
# import numpy as np
# =============================================================================
import subprocess

#b=np.load("F:\\python\cluster result\\201710162100\\201710162100_90.npy")

movie_length=23*60+59
#total_Pic=35981

#b_length=len(b)

def ClipProcess(start_Time,duration_Time):
    
    inFile = "F:\\python\\video\\avi\\201710162100\\201710162100.avi"
    outFile = "F:\\python\\video\\avi_clip\\201710162100_second\\"+str(start_Time)+".avi"
    strcmd="ffmpeg -ss "+str(start_Time)+" -t "+str(duration_Time)+" -accurate_seek -i "+str(inFile)+" -codec copy -avoid_negative_ts 1 "+str(outFile)
    subprocess.call(strcmd,shell=True) 
    print strcmd
    print outFile

def videoClip():
# i=0
    for i in range(0,movie_length,61):    
             start_Time = i;
             duration_Time = 60;
             ClipProcess(start_Time,duration_Time)
      
videoClip()       
   
    
