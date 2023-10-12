# Concept extraction by CRF

コンセプト抽出を行うモデルの訓練、動作確認

```
python3 generate_concept_samples.py
python3 train_concept_model.py
python3 concept_extractor.py
```


## メモ
// A(部位)がB(形容詞、動詞、形容動詞)です
// A(物体)がB(形容詞、動詞、形容動詞)です
// (症状名)がする
// (症状名)気味です
// 病名

// 単数を複数回繰り返すことで可能
// 「お腹が痛いのと便秘気味です」 → <単数> と <単数>　と考えそれぞれ認識するようにすればよさそう

便が赤色です。

<body>頭</body>が<>痛い</a>

<symptoms>腹痛</symptoms>がする



<material>鼻水</material>が<m_verb>止まらない</m_verb>

鼻水、便、息がきつい

<symptoms>腹痛</symptoms>が激しいです
<symptoms>便秘</symptoms>気味です


da=multi-symptoms


<body_2>後頭部</body_2>が<b_verb>痛い</b_verb>
<subs>鼻水</subs>が<s_verb>止まらない</s_verb>
<symp>頭痛</symp>です
<symp>頭痛</symp>がする
<symp>頭痛</symp>がつらい



頭が痛い
お腹が痛い
胸が痛い
背中が痛い
手足に痺れ

咳が出る

胸やけ