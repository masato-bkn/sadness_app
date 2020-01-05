from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now
from rest_framework.permissions import IsAuthenticated


class UserManager(BaseUserManager):
    """
    ユーザーマネージャー
    """

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        is_staff(管理サイトにログインできるか)と、is_superuer(全ての権限)をFalseに
        """
        extra_fields.setdefault('is_staff', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        スーパーユーザーは、is_staffとis_superuserをTrueに
        """
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    ユーザーモデル
    """
    permission_classes = (IsAuthenticated,)

    # ユーザー名
    username = models.CharField(max_length=30, unique=True)
    # メールアドレス
    email = models.EmailField(unique=True)
    
    # ログイン判定
    is_active = models.BooleanField(default=True)
    
    # 管理者ページにログインできるか
    is_staff = models.BooleanField(default=False)
    
    # 権限があるか
    is_superuser = models.BooleanField(default=True)

    # 登録日時
    created_at = models.DateTimeField(default=now)
    # 更新日時
    updated_at = models.DateTimeField(auto_now=True)

    # 何これ?? これつけないとエラーになる
    USERNAME_FIELD = 'username' 
    REQUIRED_FIELDS = ['email']

    # ? カスタムユーザを使用する時にはManagerを使う必要があるらしい
    objects = UserManager()


class AppUser(models.Model):
    """
    ユーザーモデル
    """
    # firebase認証で発行されたID
    id = models.CharField(primary_key=True, max_length=255)
    # ユーザー名
    username = models.CharField(max_length=255)
    # ディスプレイ名
    displayname = models.CharField(max_length=255)
    # アイコン
    icon = models.CharField(max_length=255)
    # 登録日時
    created_at = models.DateTimeField(default=now)
    # 更新日時
    updated_at = models.DateTimeField(auto_now=True)

class Image(models.Model):
    """
    画像モデル
    """

    # ファイル名
    name = models.CharField(max_length=255)
    # 得点
    score = models.IntegerField(max_length=3)
    # コメント
    comment = models.CharField(max_length=20)
    # ユーザー
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    # 登録日時
    created_at = models.DateTimeField(default=now)
    # 更新日時
    updated_at = models.DateTimeField(auto_now=True)
