# 関数 URL の Bedrock エンドポイント化

関数 URL を使って、Boto3 の Bedrock のエンドポイントを独自に作成するプロジェクトです。
エンドポイントは IAM 認証されます。

設定した IAM 認証は、python-client/patch_credentials_scope.py を boto3.client にあてることで超えることができます。

## デプロイ

以下のコマンドを実行して、cdk でプロジェクトをデプロイします  
リージョンは us-east-1 にデプロイされます

```
cdk deploy
```

## 実行の前に

デプロイした作成された関数 URL を、python-client/endpoint_url.py に設定します

```python
ENDPOINT_URL = "https://xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.lambda-url.us-east-1.on.aws/"

```

## boto3 で実行する

python-client のディレクトリで、以下のコマンドを実行します

Titan を実行します

```
python app.py
```

Claude Haiku を実行します

```
python app-claude.py
```

オリジナルのモデル ID を実行します

```
python app.hal.py
```
