import dill
import MeCab

mecab = MeCab.Tagger()
mecab.parse('')

# SVMモデルの読み込み
with open("svc.model", "rb") as f:
    vectorizer = dill.load(f)
    label_encoder = dill.load(f)
    svc = dill.load(f)


def extract_da(utt):  # 発話から対話行為タイプを推定
    words = []
    for line in mecab.parse(utt).splitlines():
        if line == "EOS":
            break
        else:
            word, feature_str = line.split("\t")
            words.append(word)
    tokens_str = " ".join(words)
    X = vectorizer.transform([tokens_str])
    Y = svc.predict(X)
    # 数値を対応するラベルに戻す
    da = label_encoder.inverse_transform(Y)[0]
    return da


if __name__ == '__main__':

    test_utt = [
        "お腹が痛いです", "下腹部が痛いんですよ", "頭の後ろがズキズキする", 'お腹が痛みます', 'お腹が痛む',
        'お腹の下のほうが痛みます', "熱はないです", "上です", "上のあたりです", "上の方です", "上の方が痛みます",
        "後ろが痛みます",
        "頭痛がします", "腹痛がするんです", "家",
        "お腹の上の方が痛いです"
    ]

    for utt in test_utt:
        da = extract_da(utt)
        print(utt, da)
