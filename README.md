# PCD selector

ローカル環境で動作するPCDグリッド選択ツールです。

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

### GitHub Pagesで公開する

1. このリポジトリをGitHubにプッシュ
2. リポジトリのSettings > Pagesに移動
3. Sourceを「main branch」または「gh-pages branch」に設定
4. `index.html`がルートにあることを確認
5. 公開されたURL（`https://yourusername.github.io/pcd_selector/`）にアクセス

### 使い方

1. 「メタデータYAML」ファイルを選択（必須）
2. 「投影情報YAML」ファイルを選択（オプション、grid_codeを取得）
3. Grid Codeを入力（デフォルト: 54SUE）
4. 「読み込み」ボタンをクリック
5. 地図上でグリッドをクリックして選択、または投げ縄ツールで範囲選択
6. 「選択したグリッド名をコピー」ボタンでクリップボードにコピー
