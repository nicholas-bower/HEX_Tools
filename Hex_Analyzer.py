
import numpy as np
import itertools
import matplotlib.pyplot as plt
import os
import glob

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
    mask = [data[:,2]!=0]
    f.close()
    return data[mask]
def plot_IV_By_Channel(data, name, mask_abov, corr, CV):
    voltages = set(data[:,0])
    voltages = sorted(voltages)
    fig = plt.figure()
    ax  = fig.add_subplot(111)
    colors = itertools.cycle(['r', 'b', 'g','m','c','y','k'])
    activepad_mask = [data[:,1]<199]
    data=data[activepad_mask]
    for v,col in zip(voltages,colors):
        v_mask = [data[:,0]==v]
        v_data = data[v_mask]
        color = next(colors)
        ax.plot(v_data[:,1], v_data[:,2], color, label = str(v)+'V')
    ax.set_title('IV by Channel')
    ax.set_ylabel('Current (nA)')
    ax.set_xlabel('Channel')
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(name+ '_byChannel.png')
    plt.close('all')
    fig2=plt.figure()
    ax2 = fig2.add_subplot(111)
    abscurrent = np.zeros((len(data)))
    abscurrent[:]= [abs(ele) for ele in (data[:,2])]

    badpad_mask = [(abscurrent[:]>mask_abov) ]# find the cells with current greater than 10000 when the voltage has reached 100
    badpads = data[badpad_mask]
    plot_Channels(badpads[:,1], corr, data, CV, name)
    badcells = set(badpads[:,1])
    test=np.zeros(len(data), dtype = bool)
    test[:]= [ele not in badcells for ele in data[:,1]]
    good_data=data[test]
    for v,col in zip(voltages,colors):
        v_mask = [good_data[:,0]==v]
        v_data = good_data[v_mask]
        color = next(colors)
        ax2.plot(v_data[:,1], v_data[:,2], color, label = str(v)+'V')
    ax2.set_title('IV by Channel[With \'Bad\' Channls removed]')
    ax2.set_ylabel('Current (nA)')
    ax2.set_xlabel('Channel')


    box = ax2.get_position()
    ax2.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))


    plt.savefig(name+'_sortedByChannel.png')
    plt.close('all')
def plot_totalCurrent(data, name):
    voltages = set(data[:,0])
    voltages = sorted(voltages)
    fig = plt.figure()
    ax  = fig.add_subplot(111)
    colors = itertools.cycle(['r', 'b', 'g','m','c','y','k'])
    activepad_mask = [data[:,1]<199]
    activepad=data[activepad_mask]
    for v,col in zip(voltages,colors):
        v_mask = [activepad[:,0]==v]
        v_data = activepad[v_mask]
        color = next(colors)
        ax.plot(v_data[:,1], v_data[:,4], color, label = str(v)+'V')
    ax.set_title('Total Current')
    ax.set_ylabel('Current (nA)')
    ax.set_xlabel('Channel')
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(name+ '_TotalCurrent.png')
    
    plt.close('all')
def plot_singleChannel(data, channel, name, t):
    mask = [data[:,1]==channel]
    data=data[mask]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(data[:,0], data[:,2])
    invCV= []
    if (t =='IV'):
        ax.set_title('IV Channel: '+ str(channel))
        ax.set_xlabel('Voltage (V)')
        ax.set_ylabel('I(na)')
        plt.savefig(name+ '_Channel_' + str(channel)+t+'.png')
        plt.close('all')
    elif t=='CV':
        ax.set_title('CV Channel: '+ str(channel))
        ax.set_xlabel('Voltage (V)')
        ax.set_ylabel('C(pF)')
        plt.savefig(name+ '_Channel_' + str(channel)+t+'.png')
        plt.close('all')

        for x in data[:,2]:
            invCV.append(1/x**2)
        fig2 = plt.figure()
        ax2 = fig2.add_subplot(111)
        ax2.plot(data[:,0], invCV[:])
        ax2.set_title('InvSq CV, Channel: '+ str(channel))
        ax2.set_xlabel('Voltage (V)')
        ax2.set_ylabel('1/C^2(pF)')
        plt.savefig(name+ '_Channel_INVCV' + str(channel)+t+'.png')
        plt.close('all')


    
def plot_CV_Corr(data, corr, channel, name):
    mask= [data[:,1]==channel]
    data=data[mask]

    mask = [corr[:,1]==channel]
    corr = corr[mask]
    invCVSq=[]
    CVcorr = []

    for i in range(len(data[:,0])):
        if data[i,0]>-300:
            iCor=corr[corr[:,0]==data[i,0]]
        else: iCor=corr[corr[:,0]==-300]
        iData=(data[i,2])-((iCor[0,2]))
        CVcorr.append(iData)
        invCVSq.append(1/(iData**2))
        if data[i,0]==-400:
            print ("Cell " +str(channel)+" Cpf = " + str(iData))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(data[:,0], CVcorr[:])
    ax.set_title('CV Channel: '+ str(channel))
    ax.set_xlabel('Voltage (V)')
    ax.set_ylabel('C(pF)')
    plt.savefig(name+ '_Channel_' + str(channel)+'_Corrected.png')
    plt.close('all')
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)

    ax2.plot(data[:,0], invCVSq[:])
    ax2.set_title('CORRECTED invSq CV Channel: '+ str(channel))
    ax2.set_xlabel('Voltage (V)')
    ax2.set_ylabel('1/C^2(pF)')
    plt.savefig(name+ '_Channel_INVCVSq_' + str(channel)+'_Corrected.png')
    plt.close('all')

def plot_Channels(channels, corr,IV_data, CV_data, fi):
    for c in channels:
        plot_singleChannel(IV_data, c, fi, 'IV')
        plot_singleChannel(CV_data, c, fi, 'CV')
        #plot_CV_Corr(CV_data, corr, c, fi)

def plot_Humidity(data, fi):
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
    ax2.set_title("Envirmoental data")
    ax2.set_ylim(45,53)

    # save the plot as a file
    fig.savefig(fi+'_Enviromental.png',
            format='png',
            dpi=100,
            bbox_inches='tight')

def calc_GRIV(data, fi):
    voltages = set(data[:,0])
    voltages = sorted(voltages)
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
    print (str(I_Total[:]))
    print (str(I_Sum[:]))
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
    plt.savefig(fi+ '_GR_EST.png')
    plt.close('all')
def plot_average_profile_IV(data, fi, threshold):
    voltages = set(data[:,0])
    voltages = sorted(voltages)
    small_pads = [1,2,3,4,5,6,7,8,18,28,39,51,65,80,95,111,126,
    140,155,168,179,189,197,196,195,194,193,192,191,190,180,169,
    156,141,127,112,96,81,66,52,40,29,19,9, 13,14,69,70,61,62,142,
    143,153,154,162,163]
    pad_mask=np.zeros(len(data), dtype = bool)
    pad_mask[:] = [pad not in small_pads for pad in data[:,1]]
    large_pads =data[pad_mask]
    large_pads = large_pads[large_pads[:,1]<199]#Remove Gaurdring and other pads
    averages = []
    upper = []
    lower = []
    if threshold>0:
        abscurrent = np.zeros((len(large_pads)))
        abscurrent[:]= [abs(ele) for ele in (large_pads[:,2])]

        threshold_mask = [(abscurrent[:]>threshold) ]# find the cells with current greater than 10000 when the voltage has reached 100
        badpads = large_pads[threshold_mask]
        badcells = set(badpads[:,1])
        badcell_mask=np.zeros(len(large_pads), dtype = bool)
        badcell_mask[:]= [ele not in badcells for ele in large_pads[:,1]]
        large_pads=large_pads[badcell_mask]

    for v in voltages:
        mask = [large_pads[:,0]==v]
        vstep=large_pads[mask]
        averages.append(np.average(vstep[:,2]))
        lower.append(np.average(vstep[:,2])-np.std(vstep[:,2]))
        upper.append(np.average(vstep[:,2])+np.std(vstep[:,2]))
    fig,ax = plt.subplots()
    # make a plot
    ax.fill_between(voltages, lower, upper, alpha=0.2)
    ax.plot(voltages, averages, "-")
    if threshold<-1:
        ax.set_title("Average IV Profile")
        ax.set_ylabel("Current (nA)")
        ax.set_xlabel("Voltage (V)")
        plt.savefig(fi+ '_Average_Profile_IV.png')
    else:
        ax.set_title("Average IVProfile [Highchannels removed]")
        ax.set_ylabel("Current (nA)")
        ax.set_xlabel("Voltage (V)")
        plt.savefig(fi+ '_Average_Profile_IV_Highchannels_Removed.png')
    plt.close('all')
def plot_average_profile_CV(data, fi):

    voltages = set(data[:,0])
    voltages = sorted(voltages)
    small_pads = [1,2,3,4,5,6,7,8,18,28,39,51,65,80,95,111,126,
    140,155,168,179,189,197,196,195,194,193,192,191,190,180,169,
    156,141,127,112,96,81,66,52,40,29,19,9, 13,14,69,70,61,62,142,
    143,153,154,162,163]
    pad_mask=np.zeros(len(data), dtype = bool)
    pad_mask[:] = [pad not in small_pads for pad in data[:,1]]
    large_pads =data[pad_mask]
    large_pads = large_pads[large_pads[:,1]<199]#Remove Gaurdring and other pads
    averages = []
    upper = []
    lower = []
    for v in voltages:
        mask = [large_pads[:,0]==v]
        vstep=large_pads[mask]
        averages.append(np.average(vstep[:,2]))
        lower.append(np.average(vstep[:,2])-np.std(vstep[:,2]))
        upper.append(np.average(vstep[:,2])+np.std(vstep[:,2]))

    fig,ax = plt.subplots()
    # make a plot
    ax.fill_between(voltages, lower, upper, alpha=0.2)
    ax.plot(voltages, averages, "-")
    ax.set_title("Average CV Profile")
    ax.set_ylabel("C (pF)")
    ax.set_xlabel("Voltage (V)")
    plt.savefig(fi+ '_Average_Profile_CV.png')
    plt.close('all')


