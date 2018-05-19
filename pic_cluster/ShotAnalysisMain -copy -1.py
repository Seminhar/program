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

frame=10
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

index_start1=0
index_end1=1
index_start2=2
index_end2=3
 
    
for i in range(0,order_FSX_length):
    count=0
    count_0=0
    count_1=0
    count_null=0
    repeat=0
    flag=0
    new_order_L=len(new_order)
    if(index_end2<=order_FSX_length-1):
        print "第",i,"个下标======================================"
        p1_p=order_FSX_R[index_start1]
        p1_l=order_FSX_R[index_end1]
        
        p2_p=order_FSX_R[index_start2]
        p2_l=order_FSX_R[index_end2] 

        listTxt1=[]
        listTxt2=[]
        
        p1_index = p1_p
        p2_index = p2_p
        for j in range(0,order_FSX_length):           
# =============================================================================
#                        
# =============================================================================
            for k in range(p1_p,p1_l):
                p1_index += frame
                picIndex=p1_index-10
                print "//////////////自增索引值1",picIndex                
                if(picIndex<=p1_l):
                    p1_deal=re.image_deal(Image.open(add_pic + str(picIndex)+ '.jpg'))
                    text1=re.textExtract(p1_deal).strip()
                    print "t1----------",p1_index, text1            
                    if(len(text1)>0):
                        listTxt1.append(text1)
                else: 
                    break 
            for l in range(p2_p,p2_l):
                p2_index += frame
                picIndex=p2_index-10
                print "//////////////自增索引值2",picIndex
                if(picIndex<=p2_l):
                    p2_deal=re.image_deal(Image.open(add_pic + str(picIndex)+ '.jpg'))          
                    text2=re.textExtract(p2_deal).strip()
                    print "t2-----------",p2_index, text2
                    if(len(text2)>0):
                        listTxt2.append(text2)
                else:
                    break
# =============================================================================
# 
# =============================================================================
            
            if(len(listTxt1)>len(listTxt2)):
                for n in range(len(listTxt1)):
                    for m in range(len(listTxt2)):                    
                        ratio=re.TextSimilarity(listTxt1[n],listTxt2[m])
                        print listTxt1[n],"*******与*******",listTxt2[m],"相似度-->",ratio
                        if(ratio>0.5):            
                            count=count+1
                        elif(ratio==-1):
                            count_null=count_null+1 
                            print "相似度为-1的个数",count_null
                        elif(ratio==0 or ratio<=0.5):
                            count_0=count_0+1 
                            print "相似度为0 或者小于0.5的个数",count_0
                        elif(ratio>=0.8):
                            count_1=count_1+1
                            print "相似度为1的个数",count_1
                            
                            
                        if(new_order_L>2 and (count_1>=5 or count>=10)):           
                            if(new_order[new_order_L-1]==p1_l):
                                new_order[new_order_L-1]=p2_l
                                total=new_order.tolist()
                                print  "%%%%%%%%%%%%前一组第一个值",new_order[new_order_L-2]
                                print  "%%%%%%%%%%%%新一组最后的值",p2_l
                                print   new_order
                                break      
                            else:
                                temp=[p1_p,p2_l]
                                total=total+temp                         
                                new_order=np.array(total,int)
                            
                            index_start1=index_start1
                            index_end1=index_end2
                            index_start2=index_start2+2
                            index_end2=index_end2+2
                            flag=1
                            print "*************融合后更新索引",index_start1,index_end1,index_start2,index_end2
                            break
                        elif(new_order_L<2 and (count_1>=5 or count>=10)):
                            temp=[p1_p,p2_l]
                            total=total+temp                         
                            new_order=np.array(total,int)
                            
                            index_start1=index_start1
                            index_end1=index_end2
                            index_start2=index_start2+2
                            index_end2=index_end2+2
                            flag=1
                            break
                        elif(count_0>=10 or count_null>30):
                            repeat=repeat+1
                            if(repeat==30):                    
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
                                flag=1
                                print "*************不融合后更新索引",index_start1,index_end1,index_start2,index_end2
                                break             
                               
                            else:
                                continue
                    if(flag==1):
                        print "打印旗帜"
                        break
    
                   
            else:
                 for n in range(len(listTxt2)):
                    for m in range(len(listTxt1)):                    
                        ratio=re.TextSimilarity(listTxt1[m],listTxt2[n])                    
                        if(ratio>0.5):            
                            count=count+1
                        elif(ratio==-1):
                            count_null=count_null+1 
                            print "相似度为-1的个数",count_null
                        elif(ratio==0 or ratio<=0.5):
                            count_0=count_0+1 
                            print "相似度为0 或者小于0.5的个数",count_0
                        elif(ratio>=0.7):
                            count_1=count_1+1
                            print "相似度为1的个数",count_1                                                     
                        if(new_order_L>2 and (count_1>=5 or count>=10)):           
                            if(new_order[new_order_L-1]==p1_l):
                                new_order[new_order_L-1]=p2_l
                                total=new_order.tolist()
                                print  "%%%%%%%%%%%%前一组第一个值",new_order[new_order_L-2]
                                print  "%%%%%%%%%%%%新一组最后的值",p2_l
                                print   new_order
                                break                                 
                            else:
                                temp=[p1_p,p2_l]
                                total=total+temp                         
                                new_order=np.array(total,int)
                                
                            index_start1=index_start1
                            index_end1=index_end2
                            index_start2=index_start2+2
                            index_end2=index_end2+2
                            flag=1
                            print "*************融合后更新索引",index_start1,index_end1,index_start2,index_end2
                            break
                        elif(new_order_L<2 and (count_1>=5 or count>=10)):
                            temp=[p1_p,p2_l]
                            total=total+temp                         
                            new_order=np.array(total,int)
                            
                            index_start1=index_start1
                            index_end1=index_end2
                            index_start2=index_start2+2
                            index_end2=index_end2+2
                            flag=1
                            break
                        elif(count_0>=30 or count_null>30):
                            repeat=repeat+1
                            if(repeat==30 ):                    
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
                                flag=1
                                print "*************不融合后更新索引",index_start1,index_end1,index_start2,index_end2
                                break             
                               
                            else:
                                continue
                    if(flag==1):
                        print "打印旗帜"
                        break

# =============================================================================
#            
# =============================================================================
np.save(add_outArrClu,new_order)




       
            
            
            
            
            