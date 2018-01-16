#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib


url = "http://ext.nicovideo.jp/api/getthumbinfo/sm4005866"
f = urllib.urlopen(url)
html = f.read()
print html


