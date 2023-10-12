# 技術的な覚書

## Elasticsearch

### 検索：search()
    - https://elasticsearch-py.readthedocs.io/en/v8.2.2/api.html#elasticsearch.Elasticsearch.search
    - size: 取得してくる件数
    - 

### バルクインサート
https://qiita.com/satto_sann/items/8a63761bbfd6542bb9a2#%E3%83%90%E3%83%AB%E3%82%AF%E3%82%A4%E3%83%B3%E3%82%B5%E3%83%BC%E3%83%88


## Javascript

### アットマーク

```
// decorator lights is a function which receives the class as an argument
let lights = function(tree) {
  // The behaviour of the class is modified here
  tree.treeLights = 'Christmas lights'
}

@lights  // the decorator is applied here
class ChristmasTree {}

console.log(ChristmasTree.treeLights);  // logs Christmas lights
```

https://www.web-dev-qa-db-ja.com/ja/javascript/es6-javascript%E3%81%A7%E3%82%A2%E3%83%83%E3%83%88%E3%83%9E%E3%83%BC%E3%82%AF%EF%BC%88%EF%BC%89%E3%81%AF%E4%BD%95%E3%82%92%E3%81%97%E3%81%BE%E3%81%99%E3%81%8B%EF%BC%9F-%EF%BC%88ecmascript-2015%EF%BC%89/1054489872/


## VSCode 拡張機能
```
code --install-extension donjayamanne.python-environment-manager
code --install-extension donjayamanne.python-extension-pack
code --install-extension DotJoshJohnson.xml
code --install-extension KevinRose.vsc-python-indent
code --install-extension mechatroner.rainbow-csv
code --install-extension ms-python.isort
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension njpwerner.autodocstring
code --install-extension tomoki1207.pdf
code --install-extension VisualStudioExptTeam.intellicode-api-usage-examples
code --install-extension VisualStudioExptTeam.vscodeintellicode
code --install-extension yzhang.markdown-all-in-one
```