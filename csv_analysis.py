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
#SMNAME = "sm17045764"
VIDEO = 1 #0:husei
N = 5
DAY = 7
Xn = [[0 for i in range(N)] for j in range(DAY)]



def comment_viewer(IDNAME,lengthreg,otime):

    m = 0
    for line in open(COMENT_FILE + '/' + IDNAME + '.dat','r'):
        jsonData = json.loads(line)
        time = datetime.datetime.fromtimestamp(jsonData["date"])

        if (time >= otime + datetime.timedelta(days=DAY)):
            continue
        else:
            #print (time-otime).days
            vpos = jsonData["vpos"]
            m += 1
            for j in range(N):
                if(j == 0):
                    if(vpos < lengthreg):
                        Xn[(time-otime).days][0] += 1
                elif(0 < j and j < N-1):
                    if(lengthreg * j <= vpos and vpos < lengthreg * (j + 1)):
                        Xn[(time-otime).days][j] += 1
                elif(j == N-1):
                    if(lengthreg*j < vpos):
                        Xn[(time-otime).days][j] += 1
    """
    print np.corrcoef(Xn[0], Xn[1])[0,1] #相関係数を求める
    print np.corrcoef(Xn[1], Xn[2])[0,1]
    print np.corrcoef(Xn[2], Xn[3])[0,1]
    print np.corrcoef(Xn[3], Xn[4])[0,1]
    print np.corrcoef(Xn[4], Xn[5])[0,1]
    print np.corrcoef(Xn[5], Xn[6])[0,1]
    """
    
    if(m > 100):
        csvWriter = csv.writer(cof)
        listData = [IDNAME, m, lengthreg * N]
        for num in range(DAY-1):
            listData.append(np.corrcoef(Xn[num], Xn[num+1])[0,1])
        print IDNAME
        csvWriter.writerow(listData)
        print "合計コメント:%d" % m

if __name__ == "__main__":

    if  VIDEO == 0:
        NAME        = "inc"
        DATFILENAME = "husei_list.dat"
        COMENT_FILE = "huseilist_dir"
        cof = open(str(DAY) + '_' +str(N) + '_husei_corr_coef.csv', 'ab')
    else:
        NAME        = "pop"
        DATFILENAME = "popular.dat"
        COMENT_FILE = "pop_comment"
        cof = open(str(DAY) + '_' + str(N) + '_pop_corr_coef.csv', 'ab')
    
    Tlength = 0
    for line in open(DATFILENAME,'r'):
        videojsonData = json.loads(line)
        SMNAME = videojsonData["video_id"]
        if (len(SMNAME) < 8 or SMNAME[:1] == 'n'):
            continue
        length = videojsonData["length"]
        upload = videojsonData["upload_time"]
        upload_time = datetime.datetime.strptime(upload[:13], '%Y-%m-%dT%H')
        delta_length = length * 100 / N
        comment_viewer(SMNAME,delta_length,upload_time)
    cof.close()
