# memo
1. run_server.batの実行
   1. npm start が実行され、Server.js以下が動く
   2. サーバーが立立ち上がる
2. run_main_app.vbsの実行
   1. /main_app/以下が実行される
3. run_video_app.batの実行
   1. ~/video_app/以下が実行される

- ./main_appはpythonで書かれている、それ以外はnode.js


## main_appの動作　
- google cloudのAPIを使用(音声→テキストを行うAPI)
- https://github.com/googleapis/python-speech/tree/main/samples/microphone ここら辺をまねてる？
- pyaudio（音声の録音） -> google で実装