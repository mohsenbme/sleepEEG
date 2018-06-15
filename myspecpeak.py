def myspecpeak(P,f,ind,f1=9,f2=20):
    fpk=np.zeros((1,np.shape(P)[0]))
    fpk=fpk[0]
    for j in range(0,np.shape(P)[0]):
        tmpp=P[j]
        PN=np.array(P[j]).take(ind2,axis=0)
        res=0
        while res==0:
            fN=np.array(f[j]).take(ind2,axis=0)[0]
            res=fN[1]-fN[0]

        ind_f1=find_ind(fN,f1)
        ind_f2=find_ind(fN,f2)
        f_des=np.arange(f1, f2, res)
        m=PN[:,ind_f1:ind_f2].mean(axis=1)
        indf=[i for i, x in enumerate(m<(m.mean()+m.std())) if x]
        avP=PN[indf,ind_f1:ind_f2].mean(axis=0)
        pl=([np.logical_and((avP[1:-2]-avP[0:-3])>0,(avP[1:-2]-avP[2:-1])>0)])[0]
        ind_peaks=[i+1 for i, x in enumerate(pl) if x]
        p=avP[np.ix_(ind_peaks)]
        f_peaks=f_des[np.ix_(ind_peaks)]
        if len(ind_peaks)>1:
            p=p[(f_peaks>=11) & (f_peaks<=13.5)]
            f_peaks=f_peaks[(f_peaks>=11) & (f_peaks<=13.5)]
        if len(p)>1:
            f_peaks=f_peaks[np.argmax(p)]
            p=[p[np.argmax(p)]]
        if len(p)==0:
            f_peaks=f_des[np.argmax(avP)]
            p=avP[np.argmax(avP)]
        fpk[j]=f_peaks
    tmpf=fpk
    for  j in range(0,len(fpk)):
        if fpk[j]==f1 or fpk[j]==f2:
            fpk[j]=tmpf[(fpk!=f1) & (fpk!=f2)].mean()
    return fpk
