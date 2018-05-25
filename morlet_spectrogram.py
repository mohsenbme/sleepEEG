import numpy as np
def morlet_spectrogram(sig, samp_rate, freq_range, f_step, wave_num, timescale):
    # example freq_range: [2, 18]
    # f_step: freq resoulution in Hz (e.g., 0.1 Hz)
    # wave_num: parameter for number of sinuspidal cycles in a morlet, 10 worked well for eeg
    # timescale: 5 worked well for eeg
    frecs=np.arange(freq_range[0], freq_range[1]+f_step, f_step)
    len_sig = len(sig)
    samp_period = 1/samp_rate
    row_coef = len(frecs)
    col_coef = len_sig
    EP_energy= np.zeros((row_coef,col_coef))
    for k in range(0,row_coef):
        SD_f = frecs[k]/wave_num
        SD_t = 1/(2*np.pi*SD_f)
        x=np.arange(-timescale*SD_t, timescale*SD_t+samp_period, samp_period)
        Morlets = (1/np.sqrt(SD_t*np.sqrt(np.pi))) * (np.exp( -(x**2)/(2*SD_t**2) ) * np.exp(1j*2*np.pi*frecs[k]*x ))
        Morlets=Morlets[[i for i, x in enumerate(abs(Morlets)>=max(abs(Morlets))/100) if x]]
        coef_freq = np.convolve(sig,Morlets)
        EP_energy[k] = (abs(coef_freq)**2)[round(len(Morlets)/2):col_coef+round(len(Morlets)/2)]
    return EP_energy
        
                                                   

