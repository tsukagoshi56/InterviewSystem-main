# 引継ぎ資料

1. Ubuntu セットアップ
2. git
3. python

4. elasticsearch

    参照: https://www.elastic.co/guide/en/elasticsearch/reference/7.17/targz.html#targz

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

5. mecab

    インストール

    ```cmd
    sudo apt install mecab libmecab-dev mecab-ipadic-utf8 swig -y
    ```

    pythonコード実行時、"no such file or directory..."というエラーが出たら以下を試す
    
    案１：unidic-lite をインストール

    ```
    pip install unidic-lite
    ```

    案２：`~/.bashrc`に以下を追記し、読み込み
    
    ```
    export MECABRC="/etc/mecabrc"
    ``` 
   
    ```bash
    source ~/.bashrc
    ```


6. pip3 module

    とりあえず以下を入れる

    ``` 
    pip3 install 'elasticsearch>=7.0.0,<8.0.0'
    pip3 install python-socketio
    pip3 install scikit-learn
    pip3 install mecab-python3
    pip3 install requests
    pip3 install websocket-client
    ```
