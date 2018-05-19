# -*- coding: utf-8 -*-
from PIL import  Image
import numpy as np
import math
from sympy import  *
#import Feature
import pylab as pl

#比较两个帧的相似度，通过边框度比较与中心比较法则
def Simularity(P1,P2,accept):
    Size = np.array(P1.size,int)
    r1,g1,b1 = CompressAndExtractRGB(P1)
    r2,g2,b2 = CompressAndExtractRGB(P2)    
    
    #两个帧的红色特征边框 c1 与 d1 比较
    c1array = np.array(r1,dtype=float)
    c1 = c1array[Size[1]/6:Size[1]/3,:]  #取次外框，防止电影上下有黑条的情况
    c2 = c1array[Size[1]/2*3:Size[1]*5/6,:]
    c3 = c1array[Size[1]/6:Size[1]/6*5,0:Size[0]/5]
    c4 = c1array[Size[1]/6:Size[1]/6*5,Size[0]/4*5:Size[0]]
    
    d1array = np.array(r2,dtype=float)
    d1 = d1array[Size[1]/6:Size[1]/3,:]  #取次外框，防止电影上下有黑条的情况
    d2 = d1array[Size[1]/2*3:Size[1]*5/6,:]
    d3 = d1array[Size[1]/6:Size[1]/6*5,0:Size[0]/5]
    d4 = d1array[Size[1]/6:Size[1]/6*5,Size[0]/4*5:Size[0]]
    temp1 = np.array([np.abs(c1-d1).sum(),np.abs(c2-d2).sum(),np.abs(c3-d3).sum()*2,np.abs(c4-d4).sum()*2]).sum()
    
    #两个帧的红色中心 w1 与 q1 比较
    w1 = c1array[Size[1]/5:Size[1]*4/5,Size[0]/5:Size[0]*4/5]
    q1 = d1array[Size[1]/5:Size[1]*4/5,Size[0]/5:Size[0]*4/5]
    temp2 = np.abs(w1-q1).sum()
    
    #两个帧的绿色边框 c1 与 d1 比较
    c1array = np.array(g1,dtype=float)
    c1 = c1array[Size[1]/6:Size[1]/3,:]
    c2 = c1array[Size[1]/2*3:Size[1]*5/6,:]
    c3 = c1array[Size[1]/6:Size[1]/6*5,0:Size[0]/5]
    c4 = c1array[Size[1]/6:Size[1]/6*5,Size[0]/4*5:Size[0]]

    
    d1array = np.array(g2,dtype=float)
    d1 = d1array[Size[1]/6:Size[1]/3,:]
    d2 = d1array[Size[1]/2*3:Size[1]*5/6,:]
    d3 = d1array[Size[1]/6:Size[1]/6*5,0:Size[0]/5]
    d4 = d1array[Size[1]/6:Size[1]/6*5,Size[0]/4*5:Size[0]]
    temp1 = temp1+np.array([np.abs(c1-d1).sum(),np.abs(c2-d2).sum(),np.abs(c3-d3).sum()*2,np.abs(c4-d4).sum()*2]).sum()
    
    #两个帧的绿色中心 w1 与 q1 比较
    w1 = c1array[Size[1]/5:Size[1]*4/5,Size[0]/5:Size[0]*4/5]
    q1 = d1array[Size[1]/5:Size[1]*4/5,Size[0]/5:Size[0]*4/5]
    temp2 =temp2+ np.abs(w1-q1).sum()
    
    #两个帧的蓝色边框 c1 与 d1 比较
    c1array = np.array(b1,dtype=float)
    c1 = c1array[Size[1]/6:Size[1]/3,:]
    c2 = c1array[Size[1]/2*3:Size[1]*5/6,:]
    c3 = c1array[Size[1]/6:Size[1]/6*5,0:Size[0]/5]
    c4 = c1array[Size[1]/6:Size[1]/6*5,Size[0]/4*5:Size[0]]

    
    d1array = np.array(b2,dtype=float)
    d1 = d1array[Size[1]/6:Size[1]/3,:]
    d2 = d1array[Size[1]/2*3:Size[1]*5/6,:]
    d3 = d1array[Size[1]/6:Size[1]/6*5,0:Size[0]/5]
    d4 = d1array[Size[1]/6:Size[1]/6*5,Size[0]/4*5:Size[0]]
    temp1 = temp1+np.array([np.abs(c1-d1).sum(),np.abs(c2-d2).sum(),np.abs(c3-d3).sum()*2,np.abs(c4-d4).sum()*2]).sum()
    
    #两个帧的蓝色中心 w1 与 q1 比较
    w1 = c1array[Size[1]/5:Size[1]*4/5,Size[0]/5:Size[0]*4/5]
    q1 = d1array[Size[1]/5:Size[1]*4/5,Size[0]/5:Size[0]*4/5]
    temp2 =temp2+ np.abs(w1-q1).sum()
    
    t1 = Size[0]*Size[1]-1.0/5*Size[0]*1.0/5*Size[1]
    t2 = 1.0/5*Size[0]*1.0/5*Size[1]
    if (temp1/t1 <= accept or temp2/t2 <= accept) :  #只要中心差异或者边框差异其中一个小于等于相似度阈值，我们就可以知道两帧是相似的
        return 1
    else:
        return 0


#提取当前帧的 R,G,B 特征
def CompressAndExtractRGB(P):
    tb = P.resize((P.size[0],P.size[1]))
    r,g,b = tb.split()
    return np.array(r,dtype=float) ,np.array(g,dtype=float), np.array(b,dtype=float)


#提取当前帧的 H,S,V 特征
def Rgb2Hsv(r, g, b):
    v = np.array([ [0]* len(r[0]) ]* len(r),float)
    s = np.array([ [0]* len(r[0]) ]* len(r),float)
    h = np.array([ [0]* len(r[0]) ]* len(r),float)
    for i in range(len(r)):
        for j in range(len(r[0])):
            r11 = r[i][j]/255.0
            g11 = g[i][j]/255.0
            b11 = b[i][j]/255.0
            mx = max([r11,g11,b11])
            mn = min([r11,g11,b11])
            df = mx-mn
            if mx == mn:
                h[i][j] = 0
            elif mx == r11:
                h[i][j] = (60 * ((g11-b11)/df) + 360) % 360
            elif mx == g11:
                h[i][j] = (60 * ((b11-r11)/df) + 120) % 360
            elif mx == b11:
                h[i][j] = (60 * ((r11-g11)/df) + 240) % 360
            if mx == 0:
                s[i][j] = 0
            else:
                s[i][j] = df/mx
            v[i][j] = mx
            
    return h, s, v

#通过比较相邻两帧的相似性，找到镜头边界，最后输出镜头边界序列 order    
def FilmShotsCut(time,total_begins,total_end,accept,address):
    total  = []
    j = total_begins
    for i in range(total_begins,total_end):
        if i<j:
            continue
        P1 = Image.open(address + str(i)+ '.jpg')
        begins = i
        for j in range(i,total_end+1):
            P2 = Image.open(address + str(j)+ '.jpg')
            if not Simularity(P1,P2,accept):              #不相似则把镜头边界记录下来
                break
            else:
                P1=Image.open(address + str(j)+ '.jpg')   #相似则继续往后找
        if j==total_end:            
            ends = j
        else:
            ends = j-1   
        temp = [begins,ends]
        total = total + temp 
    
    order = np.array(total,int)        
    return order
    
def ShotsChar(order,address,valueToSelect,samplingT,total_begin,total_end):
    #初始化数组 speed ， colour ， brightness 之后用来存每个镜头的这些特征
    speed = np.zeros([1,len(order)/2])
    colour = np.zeros([1,len(order)/2])
    brightness = np.zeros([1,len(order)/2])
    
    #镜头速率定义为该镜头的帧数
    k=0
    for i in  range(0,len(order),2):
        speed[0,k] = order[i+1] - order[i]
        k = k+1    
    
    #镜头的色温由镜头首个帧，中间帧，最后一个帧的色温共同确定
    k=0
    for i in   range(0,len(order),2):
        warm = np.zeros([3,1])
        P1 = Image.open(address + str(order[i])+ '.jpg')
        P3 = Image.open(address + str((order[i]+order[i+1])/2)+ '.jpg')
        P2 = Image.open(address + str(order[i+1])+ '.jpg')
        r1,g1,b1 = CompressAndExtractRGB(P1)
        h1 = Rgb2Hsv(r1, g1, b1)
        r2,g2,b2 = CompressAndExtractRGB(P2)
        h2= Rgb2Hsv(r2, g2, b2)
        r3,g3,b3 = CompressAndExtractRGB(P3)
        h3 = Rgb2Hsv(r3, g3, b3)
        
        #色温的测度函数（冷暖色的判断）
        for w in range(len(h1[0])):
            for v in range(len(h1[0][0,:])):
                if h1[0][w][v]< 105 or h1[0][w][v]>315:
                        warm[0,0] = warm[0,0] +1
                if h2[0][w][v]< 105 or h2[0][w][v]>315:
                        warm[1,0] = warm[1,0] +1
                if h3[0][w][v]< 105 or h3[0][w][v]>315:
                        warm[2,0] = warm[2,0] +1
        colour[0,k] = (warm[0,0]+warm[1,0]+warm[2,0])/(3.0*len(h1[0])*len(h1[0][0,:]))       
        k=k+1  

    #镜头的亮度由镜头首个帧，中间帧，最后一个帧的色温共同确定          
    k=0
    for i in range(0,len(order),2):
        bright = np.zeros([3,1])
        P1 = np.array(Image.open(address + str(order[i])+ '.jpg').convert('L'),int)
        P2 = np.array(Image.open(address + str((order[i]+order[i+1])/2)+ '.jpg').convert('L'),int)
        P3 = np.array(Image.open(address + str(order[i+1])+ '.jpg').convert('L'),int)
        #亮度的测度函数（亮与暗的判断）
        for w in range(len(P1)):
            for v in range(len(P1[0,:])):
                    if P1[w][v]>=65:
                        bright[0,0] = bright[0,0] +1
                    if P2[w][v]>=65:
                        bright[1,0] = bright[1,0] +1
                    if P3[w][v]>=65:
                        bright[2,0] = bright[2,0] +1                        
        brightness[0,k] = (bright[0,0]+bright[1,0]+bright[2,0])/(3.0)       
        k=k+1 
        
    #归一化四个特征值，统一化横纵坐标
    brightness_draw = brightness/brightness.max()   
    speed_draw = speed/speed.max()
    colour_draw = colour/colour.max()
    valueToSelect = AdjustValue(order,valueToSelect,samplingT,total_begin,total_end)
    
    #由于速率和声音能量特征值较小，有少许突变值，直接绘图效果不好，要先做 LOG 变换
    e = (speed_draw +0.01)/min(speed_draw [0,:]+0.01)
    speedLog = np.zeros([1,len(speed_draw [0,:])],float)
    for i in range(len(speed_draw [0,:])):
        speedLog[0,i] = math.log(e[0,i],min(e[0,:])+1)
    speedLog=speedLog/max(speedLog[0,:])
    
    e = (valueToSelect+0.01)/min(valueToSelect+0.01)
    valueToSelectLog = np.zeros(len(valueToSelect),float)
    for i in range(len(valueToSelect)):
        valueToSelectLog[i] = math.log(e[i],min(e)+1)
    valueToSelectLog=valueToSelectLog/max(valueToSelectLog)
    
    
    #定义横纵坐标，为作图做准备
    x1 = range(0,len(colour_draw[0,:]))
    y1 = np.transpose(colour_draw).tolist()
    x2 = range(0,len(brightness_draw[0,:]))
    y2 = np.transpose(brightness_draw).tolist()
    x3 = range(0,len(speedLog[0,:]))
    y3 = np.transpose(speedLog).tolist()
    x4 = range(0,len(valueToSelectLog))
    y4 = np.transpose(valueToSelectLog).tolist()
      
    
    #绘制亮度，速率，色温，声音能量折线图
    f1 = pl.figure(1)
    pl.subplot(411)
    pl.plot(x1,y1,'b')
    pl.subplot(412)
    pl.plot(x2,y2,'r')
    pl.subplot(413)
    pl.plot(x3,y3,'y')
    pl.subplot(414)
    pl.plot(x4,y4,'g')
    
    #绘制亮度，速率，色温，声音能量直方图
    f2 = pl.figure(2)
    pl.subplot(411)
    pl.hist(np.array(y1,float),np.arange(0., 1., 0.02))
    pl.subplot(412)
    pl.hist(np.array(y2,float),np.arange(0., 1., 0.02))
    pl.subplot(413)
    pl.hist(np.array(y3,float),np.arange(0., 1., 0.02))
    pl.subplot(414)
    pl.hist(np.array(y4,float),np.arange(0., 1., 0.02))
        
    return speed,colour,brightness                         

#累计每个镜头的声音能量序列
def AdjustValue(order,valueToSelect,samplingT,total_begin,total_end):
    temp =[]
    acc = 0
    total = total_end - total_begin
    for i in range(0,len(order),2):
        if int(len(valueToSelect)*order[i+1]/total)+1 >= len(valueToSelect):  #寻找该镜头所对应的声音能量段
            qq = int(len(valueToSelect)*order[i+1]/total)
        else:
            qq = int(len(valueToSelect)*order[i+1]/total)+1
            for j in range(int(len(valueToSelect)*order[i]/total),qq):
                acc = acc +valueToSelect[j]                                   #找到后进行累加操作
        temp = temp +[acc]
        acc = 0
    return np.array(temp,float)

#对离散型的序列求导
def diff(value,dx,segmentPart):
    tempList = [0]+value.tolist()
    tempList.pop()
    value2 = np.array(tempList)
    return ((value-value2)/dx)[1:segmentPart*3]

#对原始音频进行能量特征提取。输入参数分别是音频的开始，经过，结束段和每一段的采样个数（采样个数 = 每段总时间/采样时间间隔）
def SoundAnalysis(filename1,filename2,filename3,segmentPartToSelect):
    
    importPart= 23                #importPart参数表示在此段中选取 importPart 个能量大的参考点和  importPart 个能量小的参考点
    feature1 = Feature.Feature(filename1, importPart, segmentPartToSelect)
    feature2 = Feature.Feature(filename2, importPart, segmentPartToSelect)
    feature3 = Feature.Feature(filename3, importPart, segmentPartToSelect)
    importPoint1,value1 = feature1.findImportPoint()
    importPoint2,value2 = feature2.findImportPoint()
    importPoint3,value3 = feature3.findImportPoint()
    return value1,value2,value3             #返回开始，经过，结束三段的又高到低排序好的能量特征序列'


#剔除 X 中过于集中的参考点与超过正式开始结束边界的参考点
def remap(x,total,total_begin,total_end,time):
    
    w = x      #保护 x
    radius = 5 #密集阈值（默认值为 5 表示该参考点的前、后 5 个单位以内的点都被定义为过于集中的点）  
               #与 limitQual = 4  最大允许往前或往后扩充镜头数（默认值为 4 个） 保证场景与场景间没有相交部分
    
    #把超过正式开始结束边界的参考点剔除（剔除方法是置 0 ） 
    for i in range(len(w)):
            if w[i]<= total_begin+0.0:
                w[i]=0
            if w[i]>=total_end+0.0:
                w[i]=0
    
    #把过于集中的参考点也剔除（以排名靠前的点作为参考去排查后面的点）          
    for i in range(len(w)):
        if not w[i] == 0:
            for j in range(i+1,len(x)):
                if w[j]>=w[i]-radius*total/(3.0*len(w)) and w[j]<=w[i]+radius*total/(3.0*len(w)):
                    w[j]=0
                
                
    return w
 
#找到参考点对应的第几个镜头
def FindLocation(taget,order):
    
    for i in range(len(order)/2):
        if order[i*2] <= int (taget) and order[i*2+1] >= int (taget):
            return np.array([[i*2],[i*2+1]])
            
#判断 front镜头 是不是比 behind镜头 更与 location镜头相似，通过速率，亮度，色温
def SimularShot(order,location,front,behind,speed,brightness,colour,total,time): 
    
    if behind >= len(order):   #如果 behind 下一个镜头超过最后一个镜头，则直接判 front 镜头 更相似  
            return 1
    if front <= 0 :   #如果 front 前一个镜头超过第一个镜头，则直接判 behind 镜头 更相似  
            return 0
    
    #两镜头的亮度与色温差之后
    temp1 = abs(colour[0,location[0]/2]-colour[0,(front-1)/2])/max(colour[0,:])+abs(brightness[0,location[0]/2]-brightness[0,(front-1)/2])/max(brightness[0,:])
    temp2 = abs(colour[0,location[0]/2]-colour[0,(behind)/2])/max(colour[0,:])+abs(brightness[0,location[0]/2]-brightness[0,(behind)/2])/max(brightness[0,:])
                   
    
    if temp1 <= temp2 and speed[0,(front-1)/2] <= speed[0,(behind)/2]: # 如果镜头一的亮度与色温差和速率都比镜头二小
        return 1
    elif temp1 <= temp2 and speed[0,(front-1)/2] > speed[0,(behind)/2]: #如果镜头一的亮度与色温差比镜头二小，但速率不是
        if speed[0,(front-1)/2] - speed[0,(behind)/2] <= int (total*14/(60.0*time)): #速率相差不大的话，还是选镜头一
            return 1
        else:
            return 0
    elif temp1 > temp2 and speed[0,(front-1)/2] >= speed[0,(behind)/2]: #如果镜头二的亮度与色温差和速率都比镜头以小
            return 0
    else :                                               #如果镜头二的亮度与色温差比镜头一小，但速率不是
        if speed[0,(front-1)/2] - speed[0,(behind)/2] <= int (total*14/(60.0*time)):  #速率相差不大的话，还是选镜头二
            return 0
        else:
            return 1
            

#对给定的镜头，查看是往前还是往后扩张新的镜头，并执行
def Growing (total,time,order,location,candidate,front,behind,speed,brightness,colour,limitTime,now1,now2):
    
    if SimularShot(order,location,front,behind,speed,brightness,colour,total,time):  #如果 front镜头 比 behind镜头 更和参考镜头相似
             if order[(front)]-order[(front-1)]+0.0 <=  (total*limitTime/(60.0*time)):  #如果该镜头少于等于 10 秒，则直接完整扩充该镜头
                 candidate[0,now1] = order[(front-1)]
                 candidate[0,now1+1] = order[(front)]
                 now1 = now1 -2
                 front = front -2
             else:                                             #否则取该镜头中间的 14 秒
                 candidate[0,now1] = (order[(front-1)]+order[front])/2-total*limitTime/(2*60.0*time)
                 candidate[0,now1+1] = (order[(front-1)]+order[front])/2+total*limitTime/(2*60.0*time)
                 now1 = now1 -2
                 front = front -2
    else:
             if order[(behind+1)]-order[(behind)]+0.0 <=  (total*limitTime/(60.0*time)):  #如果该镜头少于等于 10 秒，则直接完整扩充该镜头
                 candidate[0,now2] = order[(behind+1)]
                 candidate[0,now2-1] = order[(behind)]
                 now2 = now2 +2
                 behind = behind +2
             else:                                             #否则取该镜头中间的 14 秒
                 candidate[0,now2-1] = (order[(behind)]+order[behind+1])/2-total*limitTime/(2*60.0*time)
                 candidate[0,now2] = (order[(behind)]+order[behind+1])/2+total*limitTime/(2*60.0*time)        
                 now2 = now2 +2
                 behind = behind +2
                 
    return candidate,now1,now2,front,behind


                 
#对给定参考点进行扩张，成为小场景
def extendShot(location,order,time,total,speed,brightness,colour):
    
    candidate = np.zeros([1,22],int) #列数要与 winner 一致
    now1 = 10      # now 用来表示 candidate的当前状态的前后指针
    now2 = 11
    limitTime = 14 #参考点自己扩散是否完整的条件（默认值是 14秒）
    limitQual = 4  #最大允许往前或往后扩充镜头数（默认值为 4 个）
    
    if order[location[1]]-order[location[0]]+0.0 <= total*limitTime/(60.0*time): #如果该镜头少于等于 14 秒，则直接完整扩充该镜头
            candidate[0,now1] = order[location[0]]
            candidate[0,now2] = order[location[1]]
            now1 = now1 -2
            now2 = now2 +2
            behind = location[1]+1   # front,behind 是取 order时的索引
            front = location[0]-1
            
            while (not limitQual == 0):
                candidate,now1,now2,front,behind = Growing(total,time,order,location,candidate,front,behind,speed,brightness,colour,limitTime,now1,now2)

                limitQual = limitQual - 1
    else  :                                                  #否则取该镜头中间的 14 秒
            candidate[0,now1] = (order[location[0]]+order[location[1]])/2-total*limitTime/(2*60.0*time)
            candidate[0,now2] = (order[location[0]]+order[location[1]])/2+total*limitTime/(2*60.0*time)
            now1 = now1 -2
            now2 = now2 +2
            behind = location[1]+1
            front = location[0]-1
            while (not limitQual == 0):
                candidate,now1,now2,front,behind = Growing(total,time,order,location,candidate,front,behind,speed,brightness,colour,limitTime,now1,now2)

                limitQual = limitQual - 1  
                
    if candidate[0,now2 -2] - candidate[0, now1 +2] <= total*limitTime/(60.0*time): #如果生成的小场景过短（少于等于 14 秒），则直接再扩充完一个镜头
                limitQual = 1
                while (not limitQual == 0):
                    candidate,now1,now2,front,behind = Growing(total,time,order,location,candidate,front,behind,speed,brightness,colour,limitTime,now1,now2)

                    limitQual = limitQual - 1  

    return candidate


#判断生成的场景是否重复了
def equal(candidate,winner):
    
    for i in range(len(winner)):
        for j in range(len(winner[0,:])):
            for k in range(len(winner[0,:])):
                if winner[i,j] == candidate[0,k] and not winner[i,j]==0 and not candidate[0,k]==0:
                    return 1
    return 0


#寻找关键场景的主函数，其中 key 为用户输入的所需寻找的场景数
def KeyScene( order,total,address,time,key,value1,value2,value3,speed,colour,brightness,total_end,total_begin ):    
    
        
    #按由高到低排序开始，经过，结束三段的声音能量，最后分别用 x1，x2，x3 记录声音能量对应的帧的位置
    y1 = total/3*( np.argsort(-np.array(value1))+1.0)/len(value1)
    y2 = total*( np.argsort(-np.array(value2))+1 +len(value1))/(len(value1)*3.0)
    y3 = total*( np.argsort(-np.array(value3))+1 +len(value1)+len(value1))/(len(value1)*3.0)
            
    #剔除 x1，x2，x3 中过于集中的参考点与超过正式开始结束边界的参考点
    target1 = remap(y1,total,total_begin,total_end,time)
    target2 = remap(y2,total,total_begin,total_end,time)
    target3 = remap(y3,total,total_begin,total_end,time)
    target = np.vstack((target1,target2,target3))
    
    #根据 taget 找到参考点所在的镜头，并且扩张成一个小场景
    winner = np.zeros([sum(key),22],int)  #列数要与 candidate 一致
    i = 0
    m = 0
    while i<3 :       #控制开始，经过，结果三大段
        enough = 0    #统计该段需要的场景数
        
        for k in range(len(target1)):  #从该段开始，从前往后找参考点
            if enough == key[i]:         #找够了场景个数才离开循环
                    break
            if not target[i][k] == 0:
                    location = FindLocation(target[i][k],order)  #找到参考点对应的第几个镜头
                    candidate = extendShot(location,order,time,total,speed,brightness,colour)   #对该镜头进行前后扩张

                    if not equal(candidate,winner):  #如果生成的场景没有重复，这加入 winner ，否则重新往后找新的参考点
                        winner[m,:] = candidate
                        m = m + 1
                        enough = enough + 1
                        
            if k == len(target1) and enough < key[i]   :  #找到最末端还没找够
                    print (' No %d of target error: please check the function remap if the variables is too strict or not'%i)

        i = i +1
    return winner,target

#把 winner的帧范围转为时间范围，并以时间顺序输出
def AdjustWinner(winner,time,total):
    
    winner_time = time*(winner+0.0)/total

    temp = winner_time.max(1)
    temparg = temp.argsort()
    arr = np.array([])
    for i in temparg:
        arr = np.append(arr,winner_time[i])
    winner_time_order = arr.reshape((len(winner_time[:,0]),len(winner_time[0,:])))
    
    
    return  winner_time,winner_time_order