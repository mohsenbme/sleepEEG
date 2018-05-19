import os
import numpy as np
data_dir='/Volumes/Mohsen/PSTIM/allscalp/'
if not os.path.exists(data_dir+'power30sec_py'):
    os.makedirs(data_dir+'power30sec_py')
swa_f=[0.5, 4] # slow wave activity range, also known as SO+delta
theta_f=[5, 8]
slowspindle_f=[9, 11]
fastspindle_f=[11, 15]
alpha_f=[8, 13]
beta_f=[5, 25]

allf=os.listdir(data_dir)
isedf=[]
for i in range(0,len(allf)):
    if allf[i][-3::]=='edf':
        isedf.append(i)
allf[isedf[0]]
for sj in range(0,len(isedf)):
    name=allf[isedf[sj]]
    print(name)
    if name=='PSTIM_727_V4.edf' or name=='PSTIM_746_V3.edf' or name=='PSTIM_752_V3.edf':
        mat_contents = sio.loadmat(data_dir+'concatenated files/'+name[:-4]+'.mat')
        X = mat_contents['X']
        mrk= mat_contents['mrk']
#         val=stageData[0,0]
#         mrk=val['stages']
        fs= mat_contents['fs']
    else:
        X, fs, Channels = myEDFread(data_dir+name)
        print('EDF loaded')
        mat_contents = sio.loadmat(data_dir+name[:-4]+'.mat')
        stageData= mat_contents['stageData']
        val=stageData[0,0]
        mrk=val['stages']
    if len(Channels)==24:
        print('power spectrum estimation...')
        P, f=myEPOCHpower(X, int(fs), 30)
    elif len(Channels)==26:
        del Channels[0]
        del Channels[0]
        print('power spectrum estimation...')
        P, f=myEPOCHpower(X[2::], int(fs), 30)
        
    r=len(P)
    c=len(P[0])
    sigma_fast_raw=np.zeros((r,c))
    sigma_fast_norm=np.zeros((r,c))
    sigma_slow_raw=np.zeros((r,c))
    sigma_slow_norm=np.zeros((r,c))
    theta_raw=np.zeros((r,c))
    theta_norm=np.zeros((r,c))
    swa_raw=np.zeros((r,c)) # slow wave activity
    swa_norm=np.zeros((r,c))
    alpha_raw=np.zeros((r,c))
    alpha_norm=np.zeros((r,c))
    beta_raw=np.zeros((r,c))
    beta_norm=np.zeros((r,c))
    print('sub-band power calculation')
    for i in range(0,len(P)):
        for j in range(0,len(P[i])):
            swa_raw[i][j], swa_norm[i][j]= subpower(P[i][j], f, swa_f[0], swa_f[1], 0.5)
            theta_raw[i][j], theta_norm[i][j]= subpower(P[i][j], f, theta_f[0], theta_f[1], 2)
            alpha_raw[i][j], alpha_norm[i][j]= subpower(P[i][j], f, alpha_f[0], alpha_f[1], 2)
            beta_raw[i][j], beta_norm[i][j]= subpower(P[i][j], f, beta_f[0], alpha_f[1], 2)
            sigma_fast_raw[i][j], sigma_fast_norm[i][j]= subpower(P[i][j], f, fastspindle_f[0], fastspindle_f[1], 2)
            sigma_slow_raw[i][j], sigma_fast_norm[i][j]= subpower(P[i][j], f, slowspindle_f[0], slowspindle_f[1], 2)
    print('saving outputs to mat')
    sio.savemat(data_dir+'power30sec_py'+'/'+name[:-4]+'_pwr30sec',{"P":P,"f":f,"mrk":mrk,"Channels":Channels,"swa_raw":swa_raw,"swa_norm":swa_norm,"theta_raw":theta_raw,"theta_norm":theta_norm,"alpha_raw":alpha_raw,"alpha_norm":alpha_norm,"beta_raw":beta_raw,"beta_norm":beta_norm,"sigma_fast_raw":sigma_fast_raw,"sigma_fast_norm":sigma_fast_norm,"sigma_slow_raw":sigma_slow_raw,"sigma_slow_norm":sigma_slow_norm})
            


        
