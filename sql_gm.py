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

#datename = "20170727"
fh = open(r'monthly_rank_movie/' + datename + '_rank_movie.json','r',encoding="utf-8_sig")
#fh = open(r'monthly_rank_movie/' + datename + '_rank_movie.json','r',encoding="utf-16")
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

        #tag[0] = tag[0].encode('cp932', 'ignore').decode('cp932')
        if tag[1] == 2:
            category_tag_list.append(tag[0])
        elif tag[1] == 1:
            lock_tag_list.append(tag[0])
        elif tag[1] == 0:
            free_tag_list.append(tag[0])
        #print(tag[0])
        """
        if tag[0] not in sum_tag_dict.keys():
            sum_tag_dict.update({tag[0]:0})
        if tag[0] not in com_tag_dict.keys():
            com_tag_dict[tag[0]] = 0
        if tag[0] not in my_tag_dict.keys():
            my_tag_dict[tag[0]] = 0
        """

        if sum_tag_dict.get(tag[0]) != None:
            """
            tmp_sum = sum_tag_dict[tag[0]]
            sum_tag_dict[tag[0]] = tmp_sum + int(data["view_counter"])
            """
            sum_tag_dict[tag[0]] += int(data["view_counter"])
        else:
            sum_tag_dict[tag[0]] = int(data["view_counter"])

        if com_tag_dict.get(tag[0]) != None:
            tmp_com = com_tag_dict[tag[0]]
            com_tag_dict[tag[0]] = tmp_com + int(data["comment_num"])
        else:
            com_tag_dict[tag[0]] = int(data["comment_num"])

        if my_tag_dict.get(tag[0]) != None:
            tmp_my = my_tag_dict[tag[0]]
            my_tag_dict[tag[0]] = tmp_my + int(data["mylist_counter"])
        else:
            my_tag_dict[tag[0]] = int(data["mylist_counter"])


if sorted(lock_tag_list) == sorted(free_tag_list):
    exit(1)
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


for flg in range(3):
    if flg == 0:
        filename = datename + "_category_result.csv"
        dictfile = category_dict
    if flg == 1:
        filename = datename + "_lock_result.csv"
        dictdile = lock_dict
        print(dictdile)
    if flg == 2:
        filename = datename + "_free_result.csv"
        dictfile = free_dict
    #with codecs.open(filename,'w',encoding = "utf-8_sig") as f:
    with codecs.open(filename,'w',encoding="utf-16") as f:
        writer = csv.writer(f, lineterminator='\n')
        sum_num = 0
        sum_num_list = []
        sum_rag_list = [[0,0,0,0],
                        [0,0,0,0],
                        [0,0,0,0],
                        [0,0,0,0],
                        [0,0,0,0]]
        sum_num_list =["「合計」",0,0,0,0]


        #for k,v in sorted(dictfile.items(),key=lambda x:x[1],reverse=True):
        if flg == 0:
            print(dictfile.keys())


        for k,v in dictfile.items():
            if flg == 1:
                print(dictfile)
            csv_list = []
            sum_num += v
            csv_list += [k,v]
            csv_list += [sum_tag_dict[k],com_tag_dict[k],my_tag_dict[k],""]
            csv_list += [round(sum_tag_dict[k]/v)
                        ,round(com_tag_dict[k]/v)
                        ,round(my_tag_dict[k]/v)]

            writer.writerow(csv_list)
        else:
            print("Error")

            """
            sum_num += v
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
            """
            #print(sum_num_list[1])
        """
        writer.writerow(["11以上"] + sum_rag_list[0])
        writer.writerow(["10以下8以上"] + sum_rag_list[1])
        writer.writerow(["7以下5以上"] + sum_rag_list[2])
        writer.writerow(["4以下2以上"] + sum_rag_list[3])
        writer.writerow(["1のみ"] + sum_rag_list[4])
        print(sum_rag_list)
        """
        """
        sum_num_list.append(sum(sum_tag_dict.values()))
        sum_num_list.append(sum(com_tag_dict.values()))
        sum_num_list.append(sum(my_tag_dict.values()))
        """
        #print(sum_num_list)
        writer.writerow(sum_num_list)
print(so_data)
