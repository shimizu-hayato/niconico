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
#Yn = [0 for i in range(N)]
#len_comment_list = []


def comment_viewer(IDNAME,otime):
    len_comment_list = []
    Yn = []
    Yn = [0 for i in range(N)]
    for line in open(COMENT_FILE + '/' + IDNAME + '.dat','r'):
        jsonData = json.loads(line)
        time = datetime.datetime.fromtimestamp(jsonData["date"])

        if (time >= otime + datetime.timedelta(days=DAY)):
            continue
        else:
            if jsonData["comment"] == None:
                continue
            len_comment = len(jsonData["comment"])
            len_comment_list.append(len(jsonData["comment"]))
            if (len_comment <= 5):
                Yn[0] += 1
            elif(15 < len_comment and len_comment <= 10):
                Yn[1] += 1
            elif(30 < len_comment and len_comment <= 15):
                Yn[2] += 1
            else:
                continue
    
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
        cof = open(str(DAY) + '_husei_len15.csv', 'ab')
    else:
        NAME        = "pop"
        DATFILENAME = "popular.dat"
        COMENT_FILE = "pop_comment"
        cof = open(str(DAY) + '_pop_len.csv15', 'ab')
    
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

