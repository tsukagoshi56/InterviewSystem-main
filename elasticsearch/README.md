# Elasticsearch

コンテナの準備(docker desktop を使用可)
```
(sudo) docker pull docker.elastic.co/elasticsearch/elasticsearch:7.17.7
(sudo) docker run --name "sample-es" -p 127.0.0.1:9200:9200 -p 127.0.0.1:9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.17.7
```

docuemnt 挿入
```
python3 makeDB.py
```

document 削除
```
curl -XDELETE 'http://localhost:9200/*'
```

