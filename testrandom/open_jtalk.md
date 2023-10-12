# open jtalk

*基本、Windows上で行うので必要なし*

## ubuntu セットアップ

Open JTalk に名工大の音声モデルを使用して音声合成を行う\
`cp`コマンド実行後、ダウンロードファイルは削除OK

参考：https://www.rcnp.osaka-u.ac.jp/~kohda/linux/espeak.html

install open_jtalk
```
$ sudo apt install open-jtalk open-jtalk-mecab-naist-jdic hts-voice-nitech-jp-atr503-m001
```

install 音声データ
```
$ wget https://sourceforge.net/projects/mmdagent/files/MMDAgent_Example/MMDAgent_Example-1.8/MMDAgent_Example-1.8.zip
$ unzip MMDAgent_Example-1.8.zip
$ sudo cp -r MMDAgent_Example-1.8/Voice/* /usr/share/hts-voice/
```


## 音声出力(wsl2 -> windows)

必要に応じて
```
sudo apt install alsa-utils
sudo apt install pulseaudio
sudo apt install pulseaudio-utils
```

上記のみではたぶん無理\
https://astherier.com/blog/2020/08/wsl2-ubuntu-sound-setting/

ダウンロード先が消えている時に見る\
https://qiita.com/nanakochi123456/items/0c3dbdd49baef080ea2f