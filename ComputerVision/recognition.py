# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 17:11:41 2018

@author: Administrator
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
import cv2
import numpy as np
from pylab import *
import pytesseract
from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
from skimage import data,filters,color,transform
import matplotlib.pyplot as plt 
import difflib  
from scipy.misc import lena, toimage 

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
# 对一幅灰度图象进行直方图均衡化
# =============================================================================
def histeq(im,nbr_bins=256):
    imhist,bins = np.histogram(im.flatten(),nbr_bins,normed= True)
    cdf = imhist.cumsum() #累积分布函数
    cdf =255*cdf/cdf[-1] #归一化    
    im2 = np.interp(im.flatten(),bins[:-1],cdf)#使用累积分布函数的线性插值，计算新的像素值
    
    # plt.figure()
    # plt.subplot(121)
    # plt.imshow(im)
    #
    # plt.subplot(122)
    # plt.imshow(im2)
    # plt.show()
    #
    return im2.reshape(im.shape),cdf
# =============================================================================
# 图象裁剪1/5下半区
# =============================================================================
def segment(im):    
    im_w=im.size[0]
    im_h=im.size[1]    
    x=im_w*(1/5)*1.0
    y=im_h*(4/5)*1.0    
    w=im_w-x
    h=im_h*(1/5)*1.0    
# =============================================================================
#     print im_w
#     print im_h
#     print w
#     print y+h
# =============================================================================
    im1=im.crop((x,y,x+w,y+h))    
# =============================================================================
#     plt.figure()    
#     plt.subplot(121)
#     plt.imshow(im)
#     
#     plt.subplot(122)
#     plt.imshow(im1)    
#     plt.show()
# =============================================================================
    
    return im1
def segmentToPart(im):
    im_w=im.size[0]
    im_h=im.size[1]    
    x=im_w*(1/5)*1.0
    y=im_h*(4/5)*1.0    
    w=im_w-x
    h=im_h*(1/5)*1.0    
    im=im.crop((x,y,x+w,y+h))
    
    im_w=im.size[0]
    im_h=im.size[1]
    x=0
    y=0
    w=im_w-x
    h=im_h*(1/4)*1.0    
    im1=im.crop((x,y,x+w,y+h))
    
    im_w=im.size[0]
    im_h=im.size[1]
    x=0
    y=im_h*(1/4)*1.0 
    w=im_w-x
    h=im_h*(1/3)*1.0
    im2=im.crop((x,y,x+w,y+h))
    
    plt.figure()    
    plt.subplot(121)
    plt.imshow(im1)  
    plt.subplot(122)
    plt.imshow(im2)    
    plt.show()
    return im1,im2
# =============================================================================
# 最大类间方差法       
# =============================================================================
def OTSU_enhance(img_gray, th_begin=0, th_end=256, th_step=1):    
    assert img_gray.ndim == 2, "must input a gary_img"  
  
    max_g = 0  
    suitable_th = 0  
    for threshold in xrange(th_begin, th_end, th_step):  
        bin_img = img_gray > threshold  
        bin_img_inv = img_gray <= threshold  
        fore_pix = np.sum(bin_img)  
        back_pix = np.sum(bin_img_inv)   
        if 0 == fore_pix:  
            break  
        if 0 == back_pix:  
            continue  
  
        w0 = float(fore_pix) / img_gray.size  
        u0 = float(np.sum(img_gray * bin_img)) / fore_pix  
        w1 = float(back_pix) / img_gray.size  
        u1 = float(np.sum(img_gray * bin_img_inv)) / back_pix  
        # intra-class variance  
        g = w0 * w1 * (u0 - u1) * (u0 - u1)  
        if g > max_g:  
            max_g = g  
            suitable_th = threshold  
    return suitable_th
# =============================================================================
# 图象预处理        
# =============================================================================
def image_deal(image_s):
    image=segment(image_s)    
    img=image.convert('L')    
    im2,cdf=histeq(np.array(img))
    #toimage(im2,255).save(address + str(i)+"_histeq"+ '.jpg')
    imgdeno=denoising(img)
    #imgdeno.save(address + str(i)+"_deno"+ '.jpg')
#    thresh1 = OTSU_enhance(array(img))
#    print thresh1
    thresh = filters.threshold_otsu(np.array(im2))
    #print "1",thresh
    #thresh2 = filters.threshold_otsu(np.array(img))
    #print "2",thresh2
    binaImage=binarizing(imgdeno,thresh)
    
    #binaImage.save(address + str(i)+"_bina"+ '.jpg')
    return binaImage

def image_deal2(image_s):
    image1,image2=segmentToPart(image_s)    
    img1=image1.convert('L')
    img2=image2.convert('L')    
    im1,cdf=histeq(np.array(img1))
    im2,cdf=histeq(np.array(img2))
    #toimage(im2,255).save(address + str(i)+"_histeq"+ '.jpg')
    imgdeno1=denoising(img1)
    imgdeno2=denoising(img2)
    #imgdeno.save(address + str(i)+"_deno"+ '.jpg')
#    thresh1 = OTSU_enhance(array(img))
#    print thresh1
    thresh1 = filters.threshold_otsu(np.array(im1))
    thresh2 = filters.threshold_otsu(np.array(im2))
    #print "1",thresh
    #thresh2 = filters.threshold_otsu(np.array(img))
    #print "2",thresh2
    binaImage1=binarizing(imgdeno1,thresh1)
    binaImage2=binarizing(imgdeno2,thresh2)    
    #binaImage.save(address + str(i)+"_bina"+ '.jpg')
    return binaImage1,binaImage2
# =============================================================================
# 文本提取
# =============================================================================
tessdata_dir_config = '--tessdata-dir "D:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'
def textRecg(p1,p2):
    
    t1=pytesseract.image_to_string(p1,lang='chi_sim',config=tessdata_dir_config )
    t2=pytesseract.image_to_string(p2,lang='chi_sim',config=tessdata_dir_config )
    print "文本t1====", t1
    print "文本t2====", t2
    if(len(t1)<=0 and len(t2)<=0):
        print "识别字符长度都为0"
        return -1      
    else:
       ratio=difflib.SequenceMatcher(None, t1, t2).quick_ratio() 
       print "相似度"+str(ratio)
       return ratio
   
def textExtract(img):
    text=pytesseract.image_to_string(img,lang='chi_sim',config=tessdata_dir_config )
    return text

def TextSimilarity(t1,t2):
       ratio=difflib.SequenceMatcher(None, t1, t2).quick_ratio()      
       return ratio
# =============================================================================
# Main
# =============================================================================
 
if __name__=="__main__":
    address='E:\\python\\pic\\test\\'
    pic_begins=3387
    pic_end=4671
    for i in range(pic_begins,pic_end):          
        p1=Image.open(address + str(i)+ '.jpg')
        p1_deal=image_deal2(p1)
        for j in range(i,pic_end):
            p2=Image.open(address + str(j)+ '.jpg')
            p2_deal=image_deal(p2)
            textRecg(p1_deal,p2_deal)









