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

VIDEO = 0 #0:husei
N = 5
DAY = 30
#Xn = [[0 for i in range(N)] for j in range(DAY)]
Yn = [0 for i in range(N)]
#len_comment_list = []


def comment_viewer(IDNAME,otime):

    len_comment_list = []
    for line in open(COMENT_FILE + '/sm11835544.dat','r'):
        jsonData = json.loads(line)
        time = datetime.datetime.fromtimestamp(jsonData["date"])

        if (time >= otime + datetime.timedelta(days=DAY)):
            continue
        else:
            if(not len(jsonData["comment"])):
                continue
            len_comment = len(jsonData["comment"])
            len_comment_list.append(len(jsonData["comment"]))
            if (len_comment <= 15):
                Yn[0] += 1
            elif(15 < len_comment and len_comment <= 30):
                Yn[1] += 1
            elif(30 < len_comment and len_comment <= 45):
                Yn[2] += 1
            elif(45 < len_comment and len_comment <= 60):
                Yn[3] += 1
            else:
                Yn[4] += 1
    
    data = np.array(len_comment_list)
    csvWriter = csv.writer(cof)
    csvlist = [IDNAME] + Yn + ["",np.mean(data),np.median(data)]
    print IDNAME
    csvWriter.writerow(csvlist)

if __name__ == "__main__":

    if  VIDEO == 0:
        NAME        = "inc"
        DATFILENAME = "husei_list.dat"
        COMENT_FILE = "huseilist_dir"
        cof = open(str(DAY) + '_husei_len.csv', 'ab')
    else:
        NAME        = "pop"
        DATFILENAME = "popular.dat"
        COMENT_FILE = "pop_comment"
        cof = open(str(DAY) + '_pop_len.csv', 'ab')
    
    Tlength = 0
    for line in open(DATFILENAME,'r'):
        videojsonData = json.loads(line)
        SMNAME = videojsonData["video_id"]
        if (len(SMNAME) < 8 or SMNAME[:1] == 'n'):
            continue
        upload = videojsonData["upload_time"]
        upload_time = datetime.datetime.strptime(upload[:13], '%Y-%m-%dT%H')
        comment_viewer(SMNAME,upload_time)
    cof.close()

