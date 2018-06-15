# sleepEEG
Follow these steps to extract spindles:
1) read edf files by myEDFread to get data X, channel names, and sampling rate fs
2) import marker files and store stages in variable mrk
3) calculate power spectrum P for every epoch: myEPOCHpower
4) find spindle peaks by myspecpeak
5) detect spindles by myEEGbursts
6) refine the detected spindles by myspindle_refine
