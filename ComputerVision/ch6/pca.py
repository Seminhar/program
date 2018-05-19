# -*- coding: utf-8 -*-
"""
Created on Fri Feb 09 17:18:01 2018

@author: Administrator
"""
from PIL import Image
from numpy import *
# =============================================================================
# 主成分分析
# =============================================================================
def pca(X):
# =============================================================================
#     输入：矩阵X
#     返回：投影矩阵、方差和均值
# =============================================================================
    #获取维数
    num_data,dim = X.shape  
    #数据中心化
    mean_X  = X.mean(axis=0)
    X = X - mean_X
    
    if dim>num_data:
        M= dot(X,X.T)#协方差矩阵
        e,EV = linalg.eigh(M)#特征值和特征向量
        tmp = dot(X.T,EV).T
        V = tmp[::-1]
        S = sqrt(e)[::-1]
        for i in range(V.shape[1]):
            V[:,i] /= S
    else:
        U,S,V = linelg.svd(X)
        V = V[:num_data]
    return V,S,mean_X
