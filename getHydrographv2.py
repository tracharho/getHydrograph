import matplotlib.pyplot as plt
import numpy as np
#from fpdf import FPDF



"""Defining an input function to get a logical input for floats"""
def getFloat(x):
    while True:
        try:
            y = float(input('Please enter a value for the ' + x + ' '))
            return y
        except ValueError:
            print('Sorry, try a logical value')

def getStr(x):
    while True:
        try:
            x = str(input(('Please input a number for '+x+' ')))
            return x
        except ValueError:
            print('Sorry, try a logical value')



"""Getting input values for the Curve Number and Drainage Area"""
DA_name = getStr('Draiange Area Name.')
rf_depth = getFloat('Rainfall Depth for the 24-hour storm.')
CN = getFloat('Curve Number.')
DA = getFloat('Drainage Area in acres.')
Tc = getFloat('Time of Concentration in minutes.')


"""Taking input values and calculating variables"""
DA_sqmi = DA/640       #converting drainage area to square miles
Tchr= Tc/60            #Taking the given time of concentration and converting it to hours
S = (1000/CN) - 10     #Variable for Retention
Ia = 0.2 * S           #Variable for Initial Abstraction
delD = Tc/7.5          #Used to determine Hydrograph Peak Time and to dimension the rainfall and unit discharge
Tp = 0.6667*Tchr            #Hydrograph incrimental time steps and used to interpolate the TypeIIaccRatio data
qp = 484*1*DA_sqmi/(Tp)     #Used to determine the peak discharge and to dimension the Unit Hydrgraph
SF = 1.00             #Safety Factor to be applied to the end hydrograph


TypeIIaccRatio = np.array([.0000,.0010,.0020,.0030,.0041,.0051,.0062,.0072,.0083,.0094,
.0105,.0116,.0127,.0138,.0150,.0161,.0173,.0184,.0196,.0208,
.0220,.0232,.0244,.0257,.0269,.0281,.0294,.0306,.0319,.0332,
.0345,.0358,.0371,.0384,.0398,.0411,.0425,.0439,.0452,.0466,
.0480,.0494,.0508,.0523,.0538,.0553,.0568,.0583,.0598,.0614,
.0630,.0646,.0662,.0679,.0696,.0712,.0730,.0747,.0764,.0782,
.0800,.0818,.0836,.0855,.0874,.0892,.0912,.0931,.0950,.0970,
.0990,.1010,.1030,.1051,.1072,.1093,.1114,.1135,.1156,.1178,
.1200,.1222,.1246,.1270,.1296,.1322,.1350,.1379,.1408,.1438,
.1470,.1502,.1534,.1566,.1598,.1630,.1663,.1697,.1733,.1771,
.1810,.1851,.1895,.1941,.1989,.2040,.2094,.2152,.2214,.2280,
.2350,.2427,.2513,.2609,.2715,.2830,.3068,.3544,.4308,.5679,
.6630,.6820,.6986,.7130,.7252,.7350,.7434,.7514,.7588,.7656,
.7720,.7780,.7836,.7890,.7942,.7990,.8036,.8080,.8122,.8162,
.8200,.8237,.8273,.8308,.8342,.8376,.8409,.8442,.8474,.8505,
.8535,.8565,.8594,.8622,.8649,.8676,.8702,.8728,.8753,.8777,
.8800,.8823,.8845,.8868,.8890,.8912,.8934,.8955,.8976,.8997,
.9018,.9038,.9058,.9078,.9097,.9117,.9136,.9155,.9173,.9192,
.9210,.9228,.9245,.9263,.9280,.9297,.9313,.9330,.9346,.9362,
.9377,.9393,.9408,.9423,.9438,.9452,.9466,.9480,.9493,.9507,
.9520,.9533,.9546,.9559,.9572,.9584,.9597,.9610,.9622,.9635,
.9647,.9660,.9672,.9685,.9697,.9709,.9722,.9734,.9746,.9758,
.9770,.9782,.9794,.9806,.9818,.9829,.9841,.9853,.9864,.9876,
.9887,.9899,.9910,.9922,.9933,.9944,.9956,.9967,.9978,.9989, 1.000])

"""Initializing the TypeIIaccRatio Mass Curve Abscissa, noted as TypeIIaccDepth"""
TypeIIaccDepth = np.array([0,6,12,18,24,30,36,42,48,54,60,66,72,78,84,90,96,102,
                 108,114,120,126,132,138,144,150,156,162,168,174,180,
                 186,192,198,204,210,216,222,228,234,240,246,252,258,
                 264,270,276,282,288,294,300,306,312,318,324,330,336,
                 342,348,354,360,366,372,378,384,390,396,402,408,414,
                 420,426,432,438,444,450,456,462,468,474,480,486,492,
                 498,504,510,516,522,528,534,540,546,552,558,564,570,
                 576,582,588,594,600,606,612,618,624,630,636,642,648,
                 654,660,666,672,678,684,690,696,702,708,714,720,726,
                 732,738,744,750,756,762,768,774,780,786,792,798,804,
                 810,816,822,828,834,840,846,852,858,864,870,876,882,
                 888,894,900,906,912,918,924,930,936,942,948,954,960,
                 966,972,978,984,990,996,1002,1008,1014,1020,1026,1032,
                 1038,1044,1050,1056,1062,1068,1074,1080,1086,1092,1098,
                 1104,1110,1116,1122,1128,1134,1140,1146,1152,1158,1164,
                 1170,1176,1182,1188,1194,1200,1206,1212,1218,1224,1230,
                 1236,1242,1248,1254,1260,1266,1272,1278,1284,1290,1296,
                 1302,1308,1314,1320,1326,1332,1338,1344,1350,1356,1362,
                 1368,1374,1380,1386,1392,1398,1404,1410,1416,1422,1428,
                 1434,1440])

"""Making the interpolated TypeIIaccRatio ordinates"""
rfmca = np.array([i* delD for i in range(int(1440/delD))])   #rfmca = Rainfall Mass Curve Abscissa, in delD intervals for 1440 minutes
rfmca = np.append(rfmca, 1440)                               #adding the last value of 1440 (24hours) to the abscissa
rfmco = rf_depth * TypeIIaccRatio                            #this dimension the storm ordinates by the rainfall depth


"""Making the runoff curve, Q = ((P(t) - 0.2*S)^2)/(P(t) + 0.8*S)"""
runoff_acc = np.array([])
for i in range(len(rfmco)):   #If the initial abstraction is higher than the rainfall depth, then the runoff at that point in the storm is 0. Else use the runoff equation to determine accumulated runoff at a point
    if rfmco[i] <= Ia:
        runoff_acc = np.append(runoff_acc, 0)
    else:
        runoff_acc = np.append(runoff_acc, ((rfmco[i] - 0.2*S)**2)/(rfmco[i] + 0.8*S))
runoff_acc_interp = np.interp(rfmca, TypeIIaccDepth, runoff_acc)  #This interpolates the storm into delD incriments.


"""Making the incrimental runoff curve, or the runoff hyetograph"""
runoff_hyetograph = np.array([0])          #initializing the hyetograph
for i in range(len(runoff_acc_interp)-1):   #to make the hyetograph, you take the incriments/difference of the each accumulated point
    runoff_hyetograph = np.append(runoff_hyetograph, runoff_acc_interp[i+1] - runoff_acc_interp[i])


"""Setting up the Unit Hydrograph Abscissa"""
UH_originaltime = Tp * np.array([0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1,  #his is the original UH abscissa.
                                 1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,
                                 1.9,2,2.2,2.4,2.6,2.8,3,3.2,3.4,
                                 3.6,3.8,4,4.5,5])
UH_t = np.array([i * (delD/60) for i in range(int(Tp*5/(delD/60)))])  #Breaking the dimensioned hydrograph abscissa into delD hour incriments

"""Initializing the Unit Hydrograph Ordinates and dimensioning it by qp"""
UH_discharge = qp * np.array([0.0000,0.0300,0.1000,0.1900,0.3100,0.4700,0.6600,0.8200,0.9300,0.9900,1.0000,0.9900,
                      0.9300,0.8600,0.7800,0.6800,0.5600,0.4600,0.3900,0.3300,0.2800,0.207,0.147,0.107,0.077,0.055,0.040,
                              0.029,0.021,0.015,0.011,0.005,0])
UH_q = np.interp(UH_t, UH_originaltime, UH_discharge)
"""WHY THE F DO YOU HAVE TO FLIP THIS?"""
UH_q = np.flip(UH_q)

"""Making the Runoff Hydrograph by convoluting the Unit Hydrograph and the Hyetograph"""
runoff_hydrograph = SF * np.convolve(UH_q, runoff_hyetograph) #God bless numpy, convoluting the dimensioned unit hydrograph by the runoff_hyetograph
hydrograph_abscissa = [i * (1440/len(runoff_hydrograph)) for i in range(len(runoff_hydrograph))] #Setting the Abscissa to the hydrograph
volume = 60*np.trapz(runoff_hydrograph, dx=delD)


"""Plotting the results"""
plt.plot(hydrograph_abscissa, runoff_hydrograph)
plt.plot(hydrograph_abscissa, runoff_hydrograph, 'ro')
plt.xlabel('Time in Minutes')
plt.ylabel('Discharge in CFS')
plt.title('Runoff Hydrograph for {}'.format(DA_name))
plt.axis([0, 1440, 0, 1.15*np.amax(runoff_hydrograph)])
plt.text(30, 0.4*np.amax(runoff_hydrograph), 'Area = {e} ac.\nCN = {f}\nTc = {g} min\nStorm Depth = {d}"\nPeak Discharge = {a:.3f} ft$^3/s$\nTime to peak = {b:.2f} min\nRunoff Volume = {c:.3f} ft$^3$\nShape Factor = 484'.format
         (a=np.amax(runoff_hydrograph), b=hydrograph_abscissa[np.argmax(runoff_hydrograph)], c=volume, d=rf_depth, e = DA, f=CN, g = Tc)
         , fontsize=10, bbox={'alpha' : .15,'pad': 2})


#plt.grid(True)
#plt.savefig('C:/Users/TRhodes/Desktop/Python/PDFs/{}_{}inch-24hourstorm.pdf'.format(DA_name, rf_depth))#', dpi = 220)
plt.show()
