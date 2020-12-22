import numpy as np
import itertools
import matplotlib.pyplot as plt
from Hex_Analyzer import *

#filepathIV='/mnt/c/Users/Nicholas Bower/Documents/'
filenameIV = 'HPK_8in_198ch_2019_HPK_1003_300um_Coarse_IV'
filepathIV='/mnt/c/Users/Nicholas Bower/Downloads/'
#filenameIV = 'HPK_8in_198ch_2019_IV_TroubleShoot_IV (1)'


filepathCV='/mnt/c/Users/Nicholas Bower/Downloads/'
filenameCV = 'HPK_8in_198ch_2019_1003_Fine_retest_CV'  
wafernumber = 'HPK_8in_198ch_2019_1003'
OutFile_Dir = '/mnt/c/Users/Nicholas Bower/Documents/'+wafernumber+'/'
checkAndMakeDir(OutFile_Dir)
outFileName = OutFile_Dir
corr = readfile('/mnt/c/Users/Nicholas Bower/Documents/HPK_8in_198ch_2019_CV _correction_short_CV (1).txt')
#corr = readfile('/mnt/c/Users/Nicholas Bower/Downloads/HPK_8in_444ch_CV_corr_CV.txt')
IV=readfile(filepathIV + filenameIV + '.txt')
#Read files using method from HEX_Analyzer
CV = readfile(filepathCV + filenameCV + '.txt')
plot_CV_ByChannel(CV,outFileName, wafernumber)
#plot_CV_ByChannel(corr, OutFile_Dir+"Correction/", wafernumber)
plot_totalCurrent(IV, outFileName)
plot_IV_By_Channel(IV,  outFileName, 300, corr, CV)
channels = [ 14, 100, 134 , 52,90,120, 137,138, 199] 
plot_Channels(channels, corr, IV, CV, outFileName)
plot_Humidity(IV, outFileName)
#calc_GRIV(IV, outFileName)
plot_average_profile_IV(IV,outFileName, 300, False)###### The threshold is the a positive value which limits the current of cells to be averaged. if the threshold is negative it wont included them
plot_average_profile_CV(CV,outFileName, corr, True)