import MeCab

from elasticsearch import Elasticsearch

tagger = MeCab.Tagger('-Owakati')
tagger.parse("")


es = Elasticsearch()

# ドキュメントを検索
# result = es.search(index="q4", query={
#                    'match': {'query': "ありません"}}, size=10)
result = es.search(index="q29", query={
                   'match': {'query': "脈が正常ではないです"}}, size=10)


# result = es.search(index="parrot", query={
#    'match': {'query': "胸焼けがします"}}, size=10)

# 検索結果からドキュメントの内容のみ表示
for document in result["hits"]["hits"]:
    print(document)
