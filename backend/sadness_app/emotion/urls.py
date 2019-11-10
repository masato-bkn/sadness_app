# coding: utf-8
from django.urls import path
from emotion import views


urlpatterns = [
    # 画像分析
    path('analize', views.analize_image),
    # 画像情報登録
    path('image/', views.ImageCreate().as_view()),
    # 画像情報取得
    path('imageList', views.ImageList().as_view()),
    # 画像削除
    path('image/<int:id>/delete',views.ImageDelete().as_view()),
    # ユーザー別画像情報取得
    path('user/<str:user>/imageList', views.ImageListByUser().as_view()),
    # ユーザー情報取得
    path('user/create',views.UserCreate().as_view()),
    # ユーザー情報取得
    path('user/<str:id>',views.UserGet().as_view()),
    # ユーザー情報更新
    path('user/<str:id>/update',views.UserUpdate.as_view()),    
]
