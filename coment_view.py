#! /usr/bin/env python
#-*- coding: utf-8 -*-

import sys, string
import re, pprint
import codecs
import glob
import json
import datetime
from dateutil.relativedelta import *
import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as dates
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

X = []
Y = []
#nm16791686
#sm29952
#sm16753732
IDNAME = "sm1916875"
video_file = 1 #0:husei 

def comment_viewer(file_flag):

    if  file_flag  == 0:
        NAME        = "inc"
        DATFILENAME = "husei_over1000.dat"
        COMENT_FILE = "husei_dir"
    else:
        NAME        = "pop"
        DATFILENAME = "popular.dat"
        COMENT_FILE = "pop_comment"

    for line in open(DATFILENAME,'r'):
        videojsonData = json.loads(line)
        if(videojsonData["video_id"] == IDNAME):
            length = videojsonData["length"]
            upload = videojsonData["upload_time"]
            otime = datetime.datetime.strptime(upload[:13], '%Y-%m-%dT%H')
            break

    for line in open(COMENT_FILE + '/' + IDNAME + '.dat','r'):
        jsonData = json.loads(line)
        time = datetime.datetime.fromtimestamp(jsonData["date"])
        if (time >= otime + datetime.timedelta(days=7)):
            continue
        else:
            X.append(jsonData["vpos"])
            Y.append(time)

    ax=plt.subplot(111)
    ax.set_xlabel("vpos(1/100[s])")
    ax.set_ylabel("date")
    ax.set_xlim(0,length * 100)
    ax.yaxis.set_major_formatter(dates.DateFormatter('%m/%d\n%H:00')) #%m/%d-%h
    ax.plot(X,Y,'o',markersize=10)
    plt.savefig(IDNAME + "_1week_" + NAME +"_graf.png")

if __name__ == "__main__":

    
    comment_viewer(video_file)
