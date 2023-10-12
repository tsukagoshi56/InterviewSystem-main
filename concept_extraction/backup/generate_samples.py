import MeCab
import re
import random
import json
import xml.etree.ElementTree

# AがBだ
body_1 = ['頭', 'のど', '胸', '背中', '胃', '目', 'お腹', '腕', '足', '首', '手', '肩', '腰',
        'お尻', '膝', 'はら', '後ろ']
body_2 = ['後頭部', '下腹部', 'へそ', 'こめかみ', 'みぞおち', '心臓']
b_verb_1 = ['痛い', '腫れている', '締め付けられる','ズキズキする', 'ジンジンする', 'むかむかする']
b_verb_2 = ['痛みがある', '違和感がある', '発疹がある']
# Aです
symptom = ['頭痛','腹痛','風邪','目がかすむ', 'めまい', '呼吸困難', '耳鳴り', '動悸']

# 息、咳など
substance = ['咳', '呼吸', '息', '鼻水', '便', '下痢', 'ウンチ']
s_verb = ['止まらない', '辛い']

# どんな時に
when = ['立ち上がった時', '力を入れるとき']
# いつから
fromwhen = ['今日', '昨日', '先週', '一日前']


# サンプル文に含まれる単語を置き換えることで学習用事例を作成
def random_generate(root):
    buf = ""
    pos = 0
    posdic = {}
    # タグがない文章の場合は置き換えしないでそのまま返す
    if len(root) == 0:
        return root.text, posdic
    # タグで囲まれた箇所を同じ種類の単語で置き換える
    for elem in root:
        if elem.tag == "body_1":
            __body1 = random.choice(body_1)
            buf += __body1
            posdic["body_1"] = (pos, pos+len(__body1))
            pos += len(__body1)
        elif elem.tag == "body_2":
            __body2 = random.choice(body_2)
            buf += __body2
            posdic["body_2"] = (pos, pos+len(__body2))
            pos += len(__body2)
        elif elem.tag == "b_verb_1":
            __b_verb_1 = random.choice(b_verb_1)
            buf += __b_verb_1
            posdic["b_verb_1"] = (pos, pos+len(__b_verb_1))
            pos += len(__b_verb_1)
        elif elem.tag == "b_verb_2":
            __b_verb_2 = random.choice(b_verb_2)
            buf += __b_verb_2
            posdic["b_verb_2"] = (pos, pos+len(__b_verb_2))
            pos += len(__b_verb_2)
        if elem.tail is not None:
            buf += elem.tail
            pos += len(elem.tail)
    return buf, posdic

# 現在の文字位置に対応するタグをposdicから取得
def get_label(pos, posdic):
    for label, (start, end) in posdic.items():
        if start <= pos and pos < end:
            return label
    return "O"

# MeCabの初期化
mecab = MeCab.Tagger()
mecab.parse('')

# 学習用ファイルの書き出し先 
fp = open("concept_samples.dat","w")

da = ''
# eamples.txt ファイルの読み込み
for line in open("examples.xml","r"):
    line = line.rstrip()
    # da= から始まる行から対話行為タイプを取得
    if re.search(r'^da=',line):
        da = line.replace('da=','')
    # 空行は無視
    elif line == "":
        pass
    else:
        # タグの部分を取得するため，周囲にダミーのタグをつけて解析
        root = xml.etree.ElementTree.fromstring("<dummy>"+line+"</dummy>")
        # 各サンプル文を1000倍に増やす
        for i in range(1000):
            sample, posdic = random_generate(root)

            # lis は[単語，品詞，ラベル]のリスト
            lis = []
            pos = 0
            prev_label = ""
            for line in mecab.parse(sample).splitlines():
                if line == "EOS":
                    break
                else:
                    word, feature_str = line.split("\t")
                    features = feature_str.split(',')
                    # 形態素情報の0番目が品詞
                    postag = features[0]
                    # 現在の文字位置に対応するタグを取得
                    label = get_label(pos, posdic)
                    # label がOでなく，直前のラベルと同じであればラベルに'I-'をつける
                    if label == "O":
                        lis.append([word, postag, "O"])
                    elif label == prev_label:
                        lis.append([word, postag, "I-" + label])
                    else:
                        lis.append([word, postag, "B-" + label])
                    pos += len(word)
                    prev_label = label
            
            # 単語，品詞，ラベルを学習用ファイルに書き出す
            for word, postag, label in lis:
                fp.write(word + "\t" + postag + "\t" + label + "\n")
            fp.write("\n")

fp.close()