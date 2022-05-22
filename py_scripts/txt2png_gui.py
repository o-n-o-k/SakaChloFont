#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
漢字をひらがなに変換して指定フォントで画像出力する

PySimpleGUI pykakasi Pillow パッケージを使用
pip install pysimplegui
pip install pykakasi
pip install Pillow

"""

import PySimpleGUI as sg
import pykakasi
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont

txtdata = u'''秘密結社holoXの掃除屋でholoXのインターン生。
冷静沈着で淡々と組織からの依頼をこなす。
音楽が好きで、よく音楽を聴いている。
本人は否定しているが、ツンデレに見られるらしい。'''

#フォントを指定
font_file = "./SakaChloFont_P.ttf"
#出力画像
saveimgfile='./image.png'
outtxt=''


sg.theme('SystemDefault')
layout = [
        [sg.Multiline(txtdata,key="basetxt",size=(800,6))],
        [sg.Button(' 全角ひらがな変換 ',key="convtxt")],
        [sg.Multiline(key="hiratxt",size=(800,6))],
        [sg.Text("フォントサイズ"), sg.InputText(key="sfontsize",default_text='24',size=(6,)),
         sg.Button(' 画像生成 ',key="convimg"),sg.Text(saveimgfile)],
        [sg.Image('./image.png',key="outimg")],
]
window = sg.Window("沙花叉直筆風ジェネレーター", layout,size=(800,600))

#引数 ひらがなにしたい文字列
def kanji2hira(txtdata):
    outtxt=""
    kakasi = pykakasi.kakasi()
    #漢字からひらがな
    kakasi.setMode('J', 'H')
    #カタカナからひらがな
    #kakasi.setMode("K", "H")
    kconv = kakasi.getConverter()
    
    #全角変換
    txtdata=txtdata.translate(str.maketrans({chr(0x0021 + i): chr(0xFF01 + i) for i in range(94)}))
    
    txtdata = txtdata.split("\n")
    for txt1 in txtdata:
        #旧apiいつかなくなるかも
        kana = kconv.do(txt1)
        outtxt=outtxt+kana+'\n'

        #新api全部ひらがなになっちゃう
        #outtxt=outtxt+''.join([item['hira'] for item in kakasi.convert(txt1)])
        
    return outtxt

#引数 画像にする文字列 フォントサイズ
def hira2img(outtxt,fontsize):
    x = []
    y = 0
    txtdata = outtxt.split("\n")
    for txt1 in txtdata:
        x.append(len(txt1))
        y += 1
        
    #画像の基本設定
    canvasSize    = (fontsize*max(x), fontsize*(y+3))
    backgroundRGB = (255, 255, 255)
    textRGB       = (0, 0, 0)

    #画像作成
    img  = PIL.Image.new('RGB', canvasSize, backgroundRGB)
    draw = PIL.ImageDraw.Draw(img)

    #文字列の描画
    font = PIL.ImageFont.truetype(font_file, fontsize)
    textWidth, textHeight = draw.textsize(outtxt,font=font)

    #画像のリサイズ
    
    textTopLeft = (fontsize, fontsize) 
    draw.text(textTopLeft, outtxt, fill=textRGB, font=font)
    csize = (0,0,textWidth+(fontsize*2),fontsize*(y+2))
    img = img.crop(csize)

    img.save(saveimgfile)
    return


while True:
    event, values = window.read()
    if event in (None, '終了'):
        break
    
    #ひらがな変換ボタン
    elif event == 'convtxt':
        window['hiratxt'].update(kanji2hira(values['basetxt']))

    #画像生成ボタン
    elif event == 'convimg':
        hira2img(values['hiratxt'],int(values['sfontsize']))
        window['outimg'].update(saveimgfile)
        
window.close()
#print(values)
