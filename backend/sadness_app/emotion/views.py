# coding: utf-8
import base64

import boto3
from rest_framework import generics, pagination, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .exception.not_found_face_exception import NotFoundFaceException
from .models import AppUser, Image
from .serializer import (AppUserSerializer, ImageRegistSerializer,
                         ImageSerializer)
from .service import face_reco


class ImageListPagination(pagination.PageNumberPagination):
    page_size = 5

@api_view(["POST"])
def upload_image(request):
    """
    画像解析
    """

    try:

        check_elements = ["data","name","bucket"]

        for element in check_elements:
            if element not in request.data:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        data = request.data["data"]
        file_name = request.data["name"]
        bucket = request.data["bucket"]

        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket)

        bucket.put_object(
            Key=file_name,
            Body=base64.b64decode(data),
            ContentType='image/png'
        )

        response = {
            "code" : 1,
            "name" : file_name
        }
        
        return Response(response)

    except Exception as e:
        # upload失敗
        response = {
            "code" : 2
        }

        Response(response)


@api_view(["GET"])
def analize_image(request):
    """
    画像解析
    """

    try:
        if "image" not in request.query_params:
            return Response(status=status.HTTP_400_BAD_REQUEST)
            
        image = request.query_params["image"]
            
        # 画像解析
        _result = face_reco.rekoginition_face(image)

        response = {
            "code": 1,
            "result" : _result
        }

        return Response(response)
    except NotFoundFaceException as e:
        # 顔が見つからなかったとき
        response = {
            "code": 2,
            "message": "Not Found Face"
        }
        return Response(response)

    except Exception as e:
        # その他
        response = {
            "code": 3,
            "message": str(e)
        }
        Response(response)

class ImageListByUser(generics.ListAPIView):    
    """´
    画像情報取得
    """
    serializer_class = ImageSerializer

    lookup_field = "user"

    def get_queryset(self):

        user = self.kwargs["user"]
        return Image.objects.filter(user=user)


class ImageList(generics.ListAPIView):
     """´
     画像情報取得
     """
     serializer_class = ImageSerializer
     queryset = Image.objects.all().order_by("score").reverse()

     pagination_class = ImageListPagination        
     

class ImageCreate(generics.CreateAPIView):
    """
    画像詳細登録
    """
    queryset = Image.objects.all()
    serializer_class = ImageRegistSerializer


class ImageDelete(generics.DestroyAPIView):
    """
    画像削除
    """
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    lookup_field = "id"


class UserCreate(generics.CreateAPIView):
    """
    ユーザー登録
    """
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer


class UserUpdate(generics.UpdateAPIView):
    """
    ユーザー更新
    """
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer

    lookup_field = "id"

class UserGet(generics.RetrieveAPIView):
    """
    ユーザー情報取得
    """
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer

    lookup_field = "id"
