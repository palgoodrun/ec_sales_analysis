# EC売上分析ツール

## 作成日

- 作成日: 2026年9月2日
- 更新日: 2026年9月15日(初版)
- 　　　: 2026年9月15日(第2版: GitHub公開用内容修正)

## 概要
- ECサイトの売り上げCSVのデータをSQLiteデータベースに保存します
- SQLでキーごとに集計し、評価するデータフレームを生成します
- データフレームはKPIを追加後評価し判定項目を追加します
- 生成したデータフレームはExcelファイルで出力されます

## 環境構築

requirements.txtに記載された、ツールの実行・テストに必要なライブラリをインストールします。

### インストール内容とバージョン
- pandas==2.3.3
- openpyxl==3.1.5
- pytest==9.1.1

### 実行方法

python -m pip install -r requirements.txt

## 主な機能

- CSVの読み込み
- データベース用のフォルダ生成
- SQLiteへの保存
- SQLiteに保存したデータをSQLで集計する
- 必要KPIの追加
- KPIの評価、判定
- 結果のExcelファイルの保存

## 処理フロー

CSVファイル読み取り

↓

SQLite保存

↓

SQL集計

↓

KPI計算

↓

KPI評価

↓

KPI判定追加

↓

Excelファイル出力

## 集計内容

### カテゴリー別

category列ごとに集計する

### 販売チャネル別

sales_channel列ごとに集計する

### 月別

month列ごとに集計する

なお、month列は元CSVのorder_date列から購入月を確認して列を追加する


### 月 × カテゴリー別

month × category の組み合わせ単位で集計する

なお、month列は元CSVのorder_date列から購入月を確認して列を追加する

## KPI

- order_count: 注文件数
- completed_order_count: キャンセル件数を除いた注文件数
- cancelled_order_count: キャンセル件数
- total_quantity: 購入数量の合計
- total_sales: 購入金額の合計
- avg_order_value: 注文ごとの平均購入金額
- cancellation_rate: キャンセル率

## キャンセル率評価

- キャンセル率の値で危険度を評価する。
- コンフィグの閾値未満で「normal」、閾値以上で「warning」
- 閾値はコンフィグから変更可能。初期値 = 20

## 入力データ

### 入力ファイル

data / orders.csv

> サンプルデータには「data / orders_sample.csv」が格納されています
> 実行時には初期設定を以下のどちらかに変更してください
 - ファイル名を「orders.csv」に変更
 - 「config - input - data_file」を「 orders_sample.csv」に変更

### 必要な列

- order_date
> 入力必須
> フォーマット: yyyy-mm-dd

- customer_id
> 任意入力

- category
> 入力必須

- sales_channel
> 入力必須

- quantity
> 入力必須

- sales_amount
> 入力必須

- is_cancelled
> 入力必須

## 設定

### config.json

必須キー
- input - data_dir: 入力ファイル保存フォルダ
- input - data_file: 入力ファイル名

- database - db_dir: データベースフォルダ
- database - db_file: データベースファイル名
- database - table_name: データベーステーブル名

- thresholds - cancellation_threshold: キャンセル率閾値
> タイプ: int または float 入力値範囲: 0 ～ 100

- output - output_dir: 出力先フォルダ
- output - output_file: 出力先ファイル名

### log_config.json

必須キー
- log - level: ログレベル
> タイプ: 文字列
- log - file_path: ログファイルパス
> タイプ: 文字列

## 実行方法

- python -m scripts.main

> プロジェクトルート（ec_sales_analysis ディレクトリ）で実行

## 出力

### Excelファイル

output/ec_sales_analysis.xlsx

### 出力シート

抽出キーごとにシート作成
> category, sales_channel, month, month_category

## ログ

正常時確認できる内容
- logger設定完了
- 開始
- CSV読み込み完了: ファイル名
- データベース保存完了: 保存先パス, テーブル名
- データフレーム集計完了（集計キーごとに）
- KPI評価完了: 処理データフレーム数
- Excelファイル保存成功: 保存先パス
- 正常終了

異常時確認できる内容
- コンフィグの設定値エラー: 必須項目, 指定タイプ, 入力範囲
- データベースの保存失敗
- データベースの読み込み失敗

## ディレクトリ構成

```text
C:.
|   README.md
|   requirements.txt
|
+---config
|       config.json
|       log_config.json
|
+---data
|       orders_sample.csv
|
+---logs # 実行時に生成（Git管理対象外）
|       ec_sales_analysis.log
|
+---modules
|       config_loader.py
|       config_validator.py
|       database_manager.py
|       dataframe_formatter.py
|       kpi_calculator.py
|       kpi_evaluator.py
|       logger_setup.py
|       pandas_aggregator.py
|       result_exporter.py
|       sql_aggregator.py
|       sql_queries.py
|
+---output # 実行時に生成（Git管理対象外）
|       ec_sales_analysis.xlsx
|
+---scripts
|       main.py
|
\---tests
        test_aggregators.py
        test_config_validator.py
        test_kpi_evaluator.py
```

## テスト

### テスト内容

- test_aggregators.py

> SQLから抽出したデータベースがpandasで作成したデータベースと同等になるかを確認
>> 各キーごとにテスト

- test_config_validator.py

> config_validatorが異常値を正しくとらえるかを確認
>> 正常稼働確認, 型エラー, 範囲エラー

- test_kpi_evaluator.py

> kpi_evaluatorがKPIを正しく計算しているかを確認
>> キャンセル率計算, キャンセル率計算後の列追加

### 実行方法

python -m pytest tests -v

## 補足

## Clone Test