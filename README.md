# Mute Script

このスクリプトは、指定した時間帯にPCの音を自動的にミュート/アンミュートするツールです。

## 機能

- ユーザーが指定した時間帯に音をミュート/アンミュート
- 設定は簡単に追加・削除・編集可能
- 時間帯設定に重複がある場合は警告が表示される
- 設定した時間は自動的に保存され、次回実行時に反映されます

## 使い方

1. GitHubリポジトリをクローンします:
    ```bash
    git clone https://github.com/usxc/mute_script.git
    ```
   
2. 必要な依存関係をインストールします:
    ```bash
    cd mute_script
    pip install -r requirements.txt
    ```

3. スクリプトを実行します:
    ```bash
    python src/main.py
    ```

## 構成

- `src/`: ソースコードが含まれています
- `requirements.txt`: 必要なPythonパッケージのリスト
- `.gitignore`: Gitで追跡しないファイルを指定

## 依存関係

- `pycaw`: Windowsのオーディオ制御ライブラリ
- `schedule`: スケジュール管理ライブラリ
- `tkinter`: GUIを作成するためのライブラリ（Python標準ライブラリ）
