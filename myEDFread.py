def myEDFread(path):
    # runtime: 8.53 sec for a 26-channel 256Hz nighttime record
    import numpy as np
    fid=open(path,'rb')
    a=fid.read(236)
    ndr=int(fid.read(8)) #number of data records in sec
    drdur=float(fid.read(8)) #duration of each data record in sec
    ns=int(fid.read(4)) #number of signal channels
    Channels=[]
    for i in range(0,int(ns)):
        Channels.append(fid.read(16).decode('UTF-8')) # changing bytes to str
    tdu=fid.read(ns*80) #transducer type
    units=fid.read(ns*8) #physical dimensions
    phmn=[]
    phmx=[]
    dmn=[]
    dmx=[]
    for i in range(0,int(ns)):
        phmn.append(float(fid.read(8))) # physical min
    for i in range(0,int(ns)):
        phmx.append(float(fid.read(8))) # physical max
    for i in range(0,int(ns)):
        dmn.append(float(fid.read(8))) # digital min
    for i in range(0,int(ns)):
        dmx.append(float(fid.read(8))) # digital max
    scalefac=[]
    for i in range(0,len(phmn)):
        scalefac.append((phmx[i]-phmn[i])/(dmx[i]-dmn[i]))
    dc=[]
    for i in range(0,len(phmn)):
        dc.append(phmx[i]-scalefac[i]*dmx[i])
    prefilters=fid.read(ns*80) #prefilters 
    nr=[]
    for i in range(0,ns):
        nr.append(int(fid.read(8))) #samples per data record
    if sum(nr)/len(nr)==nr[0]:
        fs=nr[0]/int(drdur)
    else:
        disp('cannot proceed. one of the channels has a different sampling rate')
    othr=fid.read(ns*32)
    X=np.zeros((ns,int(nr[0]*ndr)))
    for i in range(0,ndr):
        for j in range(0,ns):
            X[j][i*nr[j]:(i+1)*nr[j]]=np.fromstring(fid.read(nr[j]*2),  'int16')*scalefac[j]+dc[j]
    fid.close()
    return X, fs, Channels
