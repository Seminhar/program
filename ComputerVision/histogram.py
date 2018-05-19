# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 16:00:28 2018

@author: Administrator
"""

from __future__ import division
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from scipy.misc import lena, toimage 

def histeq(im,nbr_bins=256):
    imhist,bins = np.histogram(im.flatten(),nbr_bins,normed= True)
    cdf = imhist.cumsum()   #累积分布函数
    cdf =255*cdf/cdf[-1]    #归一化    
    im2 = np.interp(im.flatten(),bins[:-1],cdf)   #使用累积分布函数的线性插值，计算新的像素值
    plt.figure()
    plt.title("Jpic")
    arr=im2.flatten()
    n, bins, patches = plt.hist(arr, bins=256, normed=1, facecolor='b', alpha=0.75)  
    plt.show()
    return im2.reshape(im.shape),cdf

if __name__=="__main__":
    address="E:\\Python\\pic\\Test\\"
    imgs = Image.open(address + '3388_G.jpg')
    img = imgs.convert('L')
    
    plt.figure()
    plt.title("Spic")
    arr=np.array(img).flatten()
    n, bins, patches = plt.hist(arr, bins=256, normed=1, facecolor='b')  
    plt.show()
    im2,cdf = histeq(np.array(img))
    print im2.shape
#    print img.shape
    img.save(address + '3388_G_l.jpg')
    toimage(im2,255).save(address + '3388_G_z.jpg')
    plt.figure()
    plt.title("L")
    plt.imshow(img)
    
    plt.figure()    
    plt.title("J")
    plt.imshow(im2)
   