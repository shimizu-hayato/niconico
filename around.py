#! /usr/bin/env python
#-*- coding: utf-8 -*-

import sys, string
import re, pprint
import codecs
import glob
import json


def comment_over():
    out_f = open('over10000.dat','w')

    for dat_file in glob.glob('video/*.dat'):
        
        for line in open(dat_file,'r'):
            jsonData = json.loads(line)
            if 1000< jsonData["comment_counter"] and jsonData["comment_counter"] < 10000:
                
                out_f.write(line)

def comment_overlist20000():
    
    out_f = open('husei_over20000.dat','w')
    for line in open("husei_over1000.dat",'r'):
        jsonData = json.loads(line)
        if 10000 < jsonData["comment_counter"]:
            out_f.write(line)

def mylist_overlist():
    out_f = open('mylist_over.dat','w')
    count = 0
    for dat_file in glob.glob('video/*.dat'):
        
        for line in open(dat_file,'r'):
            jsonData = json.loads(line)
            if (jsonData["view_counter"] < jsonData["mylist_counter"]):
                
                out_f.write(line)
                count += 1
    print count #1694

def comment_overlist():
    out_f = open('huseiname_over10000.dat','w')
        
    for line in open("husei_over10000.dat",'r'):
        jsonData = json.loads(line)
        out_f.write(jsonData["video_id"] + '\t' + jsonData["title"] + '\t' + str(jsonData["mylist_counter"]) + '\n')

if __name__ == "__main__":
    comment_over()
    #print "Hello"
