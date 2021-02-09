import numpy as np
import itertools
import matplotlib.pyplot as plt
from Hex_Analyzer import *

filenameIV = 'HPK_8in_198ch_2019_1014_FSU_crossscheck_2_8_21_IV'
filepathIV='/mnt/c/Users/nicho/Downloads/'


filepathCV='/mnt/c/Users/nicho/Downloads/'
filenameCV = 'HPK_8in_198ch_2019_1014_FSU_crossscheck_2_8_21_CV'  
wafernumber = 'HPK_198ch_1014_Crosscheck'
OutFile_Dir = '/mnt/c/Users/nicho/Downloads/'+wafernumber+'/'
checkAndMakeDir(OutFile_Dir)
outFileName = OutFile_Dir
corr= readfile('/mnt/c/Users/nicho/Downloads/HPK_8in_198ch_2019_openCV_2_2_21_CV.txt')
#corr = readfile('/mnt/c/Users/nicho/Downloads/HPK_8in_444ch_CV_CorrectionDec_15_2020_CV.txt')
IV=readfile(filepathIV + filenameIV + '.txt')
#Read files using method from HEX_Analyzer
CV = readfile(filepathCV + filenameCV + '.txt')
plot_CV_ByChannel(CV,outFileName, wafernumber)
plot_totalCurrent(IV, outFileName,wafernumber)
plot_IV_By_Channel(IV,  outFileName, 300, corr, CV,wafernumber)
channels = [ 14, 100, 134 , 52,90,120, 137,138, 199] 
plot_Channels(channels, corr, IV, CV, outFileName,wafernumber)
plot_Environmental(IV, outFileName)
#calc_GRIV(IV, outFileName)
plot_average_profile_IV(IV,outFileName, 300, False,wafernumber)###### The threshold is the a positive value which limits the current of cells to be averaged. if the threshold is negative it wont included them
plot_average_profile_CV(CV,outFileName, corr, False,wafernumber)
