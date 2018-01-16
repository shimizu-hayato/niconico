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

video_info = []
X = []
Y = []
out_f = open('day_playnum.dat','w')


for dat_file in glob.glob('video/*.dat'):
    print dat_file,'-'*20

    for line in open(dat_file,'r'):
        jsonData = json.loads(line)
        
        upload = jsonData["upload_time"]
        time = datetime.datetime.strptime(upload[:10], '%Y-%m-%d')
        #day = time - otime
        #tag = jsonData["tags"]
        X.append(time)
        Y.append(jsonData["view_counter"])
        #if投稿が増えている場所
        #投稿日時
        #しきい値を決める
        '''
        for tag_dic in tag:
            if('category' in tag_dic):
                cate = tag_dic["tag"]
            else:
                cate = 'None'
        '''
        #out_f.write(str(day.days) + '\t' + str(jsonData["view_counter"]) + '\n')



ax=plt.subplot(111)
ax.set_xlabel("upload time")
ax.set_ylabel("view_counter")
ax.xaxis.set_major_locator(dates.AutoDateLocator())
ax.xaxis.set_major_formatter(dates.DateFormatter('%Y\n%b%d'))
ax.plot(X,Y,'o')
plt.savefig("graph2.png")
#ax.plt.show()
