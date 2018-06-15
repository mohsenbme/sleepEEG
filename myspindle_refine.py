def myspindle_refine(X,spindle_intrv):
    for j in range(0,X.shape[1]):
        issp=[]
        print(len(spindle_intrv_stg2[j]))
        for i in range(0,len(spindle_intrv_stg2[j])):
            if not mytest_spindle(X[j][int(spindle_intrv[j][i][0]):int(spindle_intrv_stg2[j][i][1])],fs):
                issp.append(i)
        spindle_intrv[j]=np.delete(spindle_intrv[j],issp,0)
    return spindle_intrv

def mytest_spindle(x,fs):
    b2, a2 = signal.butter(4, 2/(fs/2), 'high')
    b1, a1 = signal.butter(4, 30/(fs/2), 'low')
    y = signal.filtfilt(b2, a2, x)
    y = signal.filtfilt(b1, a1, y)
    out= 0
    pl=(y[0:-2]*y[1:-1])<0
    zci=[i+1 for i, x in enumerate(pl) if x]
    if len(zci)>2:
        if len(zci)%2==0:
            del zci[-1]
        ncyc= (len(zci)-1)/2
        fest=fs/((zci[-1]-zci[0]+1)/ncyc)
        if fest>=9 and fest<=16:
            out=1
        else:
            out=0
    return out
