def myEPOCHpower(X, fs, ar, epl=30, rjth=300):
    # X: Data matrix with channels in row
    # fs: sampling rate (Hz), use int(fs)
    # ar: artifact rejection switch. set 1 if you want better estimation, but 0 if you want something fast
    # epl: sleep scoring epoch length (e.g. 30 sec)
    # returns power spectrum P for every channel and epoch in every frequencies in f
    from scipy import signal
    b2, a2 = signal.butter(4, 0.5/(fs/2), 'high')
    for i in range(1, 4*fs):
        if (2 ** i >= 4*fs):
            win=2 ** i
            break
    P=[]
    f=[]
    for i in range(0,X.shape[0]):
        P.append([])
        f.append([])
    for i in range(0,X.shape[0]):
        for j in range(0,int(X.shape[1]/(epl*fs))):
            x = X[i][j*epl*fs:(j+1)*epl*fs];
            if ar==1:
                rj=abs(signal.filtfilt(b2, a2, x))>rjth
                for ii in range(0,len(rj)):
                    if rj[ii]==True:
                        rj[ii-2*fs:ii+2*fs]=True
                x=x[~rj]
            
            if len(x)>8*fs:
                fp, Pxx_den = signal.welch(x, fs=fs, window='hanning', nperseg=win, noverlap=win/2, nfft=win, detrend='constant', return_onesided=True, scaling='density', axis=-1)
                P[i].append(Pxx_den)
                f[i].append(fp)
            else:
                P[i].append(np.zeros((1,int(win/2)+1))[0])
                f[i].append(np.zeros((1,int(win/2)+1))[0])
                    
    return P, f
