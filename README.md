# flocy-gcp

フロッキーの GCP 版。
たぶん Cloud Functions を使います。

### 環境

- python3.10（>=3.10,<4）
- poetry
  - `flocky-gcp` パッケージとして作成
  - `vertualenv` は使用しない
- Cloud Functions

### python ライブラリのインストール

poetry を使用しています。Docker に入って、以下のようにインストール

```bash
poety add flask
```

### ローカル開発

1. Docker 立ち上げ

```bash
docker compose up
```

2. http://localhost:8080/ にアクセス

### デプロイ

```bash
gcloud functions deploy helloWorld \
  --entry-point=hello_world \
  --runtime=python311 \
  --trigger-http \
  --source=src/flocky_gcp/main.py \
  --allow-unauthenticated
```
