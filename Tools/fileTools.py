# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 20:29:05 2018

@author: kaisya
"""
import os
#filepath="F:\\python\\video\\mp4\\"
#filepath="F:\\python\\pic\\201801180600\\"
#文件路径
def DirFilePath(filepath):
    pathDir =  os.listdir(filepath)
    print len(pathDir)
    for allDir in pathDir:
        child = os.path.join('%s%s' % (filepath, allDir))
        print child.decode('gbk')
        
    return pathDir
    
 #目录下的文件数       
def FileCount(filepath):
    pathDir =  os.listdir(filepath)    
    print "总的个数",len(pathDir)-1
    return len(pathDir)-1

#FileCount(filepath)        
#DirFilePath(filepath)