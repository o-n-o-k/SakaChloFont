#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
フォントに収録されている文字を列挙する

fonttools パッケージを使用
pip install fonttools

'''

from fontTools import ttLib

#フォントを指定
font_file = "./SakaChloFont_P.ttf"
#出力先
list_file = "./chrlist.txt"
#1行の文字数
w = 32


with ttLib.ttFont.TTFont(font_file, fontNumber=0) as font:
    # フォント収録文字を取得
    cmap = font.getBestCmap()

chrlist = ""
i = 0
for cmap_key in cmap:
    chrlist = chrlist + chr(cmap_key)
    i += 1
    if i==w:
        chrlist = chrlist + "\n"
        i = 0

f = open(list_file, "w")
f.write(chrlist)
f.close()

