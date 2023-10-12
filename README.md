# InterviewSystem
音声対話に基づく問診システム

## Requirement
Python 3.8.10

## Elasticsearch
```
cd /home/gokuri/InterviewSystem/elasticsearch
python3 makeDB.py
```

## Usage
1. DockerDesktop で任意の Elasticsearch コンテナを起動
2. Windows のサーバが起動していることを確認
3. socketio_client を実行

## Note
- 接続エラー時は実行ファイルのIPアドレスを確認する。`ipconfig`
