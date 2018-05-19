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
add_outArray_picCluster="E:\\Python\\cluster result\\201710162100\\201710162100.npy"
add_outArray_txtCluster="E:\\Python\\cluster result\\201710162100\\201710162100_t1.npy"
add_inArray_wav='E:/python/audio/wav/201710162100/201710162100.npy'

accept=77
#视频长度  毫秒
time=29*60*60+53*60
#开始 
total_begin=1
#图片总量  16571
total_Pic=ft.FileCount(add_pic)
movie_length=23*60+59


def shot_screenTxtCluster():
    
    total=[]    
    new_order=np.array(total,int)
    order_FSX=np.load(add_outArray_picCluster)
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
        frame=10
        new_order_L=len(new_order)
        
        if(index_end2<=order_FSX_length-1):
            print "第",i,"个下标======================================"            
            p1_p=order_FSX_R[index_start1]
            p1_l=order_FSX_R[index_end1]
            
            p2_p=order_FSX_R[index_start2]
            p2_l=order_FSX_R[index_end2] 
            if(p2_p==p2_l):
                p2_p=order_FSX_R[index_start2]
                p2_l=order_FSX_R[index_end2+1]
            if(p1_p==p1_l):
                p1_p=order_FSX_R[index_start1]
                p1_l=order_FSX_R[index_end1+1]
            print "1前",p1_p
            print "1后",p1_l
            print "2前",p2_p
            print "2后",p2_l
            
            p1_index = p1_p
            p2_index = p2_p
            for j in range(0,order_FSX_length):                    
                
                if(p1_index<=p1_l and frame>0):
                    print "//////////////自增索引值1",p1_index
                    p1_deal=re.image_deal(Image.open(add_pic + str(p1_index)+ '.jpg'))
                    text1=re.textExtract(p1_deal).strip()
                    p1_index += frame 
                elif(frame<0):
                    print "//////////////逆序自增索引值1",p1_index
                    p1_deal=re.image_deal(Image.open(add_pic + str(p1_index)+ '.jpg'))
                    text1=re.textExtract(p1_deal).strip()
                    p1_index += frame 
                else:
                    p1_index = p1_p
                    p2_index = p2_p
                    frame=1
                    continue
                
                if(p2_index<=p2_l):
                    print "//////////////自增索引值2",p2_index
                    p2_deal=re.image_deal(Image.open(add_pic + str(p2_index)+ '.jpg'))          
                    text2=re.textExtract(p2_deal).strip()
                    p2_index += frame

                else:
                    p1_index = p1_p
                    p2_index = p2_p
                    frame=1
                    continue
    # =============================================================================
    #  相似度统计           
    # =============================================================================
                if(len(text1)>3 and len(text2)>3):        
                    ratio=re.TextSimilarity(text1.strip(),text2.strip())
                    if(ratio<0.5):
                       print "二次检测！！！！！"
                       p1_deal1,p1_deal2=re.image_deal2(Image.open(add_pic + str(p1_index)+ '.jpg'))
                       text1=re.textExtract(p1_deal1).strip()
                       text2=re.textExtract(p1_deal2).strip()
                       
                       p2_deal1,p2_deal2=re.image_deal2(Image.open(add_pic + str(p2_index)+ '.jpg'))
                       text3=re.textExtract(p1_deal1).strip()
                       text4=re.textExtract(p1_deal2).strip()
                       print "二次检测文本TTTTTTTT",text1.strip(),"___",text2.strip(),"___",text3.strip(),"____",text4.strip()
                       if()
                       ratio1=re.TextSimilarity(text1.strip(),text3.strip())
                       ratio2=re.TextSimilarity(text2.strip(),text4.strip())
                       ratio3=re.TextSimilarity(text1.strip(),text4.strip())
                       ratio4=re.TextSimilarity(text2.strip(),text3.strip())
                       print ratio1,ratio2,ratio3,ratio4
                       if(ratio1>0.8 or ratio2>0.8 or ratio3>0.8 or ratio4>0.8):
                           print "二次检测相似"
                           ratio=1
                else:
                    ratio=0
                    print "文本过短或者无文本，相似度置零"
                if(ratio>0.5 and ratio!=1):            
                    count+=1
                elif(ratio==-1):
                    count_null+=1 
                    print "相似度为-1的个数",count_null
                elif(ratio==0 or ratio<=0.5):
                    count_0+=1 
                    print "相似度为0 或者小于0.5的个数",count_0
                elif(ratio==1):
                    count_1 +=1
                    print "相似度为1的个数",count_1
                    
    # =============================================================================
    #数组操作       
    # =============================================================================
                if(new_order_L>2 and (count_1>=5 or count>=10)):           
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
                        print   new_order
                    index_start1=index_start1
                    index_end1=index_end2
                    index_start2=index_start2+2
                    index_end2=index_end2+2
                    print "融合的是：",p1_p,p1_l,p2_p,p2_l
                    print "*************融合后更新索引",index_start1,index_end1,index_start2,index_end2
                    break
                elif(new_order_L<2 and (count_1>=1 or count>=5)):
                    temp=[p1_p,p2_l]
                    total=total+temp                         
                    new_order=np.array(total,int)
                    print   new_order
                    index_start1=index_start1
                    index_end1=index_end2
                    index_start2=index_start2+2
                    index_end2=index_end2+2
                     
                    break
                elif(count_0>=10 or count_null>30):
                    repeat=repeat+1
                    if(repeat==1):
                        frame=25*2
                        count_0=0
                        count_null=0
                        print "再次核对"
                        continue
                    elif(repeat==2):
                        print "逆序核对"
                        p1_index = p1_l
                        count_0=0
                        count_null=0                        
                        frame=-10                      
                        continue
                    elif(repeat==3):                    
                        temp=[p1_p,p1_l]
                        temp_=[p2_p,p2_l]
                        if(i>0 and new_order[new_order_L-1]==p1_l):                    
                            total=total+temp_
                            print "不融合的是：",temp_
                        else:
                            total=total+temp+temp_
                            print "不融合的是：",temp,temp_
                            
                        new_order=np.array(total,int)                    
                        index_start1=index_start2
                        index_end1=index_end2
                        index_start2=index_start2+2
                        index_end2=index_end2+2
                        print   new_order 
                        
                        print "*************不融合后更新索引",index_start1,index_end1,index_start2,index_end2
                        break                             
                    
                else:
                    continue
            else:
                break
            
    return new_order       
# =============================================================================
#   
# =============================================================================
if __name__=="__main__":
# =============================================================================
#     order_FSX = SA.FilmShotsCut(time,total_begin,total_end,accept,add_pic)
#     np.save(add_outArray_picCluster,order_FSX)
# =============================================================================

    fushion_shot=shot_screenTxtCluster()    
    np.save(add_outArray_txtCluster,fushion_shot) #保存屏幕文本融合后的结果
    
       
            
            
            
            
            