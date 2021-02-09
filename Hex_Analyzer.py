import numpy as np
import itertools
import matplotlib.pyplot as plt
import os
import glob
from matplotlib import rc

#rc('font', **{'family':'serif','serif':['Palatino']})
#rc('text', usetex=True)

def checkAndMakeDir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)

def clearDir(dir):
    for fil in glob.glob(dir+"/*"):
        os.remove(fil)

def readfile(infile):
    f = open(infile, "r")
    data = np.zeros((500000,9), float)
    i=0
    for l in f:
        #print l
        if l[0]=='#':continue
        #if l[0]!='-':continue#####Requires the use of negative voltage
        r = l.split('\t')
        #print r
        try: 
            data[i,:9]=r[:9]
        except:
            continue
        i+=1
    mask = np.zeros(len(data), dtype = bool)
    mask=[data[:,2]!=0]
    f.close()
    return data[tuple(mask)]
def plot_IV_By_Channel(data, name, mask_abov, corr, CV,wafer):
    outfolder = name+"IV_by_Channel/"
    checkAndMakeDir(outfolder)
    voltages = set(data[:,0])
    voltages = sorted(voltages)
    fig = plt.figure()
    ax  = fig.add_subplot(111)
    colors = itertools.cycle(['r', 'b', 'g','m','c','y','k'])
    activepad_mask = [data[:,1]<199]
    data=data[tuple(activepad_mask)]
    for v,col in zip(voltages,colors):
        v_mask = [data[:,0]==v]
        v_data = data[tuple(v_mask)]
        color = next(colors)
        ax.plot(v_data[:,1], v_data[:,2], color, label = str(v)+'V')
    ax.set_title('IV by Channel'+"[" +wafer+"]")
    ax.set_ylabel('Current (nA)')
    ax.set_xlabel('Channel')
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(outfolder+wafer+ '_byChannel.png')
    plt.close('all')
    fig=plt.figure()
    ax = fig.add_subplot(111)
    abscurrent = np.zeros((len(data)))
    abscurrent[:]= [abs(ele) for ele in (data[:,2])]

    badpad_mask = [(abscurrent[:]>mask_abov) ]# find the cells with current greater than 10000 when the voltage has reached 100
    badpads = data[tuple(badpad_mask)]
    badcells = tuple(set(badpads[:,1]))
    #print (str(badcells))
    #plot_Channels(badcells, corr, data, CV, name, wafer)
    for v,col in zip(voltages,colors):
        v_mask = [data[:,0]==v]
        v_data = data[tuple(v_mask)]
        msk= [(ele not in badcells) for ele in v_data[:,1]]
        Current=v_data[:,2]
        #print (str(Current))
        Cells=v_data[:,1]
        #print(str(Cells))
        Current=Current[msk]
        #print (str(Current))

        Cells=Cells[msk]
        #print (str(Cells))

        color = next(colors)
        ax.plot(Cells, Current, color, label = str(v)+'V')
    ax.set_title('IV by Channel[With \'Bad\' Channls removed]'+"[" +wafer+"]")
    ax.set_ylabel('Current (nA)')
    ax.set_xlabel('Channel')


    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))


    plt.savefig(outfolder+wafer+'_sortedByChannel.png')
    plt.close('all')
def plot_totalCurrent(data, name,wafer):
    outfolder = name+"total_current/"
    checkAndMakeDir(outfolder)
    voltages = set(data[:,0])
    voltages = sorted(voltages)
    fig = plt.figure()
    ax  = fig.add_subplot(111)
    colors = itertools.cycle(['r', 'b', 'g','m','c','y','k'])
    activepad_mask = [data[:,1]<199]
    #print (str(activepad_mask))
    activepad=data[tuple(activepad_mask)]
    for v,col in zip(voltages,colors):
        v_mask = [activepad[:,0]==v]
        v_data = activepad[tuple(v_mask)]
        color = next(colors)
        ax.plot(v_data[:,1], v_data[:,4], color, label = str(v)+'V')
    ax.set_title('Total Current'+"[" +wafer+"]")
    ax.set_ylabel('Current (nA)')
    ax.set_xlabel('Channel')
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(outfolder+wafer+ '_TotalCurrent.png')
    
    plt.close('all')
def plot_singleChannel(data, channel, name, t,wafer):
    if t=="IV":
        outfolder = name+"SingleChannel"+t+"/"
    else:
        outfolder = name+"SingleChannel"+t+"_Uncorrected/"

    checkAndMakeDir(outfolder)
    mask = [data[:,1]==channel]
    data=data[tuple(mask)]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(data[:,0], data[:,2])
    invCV= []
    if (t =='IV'):
        ax.set_title('IV Channel: '+ str(int(channel))+"[" +wafer+"]")
        ax.set_xlabel('Voltage (V)')
        ax.set_ylabel('I(na)')
        plt.savefig(outfolder+ '_Channel_' + str(int(channel))+t+'.png')
        plt.close('all')
    elif t=='CV':
        ax.set_title('CV Channel: '+ str(int(channel))+"[" +wafer+"]")
        ax.set_xlabel('Voltage (V)')
        ax.set_ylabel('C(pF)')
        plt.savefig(outfolder+wafer+'_Channel_' + str(int(channel))+t+'.png')
        plt.close('all')

        for x in data[:,2]:
            invCV.append(1/x**2)
        fig2 = plt.figure()
        ax2 = fig2.add_subplot(111)
        ax2.plot(data[:,0], invCV[:])
        ax2.set_title('InvSq CV, Channel: '+ str(int(channel))+"[" +wafer+"]")
        ax2.set_xlabel('Voltage (V)')
        ax2.set_ylabel('1/C^2(pF)')
        plt.savefig(outfolder+ wafer+'_Channel_INVCV' + str(int(channel))+t+'.png')
        plt.close('all')


    
def plot_CV_Corr(data, corr, channel, name,wafer):
    outfolder = name+"CVCorrected_Individual_Channels/"
    checkAndMakeDir(outfolder)
    mask= [data[:,1]==channel]
    data=data[tuple(mask)]

    mask = [corr[:,1]==channel]
    corr = corr[tuple(mask)]
    invCVSq=[]
    CVcorr = []
    #print ("Plotting Channel="+str(int(channel)))
    #print(str(data[:,0]))
    for i in range(len(data[:,0])):
        voltage=data[i,0]
        if (voltage%10)!=0:
            #print ("Mod 10 test)"+str(voltage))
            voltage =voltage +(voltage%10)
            #print ("Mod 10 test)"+str(voltage))
        if voltage>-220:
            iCor=corr[corr[:,0]==voltage]
        else: iCor=corr[corr[:,0]==-220]
        if len(iCor)<1:
            #print ("CV Correction missing for V="+str(data[i,0])+"V. Terminating CV Correction.")
            break
        #print ("Data="+str(data[i,2]))
        #print ("Cor="+str(iCor[0,2]))

        iData=(data[i,2])-((iCor[0,2]))
        CVcorr.append(iData)
        invCVSq.append(1/(iData**2))
        #if data[i,0]==-200:
        #print ("Cell " +str(int(channel))+" Cpf = " + str(iData))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(data[:,0], CVcorr[:])
    ax.set_title('CORRECTED CV Channel: '+ str(int(channel))+"[" +wafer+"]")
    ax.set_xlabel('Voltage (V)')
    ax.set_ylabel('C(pF)')
    plt.savefig(outfolder+ '_Channel_' + str(int(channel))+'_Corrected.png')
    plt.close('all')
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)

    ax2.plot(data[:,0], invCVSq[:])
    ax2.set_title('CORRECTED invSq CV Channel: '+ str(int(channel))+"[" +wafer+"]")
    ax2.set_xlabel('Voltage (V)')
    ax2.set_ylabel('1/C^2(pF)')
    plt.savefig(outfolder+wafer+ '_Channel_INVCVSq_' + str(int(channel))+'_Corrected.png')
    plt.close('all')

def plot_Channels(channels, corr,IV_data, CV_data, fi,wafer):
    for c in channels:
        plot_singleChannel(IV_data, c, fi, 'IV',wafer)
        plot_singleChannel(CV_data, c, fi, 'CV',wafer)
        plot_CV_Corr(CV_data, corr, c, fi,wafer)

def plot_Environmental(data, fi):
    outfolder = fi+"Environmental_Data/"
    checkAndMakeDir(outfolder)
    humidity = data[:,8]
    time = data[:,6]
    temp = data[:,7]
    fig,ax = plt.subplots()
    # make a plot
    ax.plot(time, temp, color="red")
    # set x-axis label
    ax.set_xlabel("Time (s)",fontsize=14)
    # set y-axis label
    ax.set_ylabel("Temp (C)",color="red",fontsize=14)
    ax.set_ylim(20,26)
    # twin object for two different y-axis on the sample plot
    ax2=ax.twinx()
    # make a plot with different y-axis using second axis object
    ax2.plot(time, humidity,color="blue")
    ax2.set_ylabel("Humidity (%)",color="blue",fontsize=14)
    ax2.set_title("Environmental data")
    ax2.set_ylim(45,53)

    # save the plot as a file
    fig.savefig(outfolder+'_Environmental.png',
            format='png',
            dpi=100,
            bbox_inches='tight')

def calc_GRIV(data, fi):
    voltages = set(data[:,0])
    voltages = sorted(voltages)
    outfolder = fi+"GR_Extrapolation/"
    checkAndMakeDir(outfolder)
    I_GR=[]
    I_Total = []
    I_Sum = []
    for v in voltages:
        mask = [data[:,0]==v]
        vstep = data[mask]
        GR = vstep[vstep[:,1]==199]
        vstep=vstep[vstep[:,1]!=199]
        total_Current =GR[0,4]
        sum_Current = sum(vstep[:,2])
        I_Total.append(abs(total_Current))
        I_Sum.append(abs(sum_Current))
        I_GR.append(abs(total_Current-sum_Current))
    fig,ax = plt.subplots()
    #print (str(I_Total[:]))
    #print (str(I_Sum[:]))
    ax.plot(voltages, I_Total, label="Total Current at 199",color="red")
    ax.plot(voltages, I_Sum, label="Sum of currents",color = "blue")
    ax.plot(voltages, I_GR, label = "GR(Est)", color = "black")
    ax.set_xlabel("Voltage(V)")
    ax.set_ylabel("Current(nA)")
    ax.set_title("Gaurd Ring Current Estimation")
    box = ax.get_position()
    #ax.yscale("log")
    plt.yscale("log")
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(outfolder+ '_GR_EST.png')
    plt.close('all')
def plot_average_profile_IV(data, fi, threshold, isHD,wafer):
    outfolder = fi+"Average_IV_Profile/"
    checkAndMakeDir(outfolder)
    voltages = set(data[:,0])
    voltages = sorted(voltages)
    if isHD:
        small_pads = [1,2,3,4,5,6,7,8,9,10,12,13,26,42,57,73,91,109,128,148,
        171,193,217,241,265,288,310,330,349,367,385,402,418,432,
        433,435,436,437,438,439,
        440,441,442,443,444,431,417,401,384,366,448,329,309,287,264,240,
        216,192,170,147,127,108,90,72,46,41,25,29,30,36,37,87,88,150,151,158,157,
        207,208,267,268,261,262,297,298,381,382,411,412]
        gr=445
    else:
        small_pads = [1,2,3,4,5,6,7,8,18,28,39,51,65,80,95,111,126,
        140,155,168,179,189,197,196,195,194,193,192,191,190,180,169,
        156,141,127,112,96,81,66,52,40,29,19,9, 13,14,69,70,61,62,142,
        143,153,154,162,163]
        gr = 199
    pad_mask=np.zeros(len(data), dtype = bool)
    pad_mask[:] = [pad not in small_pads for pad in data[:,1]]
    large_pads =data[pad_mask]

    large_pads = large_pads[large_pads[:,1]<gr]#Remove Gaurdring and other pads
    averages = []
    upper = []
    lower = []
    if threshold>0:
        abscurrent = np.zeros((len(large_pads)))
        abscurrent[:]= [abs(ele) for ele in (large_pads[:,2])]

        threshold_mask = [(abscurrent[:]>threshold) ]# find the cells with current greater than 10000 when the voltage has reached 100
        badpads = large_pads[tuple(threshold_mask)]
        badcells = set(badpads[:,1])
        badcell_mask=np.zeros(len(large_pads), dtype = bool)
        badcell_mask[:]= [ele not in badcells for ele in large_pads[:,1]]
        large_pads=large_pads[badcell_mask]

    for v in voltages:
        mask = [large_pads[:,0]==v]
        vstep=large_pads[tuple(mask)]
        averages.append(np.average(vstep[:,2]))
        lower.append(np.average(vstep[:,2])-np.std(vstep[:,2]))
        upper.append(np.average(vstep[:,2])+np.std(vstep[:,2]))
    fig,ax = plt.subplots()
    # make a plot
    ax.fill_between(voltages, lower, upper, alpha=0.2)
    ax.plot(voltages, averages, "-")
    if threshold<-1:
        ax.set_title("Average IV Profile"+"[" +wafer+"]")
        ax.set_ylabel("Current (nA)")
        ax.set_xlabel("Voltage (V)")
        plt.savefig(outfolder+wafer+ '_Average_Profile_IV.png')
    else:
        ax.set_title("Average IVProfile [Highchannels removed]"+"[" +wafer+"]")
        ax.set_ylabel("Current (nA)")
        ax.set_xlabel("Voltage (V)")
        plt.savefig(outfolder+wafer+ '_Average_Profile_IV_Highchannels_Removed.png')
    plt.close('all')
def plot_average_profile_CV(data, fi, corr, isHD, wafer):
    outfolder = fi+"Average_CV_Profile/"
    checkAndMakeDir(outfolder)

    voltages = set(data[:,0])
    voltages = sorted(voltages)
    if isHD:
        small_pads = [1,2,3,4,5,6,7,8,9,10,12,13,26,42,57,73,91,109,128,148,
        171,193,217,241,265,288,310,3301,349,367,385,402,418,432,
        433,435,436,437,438,439,
        440,441,442,443,444,431,417,401,384,366,448,329,309,287,264,240,
        216,192,170,147,127,108,90,72,46,41,25,29,30,36,37,87,88,150,151,158,157,
        207,208,267,268,261,262,297,298,381,382,411,412]
        gr=445
    else:
        small_pads = [1,2,3,4,5,6,7,8,18,28,39,51,65,80,95,111,126,
        140,155,168,179,189,197,196,195,194,193,192,191,190,180,169,
        156,141,127,112,96,81,66,52,40,29,19,9, 13,14,69,70,61,62,142,
        143,153,154,162,163]
        gr = 199
    pad_mask=np.zeros(len(data), dtype = bool)
    pad_mask[:] = [pad not in small_pads for pad in data[:,1]]
    large_pads =data[pad_mask]
    large_pads = large_pads[large_pads[:,1]<199]#Remove Gaurdring and other pads
    pad_mask=np.zeros(len(corr), dtype = bool)
    pad_mask[:] = [pad in large_pads for pad in corr[:,1]]
    corr_largepad=corr[pad_mask]
    CV_avg =np.zeros((len(voltages),3), float)
    CV_corr = np.zeros((len(voltages),6), float)

    for v in range(0,len(voltages)):
        mask = [large_pads[:,0]==voltages[v]]
        vstep=large_pads[tuple(mask)]
        voltage=voltages[v]
        if (voltage%10)!=0:
            voltage =voltage -(voltage%10)
        if voltage>-220:
            mask = [corr_largepad[:,0]==voltage]
        else: mask = [corr_largepad[:,0]==-220]
        corr_vstep=corr_largepad[tuple(mask)]
        if len(corr_vstep)<1:
            #print ("CV Correction missing for V="+str(voltages[v])+"V. Terminating CV Correction\n")
            break
        CV_corr_vstep = np.zeros((len(vstep),2), float)
        for i in range(len(vstep[:,2])):


            CV_corr_vstep[i,0]=vstep[i, 2]-corr_vstep[i, 2]
            CV_corr_vstep[i,1]=CV_corr_vstep[i,0]**-2
        m= np.average(CV_corr_vstep[:,0])
        u = m + np.std(CV_corr_vstep[:,0])
        d = m - np.std(CV_corr_vstep[:,0])
        CV_corr[v,:3]=[m,u,d]
        m= np.average(CV_corr_vstep[:,1])
        u = m + np.std(CV_corr_vstep[:,1])
        d = m - np.std(CV_corr_vstep[:,1])
        CV_corr[v,3:6]=[m,u,d]
        m= np.average(vstep[:,2])
        u = m + np.std(vstep[:,2])
        d = m - np.std(vstep[:,2])
        CV_avg[v,:]=[m,u,d]
    

    fig,ax = plt.subplots()
    # make a plot
    ax.fill_between(voltages, CV_corr[:,2], CV_corr[:,1],  label=r'$\sigma$',alpha=0.2)
    ax.plot(voltages, CV_corr[:,0], "-",label = r'Average')
    ax.set_title("Average CV Profile[Corrected]"+"[" +wafer+"]")
    ax.set_ylabel("C (pF)")
    ax.set_xlabel("Voltage (V)")
    plt.savefig(outfolder+wafer+ '_Average_Profile_CV_CORRECTED.png')
    plt.close('all')
    fig,ax = plt.subplots()
    # make a plot
    ax.fill_between(voltages, CV_corr[:,5], CV_corr[:,4],  label=r'$\sigma$',alpha=0.2)
    ax.plot(voltages, CV_corr[:,3], "-",label = r'Average')
    ax.set_title("Average CV-2 Profile[Corrected]"+"[" +wafer+"]")
    ax.set_ylabel(r"$C^{-2} (pF^{-2})$")
    ax.set_xlabel("Voltage (V)")
    plt.savefig(outfolder+ wafer+'_Average_Profile_CV-2_CORRECTED.png')
    plt.close('all')
    ##
    ax.fill_between(voltages, CV_avg[:,2], CV_avg[:,1],  label=r'$\sigma$',alpha=0.2)
    ax.plot(voltages, CV_avg[:,0], "-",label = r'Average')
    ax.set_title("Average CV Profile")
    ax.set_ylabel("C (pF)")
    ax.set_xlabel("Voltage (V)")
    plt.savefig(outfolder+wafer+ '_Average_Profile_CV.png')
    plt.close('all')

def plot_CV_ByChannel(data, outfi, wafer):
    checkAndMakeDir(outfi+"CV_ByChannel/")
    voltages = set(data[:,0])
    voltages = sorted(voltages)
    fig = plt.figure()
    ax  = fig.add_subplot(111)
    colors = itertools.cycle(['r', 'b', 'g','m','c','y','k'])
    activepad_mask = [data[:,1]<199]
    activepad=data[tuple(activepad_mask)]
    for v,col in zip(voltages,colors):
        v_mask = [activepad[:,0]==v]
        v_data = activepad[tuple(v_mask)]
        color = next(colors)
        ax.plot(v_data[:,1], v_data[:,4], color, label = str(v)+'V')
    ax.set_title('Capacitance By Channel, Wafer No '+wafer)
    ax.set_ylabel('Cp (pf)')
    ax.set_xlabel('Channel')
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(outfi+"CV_ByChannel/"+wafer +'_CV_Channel_.png')
    
    plt.close('all')
