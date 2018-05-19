# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 17:24:47 2017

@author: kaisya
"""
from __future__ import division
import numpy as np
import subprocess
import pandas as pd
import datetime as dt
import math


inFileAdd ="E:\\python\\video\\avi\\201710162100\\201710162100.avi"
inArrAdd = "E:\\python\cluster result\\201710162100\\201710162100_t.npy"
outExcelAdd="E:\\python\\video\\avi_clip\\201710162100_0518\\201710162100_0518.xlsx"
outFileAdd = "E:\\python\\video\\avi_clip\\201710162100_0518\\"

b=np.load(inArrAdd)

movie_length=23*60+59
total_Pic=35981

b_length=len(b)

def ClipProcess(start_Time,duration_Time,j):
# =============================================================================
#     start_Time = (start_Pic/total_Pic)*movie_length
#     end_Time = (end_Pic/total_Pic)*movie_length
#     duration_Time = end_Time-start_Time
# =============================================================================     
    inFile = inFileAdd
    outFile = outFileAdd+str(j)+".avi"
    strcmd="ffmpeg -ss "+str(start_Time)+" -t "+str(duration_Time)+" -accurate_seek -i "+str(inFile)+" -codec copy -avoid_negative_ts 1 "+str(outFile)
    subprocess.call(strcmd,shell=True) 
    print strcmd
    print outFile
    
def DurationTime(end_Time,start_Time):
#    start_Time = (start_Pic/total_Pic)*movie_length
#    end_Time = (end_Pic/total_Pic)*movie_length
    duration_Time = end_Time-start_Time

    return duration_Time

def videoClip():
    index_P=0
    index_L=1
    Array_TimePoint=[]
    for i in range(0,b_length): 
        count=0      
        if(i<b_length):            
            if((index_P==i)&(index_L<b_length)&(index_P<b_length)):                                
                start_Pic=b[index_P]
                end_Pic=b[index_L]    
                print "索引I ",i
                print "起始图片 ",start_Pic
                print "结束图片 ",end_Pic
                start_Time = (start_Pic/total_Pic)*movie_length
                end_Time = math.floor((end_Pic/total_Pic)*movie_length)              
                time=DurationTime(end_Time,start_Time)
                while(time<0):
                    print "时长过短 ",time                                                       
                    index_L=index_L+1
                    count=count+1
                    print "count累计 ",count
                    if(index_L<b_length):                        
                        end_Pic=b[index_L]
                        print "更新结束图片位置 ",end_Pic
                    else:
                        break
                    end_Time =math.floor((end_Pic/total_Pic)*movie_length)              
                    time=DurationTime(end_Time,start_Time)
                    print "更新时长 ",time
                    print "更新结束位置 ",index_L
                    print "结束位置",end_Time
                   # end_Pic=b[i+1]                    
                   # DurationTime(start_Pic,end_Pic)
                #break;
                                       
                ClipProcess(start_Time,time,i)
                Array_TimePoint.append(end_Time)
                
                index_P=index_P+count+2                
                index_L=index_L+2
            else:
                continue                                 
    df=pd.DataFrame(Array_TimePoint)                  
    df.to_excel(outExcelAdd)  
videoClip()       
   
 
















   