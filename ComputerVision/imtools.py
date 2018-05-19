# -*- coding: utf-8 -*-
"""
Created on Thu Feb 08 13:34:39 2018

@author: Administrator
"""
import os
from PIL import Image
from numpy import *

# =============================================================================
# #返回路径下的图象文件
# =============================================================================
def get_imlist(path):
    return [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.jpg')]

# =============================================================================
# #图象缩放，重新定义图象的大小
# =============================================================================
def imresize(im,sz):
    pil_im = Image.array(uint8(im))
    return array(pil_im.resize(sz))

# =============================================================================
# 对一幅灰度图象进行直方图均衡化
# =============================================================================
def histeq(im,nbr_bins=256):
    imhist,bins = histogram(im.flatten(),nbr_bins,normed= True)
    cdf = imhist,cumsum()  #累积分布函数
    cdf =255*cdf /cdf[-1] #归一化
    im2 = interp(im.flatten(),bins[:-1],cdf)
    return im2.reshape(im.shape),cdf
 #参数1、灰度图象，2、小区间的数目
# 使用函数：
# from PIL import Image
# from numpy import *
# 
# im= array(Image.open(path).convert('L'))
# im2,cdf = imtools.histeq(im)
 
# =============================================================================
# 计算列表的平均图象
# =============================================================================
def compute_average(imlist):
    averageim = array(Image.open(imlist[0]),'f')
    for imname in imlist[1:]:
        try:
            averageim += array(Image.open(imname))
        except:
            print imname + '...skipped'
    averageim /= len(imlist)
        
    return array(averageim,'unit8')#返回unit8类型的平均图象
    
    
    
    