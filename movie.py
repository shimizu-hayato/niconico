#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
動画idから動画の詳細情報を取得

"""
import sys
import codecs
import re
import urllib,urllib.request
import json
from xml.etree.ElementTree import *
from collections import OrderedDict
from datetime import datetime

"""
rank.jsonからランキングに上がっている動画のidを取得しrank_idリストに格納
"""

#日付取得
today = datetime.today()
datename = today.strftime("%Y%m%d")
month = datetime(today.year,today.month-1,1)


rank_id = []

#rank_pass = "daily_rank/"
#movie_pass = "daily_rank_movie/"

rank_pass = "monthly_rank/"
movie_pass = "monthly_rank_movie/"


fh = open(rank_pass + datename + '_rank.json','r',encoding="utf-8_sig")
rank_data = json.loads(fh.read())
for data in rank_data:
    #print(x['link'].encode('cp932', "ignore").decode('cp932'))
    text = data['link']
    rank_num = data['rank']
    a = re.search('http://www.nicovideo.jp/watch/((s|n)(m|o)\d+)', text)
    #print(a.group(1))
    rank_id.append([a.group(1),rank_num])
"""
動画の詳細データを(http://ext.nicovideo.jp/api/getthumbinfo/動画id)から取得し
辞書型に直したのちにmovie_jsonへ格納

"""
movie_json = []
for id in rank_id:
    movie_url = "http://ext.nicovideo.jp/api/getthumbinfo/" + id[0]
    req = urllib.request.Request(url=movie_url)
    fp = urllib.request.urlopen(req)
    movie_xml = fp.read().decode('utf-8')
    root = fromstring(movie_xml)

    #動画が削除されている場合は処理を飛ばす
    if root.get("status") == 'fail':
        print('No movie '+id[0])
        continue


    link = root.findall(".//thumb/")
    tags = root.findall(".//tags/")
    month_day = 0
    for e in link:
        if e.tag == 'first_retrieve':
            upload = e.text
            month_day = datetime.strptime(upload[:10], '%Y-%m-%d')
            break
            
    if month_day < month:
        print('under '+str(month_day)+' upload movie'+id[0])
        continue

    #タグは複数あるためリストにする
    #カテゴリやロックされているタグは数字でラベルを付ける
    tag_list = []
    for t in tags:
        tag_id = []
        if t.get("category"):
            tag_id = [t.text,2]
        elif t.get("lock"):
            tag_id = [t.text,1]
        else:
            tag_id = [t.text,0]

        tag_list.append(tag_id)

    tag_list = sorted(tag_list, key=lambda x: int(x[1]),reverse=True)
    movie_dict = OrderedDict()

    movie_dict.update({'rank':id[1]})
    for e in link:
        if e.tag == 'tags':
            movie_dict.update({e.tag: tag_list})
        else:
            movie_dict.update({e.tag: e.text})

    movie_json.append(movie_dict)


today = datetime.today()
datename = today.strftime("%Y%m%d")

print(len(movie_json))

#jsonへ格納
text = json.dumps(movie_json,indent = 4,ensure_ascii=False)
f = codecs.open(movie_pass + datename + "_rank_movie.json",'w','utf-8')
f.write(text)
