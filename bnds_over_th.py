def bnds_over_th(a,th,ep_beg):
    # a is an array
    # threshold
    # ep_beg: epoch first point index in the sleep record (put 0 if not applicable)
    intrv=[]
    pks=[]
    overt=[i for i, x in enumerate(a>th) if x]
    pos=[]
    if len(overt)>0:
        pos.append(overt[0])
        df=[overt[i+1]-overt[i] for i in range(0,len(overt)-1)]
        for i in range(0,len(df)):
            if df[i]!=1:
                pos.append(overt[i])
                pos.append(overt[i+1])
        pos.append(overt[-1])
        if a[pos[0]-1]>a[pos[0]+1]:
            del pos[0]
        if len(pos)%2==1:
            del pos[-1]

        for i in range(0,int(len(pos)/2)):
            intrv.append(pos[i*2:(i+1)*2])
        pks=[]
        for i in range(0,len(intrv)):
            pks.append(max(a[intrv[i][0]:intrv[i][1]+1]))
        if ep_beg>0:
            if len(intrv)>0:
                for i in range(0,len(intrv)):
                    intrv[i][0]= intrv[i][0]+ep_beg
                    intrv[i][1]= intrv[i][1]+ep_beg
    return intrv, pks
