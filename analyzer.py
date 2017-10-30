#This file is part of ClusterRateWatch.
#Copyright 2017 William Putnam

#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at

#      http://www.apache.org/licenses/LICENSE-2.0

#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

import serial
import array
import sys

#get data sets from clustering algorithm
def getSets(str):
    global data1
    global data2
    global data3
    done = False
    tmp = ""
    if (str[2] == '3' and str[8] == 'D'):		#start with speed for now
        tmp = str[10:12]
        for i in range(0,50):					#populate data1 first...
            if (data1[i] == -1):
                data1[i] = int(tmp, 16);
                #print data1
                done = True
                break
        if (done == False):						#...then data2...
             for i in range(0,50):
                 if (data2[i] == -1):
                    data2[i] = int(tmp, 16);
                    #print data2
                    done = True
                    break
        if (done == False):						#...and finally data3...
             for i in range(0,50):
                 if (data3[i] == -1):
                    data3[i] = int(tmp, 16);
                    #print data3
                    done = True
                    if (i == 49):						#once we have full data sets, calc d avgs
                        dAvgCalcs()
                        data1 = data2;				#readjust data sets
                        data2 = data3;
                        data3 = array.array('i',(-1 for i in range(0,50)));
                    break
    return;
#----------------------------------------------------------------------------------------------------------------
#calculate the average derivatives
def dAvgCalcs():
    global data1
    global data2
    global data3
    
    d1 = array.array('i',(-1 for i in range(0,49)));
    d2 = array.array('i',(-1 for i in range(0,49)));
    d3 = array.array('i',(-1 for i in range(0,49)));
    d1avg = 0.00
    d2avg = 0.00
    d3avg = 0.00
    
    for i in range(0,49):
        d1[i] = data1[i+1] - data1[i]
        d2[i] = data2[i+1] - data2[i]
        d3[i] = data3[i+1] - data3[i]
    
    for i in range(0,49):
        d1avg += d1[i]
        d2avg += d2[i]
        d3avg += d3[i]
    
    d1avg /= 49
    d2avg /= 49
    d3avg /= 49
    
    print d1avg, d2avg, d3avg
    
    sys.stdout.flush()			#HTML will never update fast enough without this
    
    return;
#----------------------------------------------------------------------------------------------------------------
#declare variables and loop forever to read data
ser = serial.Serial('/dev/ttyS3', 115200)
strhead = ""
strdata = ""

data1 = array.array('i',(-1 for i in range(0,50)));
data2 = array.array('i',(-1 for i in range(0,50)));
data3 = array.array('i',(-1 for i in range(0,50)));

while True:		#loop out Rx/Tx chars first
    n = ser.read()
    #print n
    if (n == 'R' or n == 'T' or n == 'x'):
        pass
    #elif n.isspace() != False:
    #    strhead + n
    elif n == ':':		#now we get header...
        strhead = ser.read(9)
        strhead.strip()
        while True:	#...and data
            n = ser.read(3)
            if n.isspace() :	#reached the end of transmitted data
                #print "Header: " + strhead + "\nData: " + strdata
                #if len(strdata) > 14:
                    #print  "\nData: " + strdata,
                getSets(strdata)
                strhead = ""
                strdata = ""
                break
            else :
                strdata += n