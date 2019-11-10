# coding: utf-8
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import pagination
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from .models import Image
from .models import AppUser

from .serializer import ImageSerializer
from .serializer import ImageRegistSerializer
from .serializer import AppUserSerializer

from .service import face_reco
from .service import decode
from .exception.not_found_face_exception import NotFoundFaceException


class ImageListPagination(pagination.PageNumberPagination):
    page_size = 5

class ImageListByUserPagination(pagination.PageNumberPagination):
    page_size = 16

@api_view(['GET'])
def analize_image(request):
    """
    画像分析
    """

    try:
        img = request.query_params["img"]

        # 画像解析
        _result = face_reco.rekoginition_face(img)

        response = {
            "code": 1,
            "result" : _result
        }

        return Response(response)
    except NotFoundFaceException as e:
        # 顔が見つからなかったとき
        response = {
            "code": 2,
            "message": "Not Found Face" # TODO: 定数化する?
        }
        return Response(response)

    except Exception as e:
        # その他
        print(e)
        response = {
            "code": 3,
            "message": str(e)
        }
        return Response(response)

class ImageListByUser(generics.ListAPIView):    
    """´
    画像情報取得
    """
    serializer_class = ImageSerializer
    pagination_class = ImageListByUserPagination

    lookup_field = 'user'

    def get_queryset(self):

        user = self.kwargs['user']
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

    lookup_field = 'id'

class UserGet(generics.RetrieveAPIView):
    """
    ユーザー情報取得
    """
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer

    lookup_field = 'id'
