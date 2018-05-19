# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 11:49:57 2017

@author: win
"""
import sys
import ShotAnalysis as SA
import numpy as np
sys.path.append("E:\Python\program\ComputerVision")
sys.path.append("E:\Python\program\Tools")
import recognition as re
import fileTools as ft
import random
from PIL import Image

add_pic='E:\\python\\pic\\201710162100\\'
add_outArr="E:\\Python\\cluster result\\201710162100\\201710162100.npy"
add_outArrClu="E:\\Python\\cluster result\\201710162100\\201710162100_d.npy"
accept=77
#视频长度  毫秒
time=29*60*60+53*60
#开始 
total_begin=1
#图片总量  16571
total_end=ft.FileCount(add_pic)

frame=5
# =============================================================================
# order_FSX = SA.FilmShotsCut(time,total_begin,total_end,accept,add_pic)
# np.save("E:\\Python\\cluster result\\201709302100\\201709302100.npy",order_FSX)
# 
# =============================================================================
total=[]

new_order=np.array(total,int)
order_FSX=np.load(add_outArr)
order_FSX_R=sorted(set(order_FSX),key=order_FSX.tolist().index)
order_FSX_length=len(order_FSX_R)
# =============================================================================
# new_order_L=0
# index_start1=0
# index_end1=1
# index_start2=2
# index_end2=3
# count=0
# count_0=0
# count_1=0 
# count_null=0
# repeat=0
# p1_p=0
# p1_l=0
# p2_p=0
# p2_l=0
# =============================================================================

# =============================================================================
#  相似度统计与操作           
# =============================================================================   
def similarityCount(ratio,i):
            global count
            global count_0
            global count_1
            global count_null
            global new_order_L
            global new_order
            if(ratio>0.5):            
                count=count+1
                print "相似度为大于0.5的个数",count               
            elif(ratio==-1):
                count_null=count_null+1 
                print "相似度为0的个数",count_null               
            elif(ratio==0 or ratio<=0.5):
                count_0=count_0+1 
                print "相似度为0 或者小于0.5的个数",count_0               
            elif(ratio>=0.7):
                count_1=count_1+1
                print "相似度为大于0.7的个数",count_1
            if(new_order_L>2 and (count_1>=1 or count>=5)):           
                if(new_order[new_order_L-1]==p1_l):
                    new_order[new_order_L-1]=p2_l
                    total=new_order.tolist()
                    print  "%%%%%%%%%%%%前一组第一个值",new_order[new_order_L-2]
                    print  "%%%%%%%%%%%%新一组最后的值",p2_l
                    print   new_order                                 
                else:
                    temp=[p1_p,p2_l]
                    total=total+temp                         
                    new_order=np.array(total,int)
                
                index_start1=index_start1
                index_end1=index_end2
                index_start2=index_start2+2
                index_end2=index_end2+2
                print "*************融合后更新索引",index_start1,index_end1,index_start2,index_end2
            
            elif(new_order_L<2 and (count_1>=1 or count>=5)):
                temp=[p1_p,p2_l]
                total=total+temp                         
                new_order=np.array(total,int)
                
                index_start1=index_start1
                index_end1=index_end2
                index_start2=index_start2+2
                index_end2=index_end2+2
            elif(count_0>=10 or count_null>5):
                repeat=repeat+1
                if(repeat==2):                    
                    temp=[p1_p,p1_l]
                    temp_=[p2_p,p2_l]
                    if(i>0 and new_order[new_order_L-1]==p1_l):                    
                        total=total+temp_
                    else:
                        total=total+temp+temp_
                        
                    new_order=np.array(total,int)                    
                    index_start1=index_start2
                    index_end1=index_end2
                    index_start2=index_start2+2
                    index_end2=index_end2+2 
                    print "*************不融合后更新索引",index_start1,index_end1,index_start2,index_end2
            return 

def compareTxt(listTxt1,listTxt2,i):               
        if(len(listTxt1)>len(listTxt2)):
            for i in range(len(listTxt1)):
                for j in range(len(listTxt2)):                    
                    ratio=re.TextSimilarity(listTxt1[i],listTxt2[j])
                    similarityCount(ratio,i) 
        
        else:
             for i in range(len(listTxt2)):
                for j in range(len(listTxt1)):                    
                    ratio=re.TextSimilarity(listTxt1[j],listTxt2[i])
                    similarityCount(ratio,i)
        return

# =============================================================================
#             
# =============================================================================
def loop(): 
    index_start1= 0
    index_end1 = 1
    index_start2 = 2
    index_end2 = 3
    for i in range(0,order_FSX_length):
        
        if(index_end2<=order_FSX_length-1):    
            p1_p=order_FSX_R[index_start1]
            p1_l=order_FSX_R[index_end1]
            
            p2_p=order_FSX_R[index_start2]
            p2_l=order_FSX_R[index_end2] 
    
            listTxt1=[]
            listTxt2=[]
            
            p1_index = p1_p
            p2_index = p2_p
            for j in range(0,order_FSX_length):
                print "第",i,"个下标======================================"
                
                for i in range(p1_p,p1_l):
                    p1_index += frame
                    print "//////////////自增索引值1",p1_index
                    p1_deal=re.image_deal(Image.open(add_pic + str(p1_index)+ '.jpg'))
                    text1=re.textExtract(p1_deal).strip()
                    #print "t1----------",p1_index, text1            
                    if(len(text1)>0):
                        listTxt1.append(text1)
                for j in range(p2_p,p2_l):
                    p2_index += frame        
                    print "//////////////自增索引值2",p2_index
                    p2_deal=re.image_deal(Image.open(add_pic + str(p2_index)+ '.jpg'))          
                    text2=re.textExtract(p2_deal).strip()
                    #print "t2-----------",p2_index, text2
                    if(len(text2)>0):
                        listTxt2.append(text2)
               #return listTxt1,listTxt2
                break
        else:
             break

# =============================================================================
# main           
# =============================================================================
if __name__=="__main__":
    
    loop()    
    np.save(add_outArrClu,new_order)




       
            
            
            
            
            