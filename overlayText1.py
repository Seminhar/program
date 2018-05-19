# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 16:01:37 2018

@author: kaisya
"""
# =============================================================================
# import sys
# reload(sys)E:\Python\pic\201709302100\316.jpg
# sys.setdefaultencoding("UTF-8")
# =============================================================================
# encoding=utf8
from __future__ import division
import os
import os.path
from PIL import Image
import pytesseract
from PIL import ImageFilter
from PIL import ImageEnhance
import time
import matplotlib.pyplot as plt 
from pylab import *
from skimage import transform,data
# =============================================================================
# 二值化
# =============================================================================
def binarizing(im,threshold):
         pixdata=im.load()
         w,h=im.size
         for j in range(h):
             for i in range(w):
                 if pixdata[i,j]<threshold:
                    pixdata[i,j]=0
                 else:
                     pixdata[i,j]=255
         return im
# =============================================================================
# 图象去噪
# =============================================================================
def denoising(im):
         pixdata=im.load()
         w,h=im.size
         for j in range(1,h-1):
             for i in range(1,w-1):
                   count=0
                   if pixdata[i,j-1]>245:
                      count=count+1
                   if pixdata[i,j+1]>245:
                      count=count+1
                   if pixdata[i+1,j]>245:
                      count=count+1
                   if pixdata[i-1,j]>245:
                      count=count+1
                   if count>2:
                      pixdata[i,j]=255
         return im
# =============================================================================
# 切割
# =============================================================================
def segment(im):    
    im_w=im.size[0]
    im_h=im.size[1]    
    x=0
    y=int(im_h*(4/5)*1.0) 
    w=im_w
    h=int(im_h*(1/5)*1.0)    
    print im_w
    print im_h
    print x+w
    print y+h
    print x
    print int(y)
    im1=im.crop((x,y,x+w,y+h))
    
    plt.figure()    
    plt.subplot(121)
    plt.imshow(im)
    
    plt.subplot(122)
    plt.imshow(im1)    
    plt.show()
    
    return im1         
# =============================================================================
#      
# =============================================================================
        
tessdata_dir_config = '--tessdata-dir "E:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'
#figure()
image_s=Image.open(r'F:\python\pic\201709302100\35812.jpg')
image=segment(image_s)   
img=image.convert('L')
img.save("F:\\python\\pic\\"+"_L"+ '.jpg')

imgdeno=denoising(img)
imgdeno.save("F:\\python\\pic\\"+"_de"+ '.jpg')

thresh = filters.threshold_otsu(array(image_s))
print thresh
imgbina=binarizing(imgdeno,thresh)
imgbina.save("F:\\python\\pic\\"+"_b"+ '.jpg')
reimage=imgbina.resize((768*2,576*2))
reimage.save("F:\\python\\pic\\"+"_rb"+ '.jpg')


plt.subplot(121)
#plt.title(u'原图',fontproperties=font)
plt.axis('off')   #隐藏坐标
plt.imshow(image)
    
plt.subplot(122)
#plt.title(u'灰度图',fontproperties=font)
plt.axis('off')   #隐藏坐标
plt.imshow(imgbina) 
plt.show()

text=pytesseract.image_to_string(array(imgbina),lang='chi_sim',config=tessdata_dir_config)

print text








