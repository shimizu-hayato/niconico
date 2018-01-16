#! /usr/bin/env python
#-*- coding: utf-8 -*-

import sys, string
import re, pprint
import codecs
import glob
import csv
import json
import os
import commands

pattern = r"[sn]m\d{7,8}"
PASS = "/media/HD-PCTU2/niconicomment/tcserv.nii.ac.jp/access/c501106050@tokushima-u.ac.jp/13b81bce2f0c09a3/nicocomm/data/thread"

def bunrui():

    out_f = open('husei_list.dat','w')
    for line in open("husei_listname.dat",'r'):
        matchOB = re.match(pattern , line)
        print matchOB.group()
        for oline in open("husei_over1000.dat",'r'):
            jsonData = json.loads(oline)
            if(jsonData["video_id"] == matchOB.group()):
                out_f.write(oline)
                break


def bunrui_dat():
    for line in open('husei_list.dat','r'):
        videojsonData = json.loads(line)
        IDNAME = videojsonData["video_id"]
        if len(IDNAME) == 10:
            TARNAME = IDNAME[2:6]
        elif len(IDNAME) == 9:
            TARNAME = "0" + IDNAME[2:5]
        elif len(IDNAME) == 8:
            TARNAME = "00" + IDNAME[2:4]
        else:
            continue


        os.system("cp " + PASS + "/" + TARNAME + "/" + IDNAME +".dat huseilist_dir")





if __name__ == "__main__":
    bunrui_dat()
    #bunrui()
