#用于聚集行为的运算，无需对fiji导出的坐标文件处理
#请仔细阅读注释
for filename in ['p114nci 原始数据']: #所要计算的坐标信息文件名列表
    spaceoftime=100 #int#帧间隔，单位毫秒
    importdir='H:/microscope data/20210515x/Coordinate data/' #导入文件所在文件夹位置
    exportdir='C:/Users/60925/Desktop/' #导出文件所在文件夹位置
    exportfilename=filename+'t_NN0' #导出文件命名
    
    importlayout='.csv'#导入文件格式
    exportlayout='.csv'#导出文件格式
    importfilename=filename#str
    importfilepath=importdir+importfilename+importlayout
    #proportion=0.09091#float 40x0.09091;60x0.06135
    exportfilepath=exportdir+exportfilename+exportlayout
    print(filename)
    import time
    import os
    timestart=time.perf_counter()
    f=open(importfilepath,'rb')
    off=-50
    while True:
        f.seek(off,2)
        lines=f.readlines()
        if len(lines)>=2:
            nomax=list(map(eval,str(lines[-1]).replace("b'","").replace("\\r\\n'","").split(',')))[0]
            break
        else:
            off-=50
    f.close()
    f=open(importfilepath)
    Slice1=[]
    for line in f:
        if line==' ,Area,X,Y,Slice\n':
            continue
        else:
            line=list(map(eval,line.replace("\n","").split(',')))
            if line[-1]==1:
                Slice1.append(line)
            else:
                N0=len(Slice1)
                break
    f.seek(0)
    Slice=1;t_NN0ls=[['Time','N/N0'],['s',''],['',importfilename]];N=0
    for line in f:
        if line==' ,Area,X,Y,Slice\n':
            continue
        else:
            line=line.replace("\n","").split(',')
            if eval(line[0])%1000000==0:
                times=time.perf_counter()-timestart
                print('已完成：{0:.2f}% 执行时间：{1:.0f}分{2:.0f}秒'.format(eval(line[0])/nomax*100,times//60,times%60))
            if eval(line[-1])==Slice:
                N+=1
            else:
                t=(Slice-1)*spaceoftime/1000
                #if t==850:
                #    break
                t_NN0=N/N0
                t_NN0ls.append([t,t_NN0])
                N=0
                Slice+=1
                N+=1
    f.close()
    def exportlist2(ls,path):
        f=open(path,"w")
        for item in ls:
            f.write(str(item).strip("[]").replace(" ","").replace("'","")+"\n")
        f.close()
    exportlist2(t_NN0ls,exportfilepath)
    #os.system('shutdown /s /t 300')