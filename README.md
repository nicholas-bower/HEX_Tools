# HEX_Tools
 Tools for handling hex data collected by HEX. Formatted to take outputs from HEXDAQ.*
##Dependances
Python 2.7 or more recent [Python 2.7 may now be depreciated]
matplotlib libries.[typically installed with most python packages]
##Masked Pads
If pads are masked manually within HEX DAQ they are listed in the datafile. This unfortunately causes an error that I have yet to resolve within HEXGrapher. The solution to this is to simply delete the list of masked cells from the data (.txt) file. HEXGrapher does not need this list to mask the cells.***

***I will hopefully resolve this!!! 

##Run Instructions
The user interface is currently run through HEX Grapher. This week I hope to adjust it so it can also take arguments passed in by the terminal or by the labview program.

Currently you must specify the following : filenameIV, filepathIV, filepathCV, filenameCV, wafernumber, OutFile_Dir, corr and channels.

##Methods
HEX Analyzer utilizes the following methods. I will describe the methods utilized in the header file :
'readfile("File name and location")'
Takes a single stirng as an argument. It returns a tuple containing all of the necessary data.
'plot_CV_ByChannel(tuple(CV),string(Out file name), string(wafer number))'
Plots C vs Channel. The output is similar to that made by HEXDAQ. 
'plot_IV_ByChannel(tuple(IV),string(Out file name),  double(mask pads above),tuple(correction), tuple(CV), string(wafer number))'
Produces a pair of I vs channel plots. The first does no masking. The second masks all cells with current above the threshold specified in the argument. For these bad pads it will automatically make IV and CV curves.
'plot_CV_ByChannel(tuple(CV),string(Out file name), string(wafer number))'

To be continued.

