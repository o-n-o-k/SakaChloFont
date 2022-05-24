#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
漢字をひらがなに変換して指定フォントで画像出力する
フォント収録文字リストを用いて存在する単語は原文のまま

fonttools PySimpleGUI PySimpleGUIQt pykakasi Pillow パッケージを使用
pip install fonttools
pip install pysimplegui
pip install PySimpleGUIQt
pip install pykakasi
pip install Pillow

日本語入力できない時
/usr/lib/x86_64-linux-gnu/qt5/plugins/platforminputcontexts/libfcitxplatforminputcontextplugin.so
を以下フォルダにコピー
/home/○○○/.local/lib/python3.8/site-packages/PySide2/Qt/plugins/platforminputcontexts

"""

from fontTools import ttLib

# import PySimpleGUI as sg
import PySimpleGUIQt as sg
import pykakasi
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import random


txtdata = """秘密結社holoXの掃除屋でholoXのインターン生。
冷静沈着で淡々と組織からの依頼をこなす。
音楽が好きで、よく音楽を聴いている。
本人は否定しているが、ツンデレに見られるらしい。"""

# フォントを指定
font_file = "./SakaChloFont_P.ttf"
# 出力画像
saveimgfile = "./image.png"

outtxt = ""

# フォント収録文字を取得
with ttLib.ttFont.TTFont(font_file, fontNumber=0) as font:
    cmap = font.getBestCmap()
chrlist = ""
i = 0
for cmap_key in cmap:
    chrlist = chrlist + chr(cmap_key)

# GUIレイアウト
sg.theme("SystemDefault")
layout = [
    [sg.Multiline(txtdata, key="basetxt", size=(80, 6))],
    [sg.Button("↓ 全角ひらがな変換 ↓", key="convtxt")],
    [sg.Multiline(key="hiratxt", size=(80, 6))],
    [
        sg.Text("サイズ", size=(4, 1)),
        sg.InputText(key="sfontsize", default_text="24", size=(4, 0.8)),
        sg.Text("文字色", size=(4, 1)),
        sg.InputText(key="txt_r", default_text="0", size=(4, 0.8)),
        sg.InputText(key="txt_g", default_text="0", size=(4, 0.8)),
        sg.InputText(key="txt_b", default_text="0", size=(4, 0.8)),
        sg.Text("背景色", size=(4, 1)),
        sg.InputText(key="bg_r", default_text="255", size=(4, 0.8)),
        sg.InputText(key="bg_g", default_text="255", size=(4, 0.8)),
        sg.InputText(key="bg_b", default_text="255", size=(4, 0.8)),
        sg.Button("Random", key="ran_col", size=(6, 0.8)),
        sg.Button("画像生成", key="convimg", size=(12, 1)),
        sg.Text(saveimgfile, size=(16, 1)),
    ],
    [sg.Image("./image.png", key="outimg")],
]
window = sg.Window("沙花叉直筆風ジェネレーター", layout, size=(800, 600))

# 引数 全角変換したい文字列
def clean_text(text):
    abc_half = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    abc_full = "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ"
    digit_half = "0123456789"
    digit_full = "０１２３４５６７８９"
    katakana_half = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜｦﾝ"
    katakana_full = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
    punc_half = "!#$%&¥()*+,-./:;<=>?@[]^_`{|}~"
    punc_full = "！＃＄％＆￥（）＊＋，－．／：；＜＝＞？＠［］＾＿｀｛｜｝～"

    tmp01 = "ｶﾞｷﾞｸﾞｹﾞｺﾞｻﾞｼﾞｽﾞｾﾞｿﾞﾀﾞﾁﾞﾂﾞﾃﾞﾄﾞﾊﾞﾋﾞﾌﾞﾍﾞﾎﾞﾊﾟﾋﾟﾌﾟﾍﾟﾎﾟ"
    tmp02 = "ガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポ"
    transtable02 = {}
    for i in range(len(tmp02)):
        be = tmp01[i * 2 : i * 2 + 2]
        af = tmp02[i]
        transtable02[be] = af

    text = str(text).replace("\u3000", " ")  # 全角スペースを半角に

    before = abc_full + digit_full + katakana_half + punc_full
    after = abc_half + digit_half + katakana_full + punc_half

    transtable01 = str.maketrans(before, after)
    text = text.translate(transtable01)
    text = text.translate(transtable02)

    text = text.translate(
        str.maketrans({chr(0x0021 + i): chr(0xFF01 + i) for i in range(94)})
    )

    return text


# 引数 ひらがなにしたい文字列
def kanji2hira(txtdata):
    outtxt = ""
    kakasi = pykakasi.kakasi()

    """
    #kakasi旧api用
    #漢字からひらがな
    kakasi.setMode('J', 'H')
    #カタカナからひらがな
    #kakasi.setMode("K", "H")
    kconv = kakasi.getConverter()
    """

    # 全角変換
    txtdata = clean_text(txtdata)

    txtdata = txtdata.split("\n")
    for txt1 in txtdata:
        # 旧apiいつかなくなるかも
        # kana = kconv.do(txt1)
        # outtxt = outtxt + kana + '\n'

        # 新api 辞書型で変換される
        for txt2 in kakasi.convert(txt1):
            orig_txt = txt2["orig"]
            # 一文字づつに切り分けて フォントに収録されているか検索
            f_word = True
            for word1 in orig_txt:
                if not (word1 in chrlist):
                    f_word = False
                    break

            if f_word:
                outtxt = outtxt + txt2["orig"]  # 収録されていれば原文
            else:
                outtxt = outtxt + txt2["hira"]  # 収録されていなければひらがな

        outtxt = outtxt + "\n"

    outtxt = outtxt.strip()
    return outtxt


# 引数 画像にする文字列 フォントサイズ
def hira2img(outtxt, fontsize):
    x = []
    y = 0
    txtdata = outtxt.split("\n")
    for txt1 in txtdata:
        x.append(len(txt1))
        y += 1

    # 画像の基本設定
    mx = max(x)
    if mx < 4:
        mx = 3
    if y < 2:
        y = 1
    canvasSize = (fontsize * (mx + 2), fontsize * (y + 2))
    backgroundRGB = (int(values["bg_r"]), int(values["bg_g"]), int(values["bg_b"]))
    textRGB = (int(values["txt_r"]), int(values["txt_g"]), int(values["txt_b"]))

    # 画像作成
    img = PIL.Image.new("RGB", canvasSize, backgroundRGB)
    draw = PIL.ImageDraw.Draw(img)

    # 文字列の描画
    font = PIL.ImageFont.truetype(font_file, fontsize)
    textWidth, textHeight = draw.textsize(outtxt, font=font)

    # 画像のリサイズ
    textTopLeft = (fontsize, fontsize)
    draw.text(textTopLeft, outtxt, fill=textRGB, font=font)
    csize = (0, 0, textWidth + (fontsize * 2), fontsize * (y + 2))
    img = img.crop(csize)

    img.save(saveimgfile)
    return


while True:
    event, values = window.read()
    if event in (None, "終了"):
        break

    # ひらがな変換ボタン
    elif event == "convtxt":
        window["hiratxt"].update(kanji2hira(values["basetxt"]))

    # 画像生成ボタン
    elif event == "convimg":
        hira2img(values["hiratxt"], int(values["sfontsize"]))
        window["outimg"].update(saveimgfile)

    # Randボタン
    elif event == "ran_col":
        window["txt_r"].update(str(random.randint(0, 255)))
        window["txt_g"].update(str(random.randint(0, 255)))
        window["txt_b"].update(str(random.randint(0, 255)))
        window["bg_r"].update(str(random.randint(0, 255)))
        window["bg_g"].update(str(random.randint(0, 255)))
        window["bg_b"].update(str(random.randint(0, 255)))

window.close()
# print(values)
