========== ========== ========== ==========
       A-SAPプロジェクト対話処理部  ver.1
========== ========== ========== ==========
【ソフト名】
 A-SAPプロジェクト対話処理部

【製作者】
 静岡大学 西田研究室修士2年　村手涼雅 

【動作環境】
 macOS Catalina ver 10.15.7

【最終更新日】
 2021/5/13

【ファイル名】
 ebdm_system.py
 console_bot.py

---------- ----------
◇ 概要 ◇
pythonとElastic searchによるチャットベースの対話システム

◇ 動作条件 ◇
python(バージョン3以上)及びElasticsearchをインストールしていること
Elasticsearchで対話データベースを登録していること

◇ ファイル構成 ◇
.	
├── README.txt		説明書
├── console_bot.py	コンソール上での対話制御プログラム
├── ebdm_system.py	実行するプログラム
├── makeDB.py		Elasticsearch上にデータベースを登録するプログラム
└── senario.csv		対話データベース

◇ インストール ◇
Elasticsearchのインストールについて

・macOSの場合
以下のコマンドを順番に実行することでインストールできます。
入手可能なバージョンはいくつかあるのでそれぞれのバージョンについては公式ページ(https://www.elastic.co/guide/en/elasticsearch/reference/current/targz.html)を確認してください。
(今回はバージョン7.11.2をインストールします)

$ wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.11.2-darwin-x86_64.tar.gz
$ tar -xzf elasticsearch-7.11.2-darwin-x86_64.tar.gz
$ cd elasticsearch-7.11.2
$ bin/elasticsearch-plugin install analysis-kuromoji
$ pip3 install elasticsearch

◇ 使い方 ◇
1.Elasticsearchの起動
→ 先ほど展開したElasticsearchのディレクトリまで移動し、以下の起動コマンドを入力
→ 使い終わったら停止コマンドを実行してElasticsearchを終了してください

起動コマンド
$ ./bin/elasticsearch -d -p pid

終了コマンド
$ pkill -F pid

2. 対話データベースの作成
→ makeDB.pyを実行することでsenario.csvにある対話用データをElasticsearchに自動で登録します。
3. 対話プログラムの実行
→ ebdm_system.pyを実行することで対話が始まります。初めに/startと打ってください。Enterで回答を送信できます。

◇ 参考 ◇
東中竜一郎・稲葉通将・水上 雅博(2020). Pythonで作る対話システム オーム社

◇ 未対応箇所 ◇
・console_bot.pyの質問リスト、回答リストがプログラム内に直に書かれています、csv或いはtxtファイル内に書き込んでプログラム実行時に読み取る仕様に変更予定です。
・想定外の回答に関して質問がループする仕様になっています。
・対話パターンが非常に少ないです、自由に回答しようとしても殆どの場合質問がループするので、senario.csvのqueryを参考にして回答してみてください。