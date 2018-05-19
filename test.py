# -*- coding: utf-8 -*-
"""
Created on Mon Feb 05 21:03:06 2018

@author: Administrator
"""
from PIL import Image
from pylab import *

x=[100,100,400,400]
y=[200,500,200,500]
plot(x,y,'r*')

plot(x[:2],y[:2])
plot(x[:4],y[:4])

title('Ploting :"connect node"')

show()