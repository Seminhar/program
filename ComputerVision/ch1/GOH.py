# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 13:21:54 2017

@author: kaisya
"""

# -*- coding: utf-8 -*-
from PIL import Image  
from pylab import *  
from PCV.tools import imtools  
''''' 
图像灰度变换中一个非常有用的例子就是直方图均衡化。 
图像均衡化作为预处理操作，在归一化图像强度时是一个很好的方式， 
并且通过直方图均衡化可以增加图像对比度。 
'''  
# 添加中文字体支持  
from matplotlib.font_manager import FontProperties  
font = FontProperties(fname=r"C:/Windows/Fonts/msyh.ttc", size=14)  
  
im = array(Image.open('C:/pytm/pic/ceshi.jpg').convert('L'))  # 打开图像，并转成灰度图像  
#im = array(Image.open('../data/AquaTermi_lowcontrast.JPG').convert('L'))  
im2, cdf = imtools.histeq(im)  
  
figure()  
subplot(2, 2, 1)  
axis('off')  
gray()  
title(u'原始图像', fontproperties=font)  
imshow(im)  
  
subplot(2, 2, 2)  
axis('off')  
title(u'直方图均衡化后的图像', fontproperties=font)  
imshow(im2)  
  
subplot(2, 2, 3)  
axis('off')  
title(u'原始直方图', fontproperties=font)  
#hist(im.flatten(), 128, cumulative=True, normed=True)  
hist(im.flatten(), 128, normed=True)  
  
subplot(2, 2, 4)  
axis('off')  
title(u'均衡化后的直方图', fontproperties=font)  
#hist(im2.flatten(), 128, cumulative=True, normed=True)  
hist(im2.flatten(), 128, normed=True)  
  
show()  