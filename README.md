## 概要
人の顔を解析して悲しみを点数化するWebアプリ「[THE SADNESS](sadness.ml)」のリポジトリです。

## 機能
- ログイン/ログアウト(twitter認証)
- 画像解析
- 画像投稿
- 画像削除
- ユーザー投稿画像一覧
- ログインユーザー投稿画像一覧
- ユーザーのtwitterアカウントへ遷移(ユーザー投稿画像一覧のユーザー名押下で遷移)

***スマホで使用する際は、Chromeにてご確認ください。:bow:**

<br>

1. 画像解析 -> 登録

![1](https://github.com/masato-bkn/sadness_app/blob/img/%E7%94%BB%E5%83%8F%E8%A7%A3%E6%9E%90.gif)

2. ユーザー投稿画像一覧 -> ユーザー投稿画像一覧 -> 削除

![2](https://github.com/masato-bkn/sadness_app/blob/img/%E5%89%8A%E9%99%A4_%E4%B8%80%E8%A6%A7.gif)

3. ユーザー投稿画像一覧(スマホ)

<img src="https://github.com/masato-bkn/sadness_app/blob/img/%E4%B8%80%E8%A6%A7(%E3%82%B9%E3%83%9E%E3%83%9B).gif" width="200px" style="margin: 80px;">




## Architecture
■ Front
- Nuxt
- scss
- Bootstrap
 
■ Back
- python
- Django(DRF)
- wsgi

■ インフラ
- EC2
- CloudFront
- RDS(MySQL)
- S3
- Rekognition
- Route53
- Nginx
- wsgi
- Firebase(SNS認証)

■ その他
- Eslint
- Prettier

■ 構成図
![Architecture](https://github.com/masato-bkn/sadness_app/blob/img/architecture.png)

■ 残対応
- フロント側のテストコード作成
- 自動デプロイ導入

### サンプル画像
以下の画像で本アプリ全ての画像評価パターンが試せます。

1.最高評価

<img src="https://github.com/masato-bkn/sadness_app/blob/img/greatSadness.png" width="200px" style="display: inline; margin: 80px;">

2.複数顔有り①

<img src="https://github.com/masato-bkn/sadness_app/blob/img/manyFaces1.png" width="200px" style="margin: 80px;">

3.複数顔有り②

<img src="https://github.com/masato-bkn/sadness_app/blob/img/manyFaces2.png" width="250px" style="margin: 80px;">

4.顔なし

<img src="https://github.com/masato-bkn/sadness_app/blob/img/noFace.png" width="200px" style="margin: 80px;">



