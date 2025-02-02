# flocy-gcp

フロッキーの GCP 版。
たぶん Cloud Functions を使います。

### 環境

- python3.10（>=3.10,<4）
- FastAPI
- poetry
  - `flocky-gcp` パッケージとして作成
  - `vertualenv` は使用しない
- GCP
  - プロジェクト: flocky-449707
  - Cloud Run
  - Artifact Registry
    - Docker イメージ名: us-central1-docker.pkg.dev/flocky-449707/cloud-run-source-deploy/chat-flocky:latest
  - （あとで設定）サービスアカウント: `chat-flocky-sa@flocky-449707.iam.gserviceaccount.com`
    - role
      - roles/iam.serviceAccountUser
      - （あとで削除）roles/cloudfunctions.developer

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

1. Docker イメージのビルド

```bash
$ docker build -t us-central1-docker.pkg.dev/flocky-449707/cloud-run-source-deploy/chat-flocky:latest .
```

2. Artifact Registry へ push

```bash
$ docker push us-central1-docker.pkg.dev/flocky-449707/cloud-run-source-deploy/chat-flocky:latest
```

3. Cloud Run にデプロイ

```bash
$ gcloud run deploy --image us-central1-docker.pkg.dev/flocky-449707/cloud-run-source-deploy/chat-flocky:latest --platform=managed  --project=flocky-449707
```

4. 環境変数の設定

- LINE_CHANNEL_ACCESS_TOKEN
- LINE_CHANNEL_SECRET
- OPENAI_API_KEY
