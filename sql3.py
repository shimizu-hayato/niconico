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

tag_list = []

vew_tag_dict = {}
com_tag_dict = {}
myl_tag_dict = {}

sum_vew_dict = {}
sum_com_dict = {}
sum_myl_dict = {}



so_data = [0,0,0]
#動画数129 再生数35032915, コメント数3, マイリスト数248216
so_num = 0
flg = 1


datename = "20170730"
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
        if tag[1] == flg:
            tag_list.append(tag[0])
            
            try:
                vew_tmp = vew_tag_dict[tag[0]]
                com_tmp = com_tag_dict[tag[0]]
                myl_tmp = myl_tag_dict[tag[0]]
        
                vew_tmp.append(int(data["view_counter"]))
                com_tmp.append(int(data["comment_num"]))
                myl_tmp.append(int(data["mylist_counter"]))

        
                vew_tag_dict[tag[0]] = vew_tmp
                com_tag_dict[tag[0]] = com_tmp
                myl_tag_dict[tag[0]]  = myl_tmp

            except Exception as e:
                
                vew_tag_dict[tag[0]] = [int(data["view_counter"])]
                com_tag_dict[tag[0]] = [int(data["comment_num"])]
                myl_tag_dict[tag[0]]  = [int(data["mylist_counter"])]

def sum_count_dict(dictfile):
    sum_dict = {}
    for k,v in sorted(dictfile.items(),key=lambda x:x[1],reverse=True):
        sum_tag = sum(v)
        sum_dict.update({k:sum_tag})

    return(sum_dict)

def dev_dict(dictfile):
    dev_dict = {}  
    for k,v in sorted(dictfile.items(),key=lambda x:x[1],reverse=True):
        tmp = numpy.std(numpy.array(v))
        dev_dict.update({k:tmp})
    return(dev_dict)
        
    

sum_vew_dict = sum_count_dict(vew_tag_dict)
sum_com_dict = sum_count_dict(com_tag_dict)
sum_myl_dict = sum_count_dict(myl_tag_dict)

dev_vew_dict = dev_dict(vew_tag_dict)
dev_com_dict = dev_dict(com_tag_dict)
dev_myl_dict = dev_dict(myl_tag_dict)

tag_dict = dict(collections.Counter(tag_list))


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

#偏差値を計算する関数
"""
def std_score(a):
    return numpy.round_(50+10*(a-numpy.average(a))/numpy.std(a))

def test(label,a):
    print label
    print u"　得点",a
    print u"　合計",numpy.sum(a)
    print u"　平均(average)",numpy.average(a)
    print u"　分散( variance)",numpy.var(a)
    print u"　標準偏差(standard deviation )",numpy.std(a)
    print u"　偏差値(standard score)\n    ",std_score(a)
"""
file_flg = 1
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
        if file_flg == 1:
        
            for k,v in sorted(dictfile.items(),key=lambda x:x[1],reverse=True):
                csv_list = []
                sum_num += v
                csv_list += [k,v]
                csv_list += [sum_vew_dict[k],sum_com_dict[k],sum_myl_dict[k],""]
                csv_list += [round(sum_vew_dict[k]/v)
                             ,round(sum_com_dict[k]/v)
                             ,round(sum_myl_dict[k]/v)
                             ,round(dev_vew_dict[k])
                             ,round(dev_com_dict[k])
                             ,round(dev_myl_dict[k])]

                writer.writerow(csv_list)
                
                #print(vew_tag_dict[k])
            
        else:
            for k,v in sorted(dictfile.items(),key=lambda x:x[1],reverse=True):
                if v > 10:
                    sum_rag_list[0][0] += v
                    sum_rag_list[0][1] += sum_vew_dict[k]
                    sum_rag_list[0][2] += sum_com_dict[k]
                    sum_rag_list[0][3] += sum_myl_dict[k]
                    
                elif 10 >= v and v > 7:
                    sum_rag_list[1][0] += v
                    sum_rag_list[1][1] += sum_vew_dict[k]
                    sum_rag_list[1][2] += sum_com_dict[k]
                    sum_rag_list[1][3] += sum_myl_dict[k]
                elif 7 >= v and v > 4:
                    sum_rag_list[2][0] += v
                    sum_rag_list[2][1] += sum_vew_dict[k]
                    sum_rag_list[2][2] += sum_com_dict[k]
                    sum_rag_list[2][3] += sum_myl_dict[k]
                elif 4 >= v and v > 1:
                    sum_rag_list[3][0] += v
                    sum_rag_list[3][1] += sum_vew_dict[k]
                    sum_rag_list[3][2] += sum_com_dict[k]
                    sum_rag_list[3][3] += sum_myl_dict[k]
                else:
                    sum_rag_list[4][0] += v
                    sum_rag_list[4][1] += sum_vew_dict[k]
                    sum_rag_list[4][2] += sum_com_dict[k]
                    sum_rag_list[4][3] += sum_myl_dict[k]

                sum_num_list[2] += sum_vew_dict[k]
                sum_num_list[3] += sum_com_dict[k]
                sum_num_list[4] += sum_myl_dict[k]

            writer.writerow(["11以上"] + sum_rag_list[0])
            writer.writerow(["10以下8以上"] + sum_rag_list[1])
            writer.writerow(["7以下5以上"] + sum_rag_list[2])
            writer.writerow(["4以下2以上"] + sum_rag_list[3])
            writer.writerow(["1のみ"] + sum_rag_list[4])
            print(sum_rag_list)
            writer.writerow(sum_num_list)

if flg == 2:
    category_file = "category_result.csv"
    file_save(category_file,tag_dict)
elif flg == 1:
    lock_file = "lock_result.csv"
    file_save(lock_file,tag_dict)
elif flg == 0:
    free_file = "free_result.csv"
    file_save(free_file,tag_dict)
print(so_data)
