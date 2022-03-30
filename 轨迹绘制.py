#用于绘制粒子轨迹，使用海归绘图体系
#请仔细阅读注释
#单个粒子坐标信息可由“瞬时速度计算.py” importData()、numberparticles()、exportlist3()三个函数联用获得

import turtle as t;import math
def gradualchange(allc,count): #渐变色函数。allc为总数据点数或是总颜色数，count为某一数据点的序号。实际上设置的是count点的颜色。
    allc/=5
    if count>=0 and count<=allc:
        t.pencolor(int(255-255/allc*count),0,255)
        print(int(255-255/allc*count))
    if count>allc and count<=2*allc:
        t.pencolor(0,int(255/allc*(count-allc)),255)
        print(int(255/allc*(count-allc)))
    if count>2*allc and count<=3*allc:
        t.pencolor(0,255,int(255-255/allc*(count-2*allc)))
        print(int(255-255/allc*(count-2*allc)))
    if count>3*allc and count<=4*allc:
        t.pencolor(int(255/allc*(count-3*allc)),255,0)
        print(int(255/allc*(count-3*allc)))
    if count>4*allc and count<=5*allc:
        t.pencolor(255,int(255-255/allc*(count-4*allc)),0)
        print(int(255-255/allc*(count-4*allc)))
f=open('已经转化为海龟坐标4_442-472.csv') #粒子坐标数据，共三列第一列为编号，第二列为x轴坐标，滴三列为y轴坐标。注意fiji坐标与海龟坐标的转换
Data=[]
for line in f:
    line=line.replace('\n','')
    Data.append(list(map(eval,line.split(','))))
f.close()
t.setup(1280,960,0,0)
t.pensize(5)
t.colormode(255)
t.pu();t.goto(Data[0][1],Data[0][2]);t.pd()
t.bgpic('80-1_726-760.gif') #用于作图的背景图片，需要gif格式
for i in range(len(Data))[0:len(Data)-3]:#以turtle.circle(),即圆方程,为平滑方程进行平滑
    gradualchange(len(Data)-3,i)
    if i==0:
        A=[Data[i+0][1],Data[i+0][2]]
        B=[Data[i+1][1],Data[i+1][2]]
        C=[Data[i+2][1],Data[i+2][2]]
        E=[(A[0]+B[0])/2,(A[1]+B[1])/2]
        F=[(B[0]+C[0])/2,(B[1]+C[1])/2]
        kEO=(A[0]-B[0])/(B[1]-A[1])
        kFO=(B[0]-C[0])/(C[1]-B[1])
        xO=(F[1]-E[1]+kEO*E[0]-kFO*F[0])/(kEO-kFO)
        yO=kEO*(xO-E[0])+E[1]
        O=[xO,yO]
        kAO=(O[1]-A[1])/(O[0]-A[0])
        kAD=(A[0]-O[0])/(O[1]-A[1])
        xG=(A[1]-E[1]+kEO*E[0]-kAD*A[0])/(kEO-kAD)
        yG=kEO*(xG-E[0])+E[1]
        G=[xG,yG]
        vectorAG=[G[0]-A[0],G[1]-A[1]]
        vectorHI=[1,0]
        angleAGHI=math.acos((vectorAG[0]*vectorHI[0]+vectorAG[1]*vectorHI[1])/\
                         (pow(vectorAG[0]**2+vectorAG[1]**2,0.5)*1))*180/3.1415
        r=pow((O[0]-B[0])**2+(O[1]-B[1])**2,0.5)
        vectorOA=[A[0]-O[0],A[1]-O[1]]
        vectorOC=[C[0]-O[0],C[1]-O[1]]
        angleOAOC=math.acos((vectorOA[0]*vectorOC[0]+vectorOA[1]*vectorOC[1])/\
                     (pow(vectorOA[0]**2+vectorOA[1]**2,0.5)*pow(vectorOC[0]**2+vectorOC[1]**2,0.5)))*180/3.1415
        if vectorAG[1]>0 or vectorAG[1]==0: 
                t.seth(angleAGHI)
        else:
                t.seth(-angleAGHI)
        t.circle(-r,angleOAOC)
        t.pu()
        t.goto(B[0],B[1])
        t.pd()
    else:
        A=[Data[i+0][1],Data[i+0][2]]
        B=[Data[i+1][1],Data[i+1][2]]
        C=[Data[i+2][1],Data[i+2][2]]
        E=[(A[0]+B[0])/2,(A[1]+B[1])/2]
        F=[(B[0]+C[0])/2,(B[1]+C[1])/2]
        kEO=(A[0]-B[0])/(B[1]-A[1])
        kFO=(B[0]-C[0])/(C[1]-B[1])
        xO=(F[1]-E[1]+kEO*E[0]-kFO*F[0])/(kEO-kFO)
        yO=kEO*(xO-E[0])+E[1]
        O=[xO,yO]
        kAO=(O[1]-A[1])/(O[0]-A[0])
        kAD=(A[0]-O[0])/(O[1]-A[1])
        xG=(A[1]-E[1]+kEO*E[0]-kAD*A[0])/(kEO-kAD)
        yG=kEO*(xG-E[0])+E[1]
        G=[xG,yG]
        vectorAG=[G[0]-A[0],G[1]-A[1]]
        vectorHI=[1,0]
        angleAGHI=math.acos((vectorAG[0]*vectorHI[0]+vectorAG[1]*vectorHI[1])/\
                         (pow(vectorAG[0]**2+vectorAG[1]**2,0.5)*1))*180/3.1415
        r=pow((O[0]-B[0])**2+(O[1]-B[1])**2,0.5)
        vectorOA=[A[0]-O[0],A[1]-O[1]]
        vectorOB=[B[0]-O[0],B[1]-O[1]]
        vectorOC=[C[0]-O[0],C[1]-O[1]]
        angleOAOC=math.acos((vectorOA[0]*vectorOC[0]+vectorOA[1]*vectorOC[1])/\
                     (pow(vectorOA[0]**2+vectorOA[1]**2,0.5)*pow(vectorOC[0]**2+vectorOC[1]**2,0.5)))*180/3.1415
        angleOAOB=math.acos((vectorOA[0]*vectorOB[0]+vectorOA[1]*vectorOB[1])/\
                     (pow(vectorOA[0]**2+vectorOA[1]**2,0.5)*pow(vectorOB[0]**2+vectorOB[1]**2,0.5)))*180/3.1415
        if vectorAG[1]>0 or vectorAG[1]==0: 
            t.seth(angleAGHI)
        else:
            t.seth(-angleAGHI)
        if vectorOA[0]*vectorOC[1]-vectorOC[0]*vectorOA[1]>0:
            r_parameter='+'
        elif vectorOA[0]*vectorOC[1]-vectorOC[0]*vectorOA[1]<0:
            r_parameter='-'
        t.pu()
        t.circle(eval(r_parameter+str(r)),angleOAOB)
        t.pd()
        t.circle(eval(r_parameter+str(r)),angleOAOC-angleOAOB)
        t.pu()
        t.goto(B[0],B[1])
        t.pd()
t.pu()
t.goto(Data[-1][1],Data[-1][2])
t.pd()
for i in range(1,101): #渐变色图注
    gradualchange(100,i)
    t.goto(Data[-1][1],Data[-1][2]-i)
t.hideturtle()
t.done()
