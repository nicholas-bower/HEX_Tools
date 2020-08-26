import numpy as np
import itertools
import matplotlib.pyplot as plt
from Hex_Analyzer import *

#filepathIV='/mnt/c/Users/Nicholas Bower/Documents/'
filenameIV = 'HPK_8in_198ch_2001_FullScan_IV'
filepathIV='/mnt/c/Users/Nicholas Bower/Documents/'
#filenameIV = 'HPK_8in_198ch_2019_IV_TroubleShoot_IV (1)'


filepathCV='/mnt/c/Users/Nicholas Bower/Documents/'
filenameCV = 'HPK_8in_198ch_2001_FullScan_CV'  
wafernumber = '2001'
OutFile_Dir = '/mnt/c/Users/Nicholas Bower/Documents/HPK_300um_'+wafernumber+'/'
checkAndMakeDir(OutFile_Dir)
outFileName = OutFile_Dir+'HPK_200um_'+wafernumber
corr = readfile('/mnt/c/Users/Nicholas Bower/Documents/HPK_8in_198ch_2019_CV _correction_short_CV (1).txt')
IV=readfile(filepathIV + filenameIV + '.txt')
#Read files using method from HEX_Analyzer
CV = readfile(filepathCV + filenameCV + '.txt')

plot_totalCurrent(IV, outFileName)
plot_IV_By_Channel(IV,  outFileName, 100, corr, CV)
channels = [ 14, 21] 
plot_Channels(channels, corr, IV, CV, outFileName)
plot_Humidity(IV, outFileName)
calc_GRIV(IV, outFileName)
plot_average_profile_IV(IV,outFileName, 300)###### The threshold is the a positive value which limits the current of cells to be averaged. if the threshold is negative it wont included them

plot_average_profile_CV(CV,outFileName)