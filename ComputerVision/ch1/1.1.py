# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 14:58:52 2018

@author: kaisya
"""

from PIL import Image
from pylab import *

# 添加中文字体支持
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"C:\windows\fonts\SimSun.ttc", size=14)
figure()
#打开图片
pil_im = Image.open('E:/python/pic/201710162100/450.jpg')
#gray()
subplot(121)
title(u'原图',fontproperties=font)
axis('off')   #隐藏坐标
imshow(pil_im)
#转换成灰度图像
pil_im = Image.open('E:/python/pic/201710162100/450.jpg').convert('L')
subplot(122)
title(u'灰度图',fontproperties=font)
axis('off')   #隐藏坐标
imshow(pil_im)

show()