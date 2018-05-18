def myEPOCHpower(X, fs, epl):
    # X: Data matrix with channels in row
    # fs: sampling rate (Hz), use int(fs)
    # epl: sleep scoring epoch length (e.g. 30 sec)
    # returns power spectrum P for every channel and epoch in every frequencies in f
    from scipy import signal
    for i in range(1, 4*fs):
        if (2 ** i >= 4*fs):
            win=2 ** i
            break
    P=[]
    for i in range(0,X.shape[0]):
        P.append([])
    for i in range(0,X.shape[0]):
        for j in range(0,int(X.shape[1]/(epl*fs))):
            f, Pxx_den = signal.welch(X[i][j*epl*fs:(j+1)*epl*fs], fs=fs, window='hanning', nperseg=win, noverlap=win/2, nfft=win, detrend='constant', return_onesided=True, scaling='density', axis=-1)
            P[i].append(Pxx_den)
    return P, f
