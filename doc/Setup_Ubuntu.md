## Git
create ssh key
```cmd
$ ssh-keygen -t rsa
$ cat ~/.ssh/id_rsa.pub
```

update
```cmd
$ sudo add-apt-repository ppa:git-core/ppa
$ sudo apt update && sudo apt upgrade
```

git clone

## python
念のためバージョンをそろえる
```
$ python3 -V
Python 3.8.10
```

pythonインストール前に下記を実行(ubuntu 推奨環境)
```
sudo apt-get update; sudo apt-get install make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```

### pyenv
参考：https://github.com/pyenv/pyenv

python 3.8.10 install
```
pyenv install 3.8.10
```

### python(普通)
参考：https://www.python.jp/install/windows/install.html

```
wget <インストールするpythonバージョンのURL>
```

## Elasticsearch
install: https://www.elastic.co/guide/en/elasticsearch/reference/7.17/targz.html#targz
```
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.17.3-linux-x86_64.tar.gz
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.17.3-linux-x86_64.tar.gz.sha512
shasum -a 512 -c elasticsearch-7.17.3-linux-x86_64.tar.gz.sha512 
tar -xzf elasticsearch-7.17.3-linux-x86_64.tar.gz
cd elasticsearch-7.17.3/ 
```

japanese module: https://www.elastic.co/guide/en/elasticsearch/plugins/7.17/analysis-kuromoji.html
```
sudo bin/elasticsearch-plugin install analysis-kuromoji
```

## MeCab
インストール
```cmd
sudo apt install mecab libmecab-dev mecab-ipadic-utf8 swig -y
```

`~/.bashrc`に以下を追記
```
export MECABRC="/etc/mecabrc"
```

## pip3 install
モジュールのインストール
```
pip3 install 'elasticsearch>=7.0.0,<8.0.0'
pip3 install python-socketio
pip3 install scikit-learn
pip3 install mecab-python3
pip3 install requests
pip3 install websocket-client
```

参考
```
$ pip3 list
Package            Version
------------------ ---------
bidict             0.22.0
certifi            2021.10.8
charset-normalizer 2.0.12
elastic-transport  8.1.2
elasticsearch      7.17.3
idna               3.3
joblib             1.1.0
mecab-python3      1.0.5
numpy              1.22.3
pip                21.1.1
python-engineio    4.3.2
python-socketio    5.6.0
requests           2.27.1
scikit-learn       1.0.2
scipy              1.8.0
setuptools         3.3
threadpoolctl      3.1.0
urllib3            1.26.9
websocket-client   1.3.2
```
