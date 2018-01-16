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
N = 30
DAY = 30
Xn = [[0 for i in range(N)] for j in range(DAY)]
Yn = [0 for i in range(N)]


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
                if (otime + datetime.timedelta(days=j) <= time and time < otime + datetime.timedelta(days=j+1)):
                    Yn[j] += 1
                    continue
    timelist = []
    csvWriter = csv.writer(cof)
    timelist = [IDNAME,m]
    #timelist = listData + Yn
    print IDNAME
    csvWriter.writerow(timelist + Yn)
    print "合計コメント:%d" % m

if __name__ == "__main__":

    if  VIDEO == 0:
        NAME        = "inc"
        DATFILENAME = "husei_list.dat"
        COMENT_FILE = "huseilist_dir"
        cof = open(str(DAY) + '_husei_time.csv', 'ab')
    else:
        NAME        = "pop"
        DATFILENAME = "popular.dat"
        COMENT_FILE = "pop_comment"
        cof = open(str(DAY) + '_pop_time.csv', 'ab')
    
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
