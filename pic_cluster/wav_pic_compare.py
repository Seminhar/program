# -*- coding: utf-8 -*-
"""
Created on Thu May 17 00:50:28 2018

@author: Administrator
"""
from __future__ import division
import sys
import math
import numpy as np
sys.path.append("E:\Python\program\ComputerVision")
sys.path.append("E:\Python\program\Tools")
import fileTools as ft


add_pic='E:\\python\\pic\\201710162100\\'
add_outArray_picCluster="E:\\Python\\cluster result\\201710162100\\201710162100.npy"
add_outArray_screenTxtCluster="E:\\Python\\cluster result\\201710162100\\201710162100_t.npy"
add_inArray_wav='E:/python/audio/wav/201710162100/201710162100.npy'

total_begin=1
#图片总量  16571
total_Pic=ft.FileCount(add_pic)
movie_length=23*60+59

def DurationTime(end_Time,start_Time):
    
    duration_Time = end_Time-start_Time

    return duration_Time

def toTimepoint(array_pic):
    index_P=0
    index_L=1
    b_length=len(array_pic)
    Array_TimePoint=[]
    for i in range(0,b_length): 
        count=0      
        if(i<b_length):            
            if((index_P==i)&(index_L<b_length)&(index_P<b_length)):                                
                start_Pic=array_pic[index_P]
                end_Pic=array_pic[index_L]    
                end_Time =math.floor((end_Pic/total_Pic)*movie_length)             
                Array_TimePoint.append(end_Time)
                
                index_P=index_P+count+2                
                index_L=index_L+2
            else:
                continue
    return  Array_TimePoint 

def compare_fusion(array_wav_time,array_pic_time):
    
    print array_wav_time
    print array_pic_time
    tmp = [val for val in array_wav_time if val in array_pic_time] #交集
    print tmp
    print list(set(array_wav_time).difference(set(array_pic_time)))  #差集
    return tmp
if __name__=="__main__":
 
    array_screenTxt=np.load(add_outArray_screenTxtCluster)
    array_wav_time=np.load(add_inArray_wav)         #加载音频的处理结果
    array_pic_time=toTimepoint(array_screenTxt) #转换成时间点
    
    wav_pic_time=compare_fusion(array_wav_time,array_pic_time) #音频时间点和图片融合时间点
    
    