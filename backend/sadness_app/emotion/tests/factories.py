# coding: utf-8
import factory
from django.utils import timezone
from emotion import models


class AppUserFactory(factory.django.DjangoModelFactory):
    """
    AppUser Factory
    """

    # firebase認証で発行されたID
    id = 1
    # ユーザー名
    username = "test user"
    # ディスプレイネーム
    displayName = "Test User"
    # アイコン
    icon = "http://XXXX.png"
    # 登録日時
    created_at = timezone.now()
    # 更新日時
    updated_at = timezone.now()

    class Meta:
        model = models.AppUser

class ImageFactory(factory.django.DjangoModelFactory):
    """
    Image Factory
    """

    # ファイル名
    name = "test.png"
    # 得点
    score = 50
    # コメント
    comment = "test"
    # ユーザー
    user = factory.SubFactory(AppUserFactory)
    # 登録日時
    created_at = timezone.now()
    # 更新日時
    updated_at = timezone.now()

    class Meta:
        model = models.Image
