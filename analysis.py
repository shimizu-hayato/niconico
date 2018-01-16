#! /usr/bin/env python
#-*- coding: utf-8 -*-

import sys, string
import re, pprint
import codecs
import glob
import csv
import json
import numpy as np
import datetime
from dateutil.relativedelta import *
import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as dates
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

#h:sm16949803sm10194693sm10282214sm10920117sm11340017
#IDNAME = "sm16949803"
IDNAME = "sm17045764"
video_file = 1 #0:husei
Xn = [[0 for i in range(10)] for j in range(7)]

def comment_viewer(file_flag):

    if  file_flag  == 0:
        NAME        = "inc"
        DATFILENAME = "husei_over1000.dat"
        COMENT_FILE = "husei_comment"
        #cof = open('corr_coef.csv', 'ab')
    else:
        NAME        = "pop"
        DATFILENAME = "popular.dat"
        COMENT_FILE = "pop_comment"
        #cof = open('pop_corr_coef.csv', 'ab')
    
        
    for line in open(DATFILENAME,'r'):
        videojsonData = json.loads(line)
        if(videojsonData["video_id"] == IDNAME):
            length = videojsonData["length"]
            upload = videojsonData["upload_time"]
            otime = datetime.datetime.strptime(upload[:13], '%Y-%m-%dT%H')
            break
    
    lengthreg = length * 10
    m = 0
    for line in open(COMENT_FILE + '/' + IDNAME + '.dat','r'):
        jsonData = json.loads(line)
        time = datetime.datetime.fromtimestamp(jsonData["date"])
        vpos = jsonData["vpos"]

        if (time >= otime + datetime.timedelta(days=7)):
            continue
        else:
            #print (time-otime).days
            m += 1
            if(vpos < lengthreg):
                Xn[(time-otime).days][0] += 1
                
            elif(lengthreg <= vpos and vpos < lengthreg*2):
                Xn[(time-otime).days][1] += 1
                
            elif(lengthreg*2 <= vpos and vpos < lengthreg*3):
                Xn[(time-otime).days][2] += 1
                
            elif(lengthreg*3 <= vpos and vpos < lengthreg*4):
                Xn[(time-otime).days][3] += 1
                
            elif(lengthreg*4 <= vpos and vpos < lengthreg*5):
                Xn[(time-otime).days][4] += 1
                
            elif(lengthreg*5 <= vpos and vpos < lengthreg*6):
                Xn[(time-otime).days][5] += 1

            elif(lengthreg*6 <= vpos and vpos < lengthreg*7):
                Xn[(time-otime).days][6] += 1

            elif(lengthreg*7 <= vpos and vpos < lengthreg*8):
                Xn[(time-otime).days][7] += 1

            elif(lengthreg*8 <= vpos and vpos < lengthreg*9):
                Xn[(time-otime).days][8] += 1

            elif(lengthreg*9 <= vpos):
                Xn[(time-otime).days][9] += 1

    """           
    x = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])



    plt.plot(Xn[0], Xn[1],'.')
    plt.savefig(IDNAME + "dat.png")
    plt.show()
    """
    print np.corrcoef(Xn[0], Xn[1])[0,1] #相関係数を求める
    print np.corrcoef(Xn[1], Xn[2])[0,1]
    print np.corrcoef(Xn[2], Xn[3])[0,1]
    print np.corrcoef(Xn[3], Xn[4])[0,1]
    print np.corrcoef(Xn[4], Xn[5])[0,1]
    print np.corrcoef(Xn[5], Xn[6])[0,1]
    """
    csvWriter = csv.writer(cof)
    listData = [IDNAME]
    for num in range(5):
        listData.append(np.corrcoef(Xn[num], Xn[num+1])[0,1])
    
    csvWriter.writerow(listData)
    cof.close()
    """
    print "合計コメント:%d" % m
if __name__ == "__main__":

    
    comment_viewer(video_file)
