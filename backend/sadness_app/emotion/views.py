# coding: utf-8
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
            "message": "Not Found Face" # TODO: 定数化する?
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
