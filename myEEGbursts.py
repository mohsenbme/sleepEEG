def myEEGbursts(X,fs,ind_epoch,fc,bw,thrfactor=4,epl=30,rjth=200,intrvmin=0.25):
    # X: EEG Data (re-referenced) with channels in rows (at least 2 channels are required)
    # fs: sampling rate in Hz (e.g., 256)
    # epl: scoring epoch length (e.g., 30)
    # ind_epoch: list of epoch indexes for the stage of interest (e.g., indices for stage 2)
    # fc: list(or array) of peak frequency of the burst activity (e.g. 12 Hz for spindle) for each channel
    # bw: bandwidth around fc for detecting bursts. for example for fs=12 Hz and bw=3 Hz, 10.5-13.5 Hz range is considered
    # rjth: epochs with maximum absolute value greater than rjth (e.g. 200 uV) will be discarded for baseline activity calculation
    # intrvmin: minimum duration for detected bursts (e.g. 0.25 sec)
    
    fc=np.array(fc)
    b2, a2 = signal.butter(4, 0.5/(fs/2), 'high')
    spindle_intrv=[]
    spindle_pks=[]
    
    for i in range(0,X.shape[0]):
        spindle_intrv.append([])
        spindle_pks.append([])
        
    
    for j in range(0,3):#X.shape[0]):
        # finding clean epochs for baseline activity calculation
        print(j)
        ind_cln=[]
        for e in range(0,len(ind_epoch)):
            if max(abs(signal.filtfilt(b2,a2,X[j][int(ind_epoch[e]*epl*fs):int((ind_epoch[e]+1)*epl*fs)])))<rjth:
                ind_cln.append(ind_epoch[e])
                
        # wavelet spectrogram and baseline activity calculation for each channel
        tmpth=[] 
        spec=[]
        for e in range(0,len(ind_epoch)):
            EP_energy = morlet_spectrogram(X[j][int(ind_epoch[e]*epl*fs):int((ind_epoch[e]+1)*epl*fs)],fs,[fc[j]-bw/2,fc[j]+bw/2], 0.1, 10, 5)
            av=np.mean(EP_energy,axis=0)**2
            spec.append(av)
            if sum([ np.sum(a == ind_epoch[e]) for a in ind_cln]):
                tmpth.append(np.mean(av))
        th=np.mean(tmpth)
        
        # finding EEG bursts by applying the criteria to the average spectrogram
        for e in range(0,len(ind_epoch)):
            intrv, pks = bnds_over_th(spec[e],thrfactor*th,ind_epoch[e]*epl*fs)
            for i in range(0,len(pks)):
                if (intrv[i][1]-intrv[i][0])/fs>intrvmin and max(abs(signal.filtfilt(b2,a2,X[j][int(intrv[i][0]):int(intrv[i][1])])))<(0.4*rjth):
                    spindle_intrv[j].append(intrv[i])
                    spindle_pks[j].append(pks[i])
    return spindle_intrv
       
