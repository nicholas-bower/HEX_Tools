import numpy as np
import itertools
import matplotlib.pyplot as plt
from Hex_Analyzer import *

#filepathIV='/mnt/c/Users/Nicholas Bower/Documents/'
filenameIV = 'HPK_8in_198ch_2019_2102_coarse_IV'
filepathIV='/mnt/c/Users/Nicholas Bower/Documents/'
#filenameIV = 'HPK_8in_198ch_2019_IV_TroubleShoot_IV (1)'


filepathCV='/mnt/c/Users/Nicholas Bower/Documents/'
filenameCV = 'HPK_8in_198ch_2019_2102_coarse_CV'  
wafernumber = '2102_PreArc_CV'
OutFile_Dir = '/mnt/c/Users/Nicholas Bower/Documents/HPK_300um_'+wafernumber+'/'
checkAndMakeDir(OutFile_Dir)
outFileName = OutFile_Dir+'HPK_300um_'+wafernumber
corr = readfile('/mnt/c/Users/Nicholas Bower/Documents/HPK_8in_198ch_2019_CV _correction_short_CV (1).txt')

#Read files using method from HEX_Analyzer
CV = readfile(filepathCV + filenameCV + '.txt')
IV=readfile(filepathIV + filenameIV + '.txt')
plot_totalCurrent(CV, outFileName)
#plot_IV_By_Channel(IV,  outFileName, 100)
channels = [7, 12, 66, 8 , 16, 6,17 ,18, 81] 
#plot_singleChannel(IV,199, outFileName,'IV')
#plot_Channels(channels, corr, IV, CV, outFileName)
#plot_Humidity(IV, outFileName)
#calc_GRIV(IV, outFileName)