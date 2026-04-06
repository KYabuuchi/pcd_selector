# PCD selector

ローカル環境で動作するPCDグリッド選択ツールです。

[https://KYabuuchi.github.io/pcd_selector/](https://KYabuuchi.github.io/pcd_selector/)

## ローカル環境での使用方法

```bash
./selector.py pointcloud_metadata.yaml [map_projector_info.yaml]
```

![output](demo.gif)

## Webアプリケーション版

`index.html`をブラウザで開くか、GitHub Pagesでホストすることで、Webブラウザ上で動作します。

### ローカルで試す

```bash
# ブラウザで直接開く
open index.html
# または
python3 -m http.server 8000
# その後、ブラウザで http://localhost:8000 にアクセス
```
