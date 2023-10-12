import MeCab

if __name__ == '__main__':
    tagger = MeCab.Tagger()
    tagger.parse("")

    # sample_txt = '昨日からお腹が痛いです'
    sample_txt = '胸焼けがします'

    print(tagger.parse(sample_txt))

    keywords = []
    node = tagger.parseToNode(sample_txt)
    while node:
        if node.feature.split(",")[0] == u"名詞":
            keywords.append(node.surface)
        elif node.feature.split(",")[0] == u"形容詞":
            keywords.append(node.feature.split(",")[6])
        elif node.feature.split(",")[0] == u"動詞":
            keywords.append(node.feature.split(",")[6])
        node = node.next

    print(keywords)
