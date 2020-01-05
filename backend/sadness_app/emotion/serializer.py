# coding: utf-8

from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from .models import AppUser
from .models import Image

from django.contrib.auth.hashers import make_password


class AppUserSerializer(serializers.ModelSerializer):
    """
    ユーザー情報
    """

    class Meta:
        model = AppUser
        fields = ('id','username','displayname','icon')

class ImageRegistSerializer(serializers.ModelSerializer):
    """
    画像登録
    """
    user = serializers.PrimaryKeyRelatedField(queryset=AppUser.objects.all())

    class Meta:
        model = Image
        fields = ('id','user','name', 'score', 'comment', 'created_at')
        read_only_field = ('user')


class ImageSerializer(serializers.ModelSerializer):
    """
    画像一覧取得
    """
    user = AppUserSerializer()

    class Meta:
        model = Image
        fields = ('id','user','name', 'score', 'comment', 'created_at')
        read_only_field = ('user')

