#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys, string
import re, pprint
import codecs
import glob
import csv
import json
import collections
import datetime
from collections import OrderedDict
import numpy


#日付取得
today = datetime.datetime.today()
datename = today.strftime("%Y%m%d")

category_tag_list = []
lock_tag_list = []
free_tag_list = []
sum_tag_dict = {}
com_tag_dict = {}
my_tag_dict = {}
so_data = [0,0,0]
#動画数129 再生数35032915, コメント数3, マイリスト数248216
so_num = 0


fh = open(r'monthly_rank_movie/' + datename + '_rank_movie.json','r',encoding="utf-8_sig")
rank_data = json.loads(fh.read())
for data in rank_data:
    #print(x['link'].encode('cp932', "ignore").decode('cp932'))
    if "so" in data["video_id"]:
        so_num = so_num + 1
        if int(data["comment_num"]) > 0:
            print(data["video_id"])

        so_data[0] += int(data["view_counter"])
        so_data[1] += int(data["comment_num"])
        so_data[2] += int(data["mylist_counter"])
        continue
    tags = data['tags']
    for tag in tags:
        """
        try:
            print(tag[0])
        except Exception as e:
            tag[0] = tag[0].encode('cp932', 'ignore').decode('cp932')
            print(e)
        """

        tag[0] = tag[0].encode('cp932', 'ignore').decode('cp932')
        if tag[1] == 2:
            category_tag_list.append(tag[0])
        elif tag[1] == 1:
            lock_tag_list.append(tag[0])
        elif tag[1] == 0:
            free_tag_list.append(tag[0])
        #print(tag[0])
        if tag[0] not in sum_tag_dict.keys():
            sum_tag_dict[tag[0]] = []
        if tag[0] not in com_tag_dict.keys():
            com_tag_dict[tag[0]] = []
        if tag[0] not in my_tag_dict.keys():
            my_tag_dict[tag[0]] = []


        sum_tmp = sum_tag_dict[tag[0]]
        com_tmp = com_tag_dict[tag[0]]
        my_tmp = my_tag_dict[tag[0]]

        sum_tmp.append(int(data["view_counter"]))
        
        sum_tag_dict[tag[0]] = sum_tmp
        com_tag_dict[tag[0]] += [int(data["comment_num"])]
        my_tag_dict[tag[0]]  += [int(data["mylist_counter"])]

print(sum_tag_dict)
exit()

        

category_dict = dict(collections.Counter(category_tag_list))
lock_dict = dict(collections.Counter(lock_tag_list))
free_dict = dict(collections.Counter(free_tag_list))
print(len(free_dict))
#print(sum_tag_dict)

"""
print("category:")
print(category_dict)
print("lock:")
#print(tag_dict)

for k,v in tag_dict.items():
    print(k)
    if v < 3:
        del tag_dict[k]
"""

def file_save(filename,dictfile):

    with codecs.open(filename,'w',encoding = "utf-16") as f:
        writer = csv.writer(f, lineterminator='\n')
        sum_num = 0
        sum_rag_list = [[0,0,0,0],
                        [0,0,0,0],
                        [0,0,0,0],
                        [0,0,0,0],
                        [0,0,0,0]]
        sum_num_list =["「合計」",0,0,0,0]
        for k,v in sorted(dictfile.items(),key=lambda x:x[1],reverse=True):
            csv_list = []
            sum_num += v
            csv_list += [k,v]
            if filename == "category_result.csv":
                csv_list += [sum_tag_dict[k],com_tag_dict[k],my_tag_dict[k],""]
                csv_list += [round(sum_tag_dict[k]/v)
                        ,round(com_tag_dict[k]/v)
                        ,round(my_tag_dict[k]/v)]

                writer.writerow(csv_list)
                
                #print(sum_tag_dict[k])

            else:
            
                if v > 10:
                    sum_rag_list[0][0] += v
                    sum_rag_list[0][1] += sum_tag_dict[k]
                    sum_rag_list[0][2] += com_tag_dict[k]
                    sum_rag_list[0][3] += my_tag_dict[k]
                    
                elif 10 >= v and v > 7:
                    sum_rag_list[1][0] += v
                    sum_rag_list[1][1] += sum_tag_dict[k]
                    sum_rag_list[1][2] += com_tag_dict[k]
                    sum_rag_list[1][3] += my_tag_dict[k]
                elif 7 >= v and v > 4:
                    sum_rag_list[2][0] += v
                    sum_rag_list[2][1] += sum_tag_dict[k]
                    sum_rag_list[2][2] += com_tag_dict[k]
                    sum_rag_list[2][3] += my_tag_dict[k]
                elif 4 >= v and v > 1:
                    sum_rag_list[3][0] += v
                    sum_rag_list[3][1] += sum_tag_dict[k]
                    sum_rag_list[3][2] += com_tag_dict[k]
                    sum_rag_list[3][3] += my_tag_dict[k]
                else:
                    sum_rag_list[4][0] += v
                    sum_rag_list[4][1] += sum_tag_dict[k]
                    sum_rag_list[4][2] += com_tag_dict[k]
                    sum_rag_list[4][3] += my_tag_dict[k]

                    sum_num_list[2] += sum_tag_dict[k]
                    sum_num_list[3] += com_tag_dict[k]
                    sum_num_list[4] += my_tag_dict[k]

                writer.writerow(["11以上"] + sum_rag_list[0])
                writer.writerow(["10以下8以上"] + sum_rag_list[1])
                writer.writerow(["7以下5以上"] + sum_rag_list[2])
                writer.writerow(["4以下2以上"] + sum_rag_list[3])
                writer.writerow(["1のみ"] + sum_rag_list[4])
                print(sum_rag_list)
                writer.writerow(sum_num_list)

category_file = "category_result.csv"
file_save(category_file,category_dict)
lock_file = "lock_result.csv"
file_save(lock_file,lock_dict)
free_file = "free_result.csv"
file_save(free_file,free_dict)
print(so_data)
