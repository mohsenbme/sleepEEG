def subpower(P, f, f1, f2, nfl):
    # returns power (rawP) and relative power(normP) for frequencies in range f1<f<f2
    # nfl: the minimum freq for normalized power calculation 
    # f and P: outputs from myEPOCHpower function
    ind_f1=find_ind(f,f1)
    ind_f2=find_ind(f,f2)
    rawP=sum(P[ind_f1:ind_f2])*(f[2]-f[1])
    ind_2hz=find_ind(f,nfl) # nfl=2 Hz
    totalp=sum(P[ind_2hz::])*(f[2]-f[1])
    normP=rawP/totalp
    return rawP, normP
