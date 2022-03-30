#给出粒子运动的t-v数据，所有粒子的均值
#请仔细阅读注释
import numpy as np
from scipy.interpolate import UnivariateSpline
import matplotlib.pyplot as plt
#载入二维数据，调试用
def importData2D(path):
    ls=[]
    Data=open(path)
    for line in Data:
        line=line.replace("\n","").split(',')
        ls.append(line)
    Data.close()
    return ls
#importData #输入值为.txt或csv格式的文件路径，共四列area,x,y,slice,注意删除fiji导出数据的第一行;返回列表，第一层列表为列表格式储存，第二层列表将每一帧点数据分为一组，第三层是每一点的数据分别为area,x,y,slice.
def importData(path):
    Data=open(path)
    slices=1
    ls=[[]]
    for line in Data:
        line=line.replace("\n","").split(',')
        if int(line[-1])==slices:
            ls[slices-1].append(list(map(eval,line)))
        else:
            slices+=1
            ls.append([])
            ls[slices-1].append(list(map(eval,line)))
    Data.close()
    lsresl=[] #洗去重复帧,帧数值重新排序
    for n in range(len(ls))[:-1]:
        lsn0=[];lsnp0=[]
        for point in ls[n]:
            pointn=eval(str(point))
            pointn[-1]=0
            lsn0.append(pointn)
        for point in ls[n+1]:
            pointnp=eval(str(point))
            pointnp[-1]=0
            lsnp0.append(pointnp)
        if lsn0==lsnp0:
            lsresl.append(ls[n])
        else:
            continue
    for item in lsresl:
        ls.remove(item)
    for n in range(len(ls)):
        for point in ls[n]:
            point[-1]=n+1
    return ls
#number particles
def numberparticles(RawData):#输入值为importData返回的列表;返回列表共三层，第一层表示列表格式存储，第二层表示不同的粒子，第三层为每一点的数据area,x,y,slice.不要求输入的帧连续
    particles=[]
    for i in RawData[0]:
        particles.append([i])
    n=0
    while n<len(RawData)-1:
        for pointn in RawData[n]:
            number=-1;minn=1700;numbermin=-1
            for pointnp in RawData[n+1]:
                number+=1
                d=pow(((pointn[1]-pointnp[1])**2+(pointn[2]-pointnp[2])**2),0.5)
                if d<minn and d<150 and abs(pointn[0]-pointnp[0])<100:#由粒子运动速度调整d，速度越大d越大
                    minn=d
                    numbermin=number
                else:
                    continue
            if minn==1700:
                continue
            else:
                for particle in particles:
                    if particle[-1]==pointn:
                        particle.append(RawData[n+1][numbermin])
                        break
                    elif particle==particles[-1]:
                        if particle[-1]==pointn:
                            particle.append(RawData[n+1][numbermin])
                            break
                        else:
                            particles.append([RawData[n+1][numbermin]])
                            break
        n+=1
    return particles
#export list 2层
def exportlist2(ls,path):
    f=open(path,"w")
    for item in ls:
        f.write(str(item).strip("[]").replace(" ","").replace("'","")+"\n")
    f.close()
#export list 3层
def exportlist3(ls,path):
    f=open(path,"w")
    for particle in ls:
        for point in particle:
            f.write(str(point).strip("[]").replace(" ","").replace("'","")+"\n")
        f.write("\n")
    f.close()
#export list 3层拆为2层按文件输出
def exportlist3to2(ls,path):
    pathf=path[:-4];pathb=path[-4:]
    for n in range(len(ls)):
        exportlist2(ls[n],pathf+str(n)+pathb)
#give particles_t_s list 输入经过numberparticles处理后的列表，每帧时间间隔time,像素与长度的换算系数proportion。
#返回一个三层列表，第一层表示以列表储存，第二层表示不同个的粒子，第三层为每一个粒子在相应帧走过的总路程s(μm)与总位移时间t(ms)。
def give_particles_t_s(particles,Time,proportion): 
    particles_t_s=[]
    for particle in particles:
        if len(particle)<50:#帧数小于50的粒子不进入计算，排除异常标记
            continue
        else:
            particles_t_s.append([])
            particles_t_s[-1].append([(particle[0][-1]-1)*Time,0])
            s=0
            for n in range(len(particle)-1):
                s+=pow((particle[n][1]-particle[n+1][1])**2+(particle[n][2]-particle[n+1][2])**2,0.5)*proportion
                t=(particle[n+1][-1]-1)*Time
                particles_t_s[-1].append([t,s])
    death=[]#去除死粒子
    for pa in range(len(particles_t_s)):
        if (particles_t_s[pa][-1][1]-particles_t_s[pa][0][1])/\
            (particles_t_s[pa][-1][0]-particles_t_s[pa][0][0])<0.00026884:
               death.append(pa) 
    death.reverse()
    for i in death:
        particles_t_s.remove(particles_t_s[i])
    #对s-t进行平滑操作，防止微分后起伏过大
    #particles_t_ssmmo=[]
    #for particle in particles_t_s:
    #    particlesmmo=[]
    #    pa=np.array(particle)
    #    s=UnivariateSpline(pa[:,0],pa[:,1],s=2)
    #    x=pa[:,0].tolist()
    #    y=s(pa[:,0]).tolist()
    #    for n in range(len(x)):
    #        particlesmmo.append([x[n],y[n]])
    #    particles_t_ssmmo.append(particlesmmo)
    #particles_t_s=particles_t_ssmmo
    return particles_t_s
#particles_t_s list convert to particles_t_v list #对particles_t_s list进行微分ds/dt,输出微分后的列表。
#列表共三层，第一层，第二层表示不同个的粒子，第三层为每一个粒子在相应帧的时间t(ms)与速度vn(μm/ms)
def t_stot_v(particles_t_s):
    particles_t_v=[]
    for particle in particles_t_s:
        if len(particle)>=3:
            particles_t_v.append([])
            for n in range(len(particle)-1)[1:]:
                vn=(particle[n+1][1]-particle[n-1][1])/(particle[n+1][0]-particle[n-1][0])
                t=particle[n][0]
                particles_t_v[-1].append([t,vn])
        else:
            continue
############################
    longest=0
    for particle in particles_t_v:
        if len(particle)>longest:
            longest=len(particle)
        else:
            continue
    for particle in particles_t_v:
        if len(particle)<longest:
            for i in range(longest-len(particle)):
                particle.append([np.nan,np.nan])
    aparticles_t_v=np.array(particles_t_v)#去除每一粒子离群的速度
    mean=np.nanmean(aparticles_t_v[:,:,1],axis=1) #1D
    SD=np.nanstd(aparticles_t_v[:,:,1],axis=1)#1D
    judge=(abs(aparticles_t_v[:,:,1].swapaxes(0,1)-mean)<3*SD).swapaxes(0,1)
    for pa in range(len(judge)):
        for po in range(len(judge[pa])):
            if judge[pa][po]==False:
                aparticles_t_v[pa][po]=[np.nan,np.nan]
    a_psv=np.nansum(aparticles_t_v[:,:,1],axis=1)
    aparticles_t_v=np.delete(aparticles_t_v,(a_psv==0).nonzero(),axis=0)#删除全nan粒子
    a_psv=np.nansum(aparticles_t_v[:,:,1],axis=1)
    mean=np.nanmean(a_psv)#去除离群的粒子
    SD=np.nanstd(a_psv)
    judge=abs(a_psv-mean)<3*SD
    for pa in range(len(judge)):
        if judge[pa]==False:
            aparticles_t_v=np.delete(aparticles_t_v,pa,axis=0)
    aparticles_t_v[np.isnan(aparticles_t_v).nonzero()]=0 #剔除列表中的nan
    particles_t_v=aparticles_t_v.tolist()         
    for particle in particles_t_v:
        while [0,0] in particle:
            particle.remove([0,0])
    while [] in particles_t_v:
        particles_t_v.remove([])
##############################    
    return particles_t_v
#计算每一帧粒子的平均速度，返回列表t-va(time(s),v average(μm/s)
def t_va(particles_t_v,importfilename,space_of_time):
    maxtime=0
    for particle in particles_t_v:
        for point in particle:
            if point[0]>maxtime:
                maxtime=point[0]
            else:
                continue
    maxtime=int(maxtime)
    t_vc={}
    for time in range(maxtime+1)[::space_of_time][1:]:
        t_vc[str(time)+'.0']=[]
#######################
    for particle in particles_t_v:
        for point in particle:
            t_vc[str(point[0])].append(point[1])#t(ms),vc(μm/ms)
    for k in t_vc:
        arrtv=np.array(t_vc[k])
        mean=np.mean(arrtv)#去除同一时间，速度值离群的粒子速度
        SD=np.std(arrtv)
        arrtv=np.delete(arrtv,((arrtv-mean)>3*SD).nonzero())
        t_vc[k]=arrtv.tolist()
    t_va=[['Time','speed'],['s','μm/s'],['',importfilename]]
    for k in t_vc:
        if len(t_vc[k])!=0:
            t=eval(k)
            va=sum(t_vc[k])/len(t_vc[k])
            t_va.append([t/1000,va*1000])#t(s),va(μm/s)
    x=np.array(t_va[3:])[:,0]
    y=np.array(t_va[3:])[:,1]
    plt.plot(x,y,'o')
    plt.title(importfilename)
    plt.show()
    return t_va
#自动生成filename
def generatefilename(): 
    filenamels=[]
    for a in ['40','60','80','100']:
        for b in range(3):
            if b==0:
                filename=str(a)
            else:
                filename=str(a)+'-'+str(b)
            filenamels.append(filename)
    return filenamels
#文件名设置，参数设置,与函数调用。输入文件名，输出文件名为‘输入文件名’+‘t_va’

for filename in ['100']: #所要处理的坐标信息文件的文件名的列表，注意确保这些坐标信息已经删除了第一行文本信息。
    space_of_time=100 #int 每一帧的间隔时间单位ms
    proportion=0.09091 #float 40x0.09091;60x0.06135 像素点长度对应的实际长度
    importdir='H:/microscope data/20210707x/DANGE/Coordinate data/' #导入文件所在文件夹位置
    exportdir='C:/Users/60925/Desktop/' #导出文件所在文件夹位置
    
    importlayout='.csv' #导入文件格式
    exportlayout='.csv' #导出文件格式
    exportfilename=filename+'t_va' #str 导出文件后缀名   
    importfilename=filename#str
    importpath=importdir+importfilename+importlayout
    exportpath=exportdir+exportfilename+exportlayout
    exportlist2(t_va(t_stot_v(give_particles_t_s(numberparticles(importData(importpath)),space_of_time,proportion)),importfilename,space_of_time),exportpath)
    print(filename)
#exportlist3to2((give_particles_t_s(numberparticles(importData('20.csv')),100,0.09091)),'20ts.csv')
#main('100-2')
#main(generatefilename())
#print(generatefilename())
#exportlist3(numberparticles(importData('E:/microscope data/20210707/DANGE/Coordinate data/80-1_726-760.csv')),'E:/microscope data/20210707/DANGE/Coordinate data/xx.csv')

