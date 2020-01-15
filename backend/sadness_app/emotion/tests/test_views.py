import ast
import json

import boto3
import emotion.config.setting as st
from django.utils import timezone
from django.utils.timezone import localtime
from emotion.models import AppUser, Image
from emotion.tests import factories
from rest_framework.test import APITestCase


class TestAnalizeImage(APITestCase):
    def test_get_success(self):
        """画像解析APIへのGETリクエスト（正常系） """

        target_url = "/api/analize"

        file = "TestAnalizeImage_Success.png"

        # テストデータ s3送信
        s3 = boto3.resource("s3")
        bucket = s3.Bucket(st.BUCKET_NAME)
        bucket.upload_file(f"emotion/tests/img/{file}", file)

        params = {
            "image" : file
        }

        response = self.client.get(target_url, params, format="json") 

        _response = ast.literal_eval(response.content.decode())      

        self.assertEqual(_response["code"], 1)
    
    def test_get_bad_request(self):
        """画像解析APIへのGETリクエスト（正常系） """

        target_url = "/api/analize"

        params = {
            "XXX" : "test"
        }

        response = self.client.get(target_url, params, format="json") 

        self.assertEqual(response.status_code, 400)



class TestImageListByUser(APITestCase):
    """ImageListByUser テストクラス """
        
    def test_get_success(self):
        """ユーザー別画像情報取得APIへのGETリクエスト（正常系） """

        # テストデータ作成
        factories.ImageFactory()

        user = AppUser.objects.get()
        image = Image.objects.get()

        target_url = f"/api/user/{user.id}/imageList"

        # API リクエストを実⾏ 
        response = self.client.get(target_url, format="json") 

        # データベースの状態を検証
        self.assertEqual(AppUser.objects.count(), 1)
        
        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 200)

        expected_json_dict = [
            {
                "id": image.id,
                "user": {
                    "id" : image.user.id,
                    "username" : image.user.username
                },
                "name": image.name,
                "score": image.score,
                "comment": image.comment,
                "created_at": str(localtime(image.created_at)).replace(" ", "T").replace("+00:00", "Z")
            }
        ]

        self.assertJSONEqual(str(response.content, encoding="utf8"), expected_json_dict) 


    def test_get_bad_request(self):
        """画像情報取得APIへのGETリクエスト（異常系） """

        target_url = "/api/user/999/imageList"

        # API リクエストを実⾏ 
        response = self.client.get(target_url, format="json") 
        _response = json.loads(str(response.content, encoding="utf8"))  

        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 200)


class TestImageList(APITestCase):
    """ImageList のテストクラス"""
    
    def test_get_success(self):
        """画像情報取得APIへのGETリクエスト（正常系） """

        target_url = "/api/imageList"

        # テストデータ作成
        factories.ImageFactory()

        #API リクエストを実⾏ 
        response = self.client.get(target_url, format="json") 

        #データベースの状態を検証
        self.assertEqual(Image.objects.count(), 1)
        
        #レスポンスの内容を検証
        self.assertEqual(response.status_code, 200)
        
        image = Image.objects.get()
        
        expected_json_dict = {
            "count": 1,
            "next": None,
            "previous": None,
            "results" : [
                {
                    "id": image.id,
                    "user": {
                        "id" : image.user.id,
                        "username" : image.user.username
                    },
                    "name": image.name,
                    "score": image.score,
                    "comment": image.comment,
                    "created_at": str(localtime(image.created_at)).replace(" ", "T").replace("+00:00", "Z"), 
                }
            ]
        }
        self.maxDiff = 1000
        self.assertJSONEqual(str(response.content, encoding="utf8"), expected_json_dict) 

class TestImageCreate(APITestCase):
    """ImageCreateテストクラス"""
    
    def test_create_success(self):
        """画像詳細登録APIへのGETリクエスト（正常系） """
        
        target_url = "/api/image/"

        params = {
            "user" : 1,
            "name" : "test.png",
            "score" : 50,
            "comment" : "test"
        }

        # テストデータ作成
        factories.AppUserFactory()

        #API リクエストを実⾏ 
        response = self.client.post(target_url, params, format="json") 
        
        #データベースの状態を検証
        self.assertEqual(Image.objects.count(), 1)
        
        #レスポンスの内容を検証
        self.assertEqual(response.status_code, 201)
        
        image = Image.objects.get()
        
        expected_json_dict = {
            "id": image.id,
            "user": "1",
            "name": image.name,
            "score": image.score,
            "comment": image.comment,
            "created_at": str(localtime(image.created_at)).replace(" ", "T").replace("+00:00", "Z"), 
        }
        self.maxDiff = 1000
        self.assertJSONEqual(str(response.content, encoding="utf8"), expected_json_dict) 
    
    def test_create_bad_request(self):
        """画像詳細登録APIへのGETリクエスト（異常系） """
        
        target_url = "/api/image/"

        params = {}

        # テストデータ作成
        factories.AppUserFactory()

        #API リクエストを実⾏ 
        response = self.client.post(target_url, params, format="json") 
        
        #データベースの状態を検証
        self.assertEqual(Image.objects.count(), 0)
        
        #レスポンスの内容を検証
        self.assertEqual(response.status_code, 400)

class TestImageDelete(APITestCase):
    """
    ImageDelete テストクラス
    """

    def test_delete_success(self):
        """画像削除APIへのDELETEリクエスト（正常系） """
        
        # テストデータ作成
        factories.ImageFactory()

        image = Image.objects.get()

        target_url = f"/api/image/{image.id}/delete"

        #API リクエストを実⾏ 
        response = self.client.delete(target_url, format="json") 

        #レスポンスの内容を検証
        self.assertEqual(response.status_code, 204)

        #データベースの状態を検証
        self.assertEqual(Image.objects.count(), 0)
    
    def test_delete_bad_request(self):
        """画像削除APIへのDELETEリクエスト（異常系） """
        
        target_url = f"/api/image/999/delete"

        #API リクエストを実⾏ 
        response = self.client.delete(target_url, format="json") 

        #レスポンスの内容を検証
        self.assertEqual(response.status_code, 404)

class TestUserCreate(APITestCase):
    """
    UserCreate テストクラス
    """

    def test_cleate_success(self):
        """ユーザー登録APIへのPOSTリクエスト（正常系） """
        
        target_url = f"/api/user/create"

        params = {
            "id": 1,
            "username": "test user"
        }

        #API リクエストを実⾏ 
        response = self.client.post(target_url, params, format="json") 

        #レスポンスの内容を検証
        self.assertEqual(response.status_code, 201)

        #データベースの状態を検証
        self.assertEqual(AppUser.objects.count(), 1)

        user = AppUser.objects.get()

        expected_json_dict = {
            "id": user.id,
            "username": user.username
        }

        self.assertJSONEqual(str(response.content, encoding="utf8"), expected_json_dict) 

    def test_cleate_bad_request(self):
        """ユーザー登録APIへのPOSTリクエスト（異常系） """
        
        target_url = f"/api/user/create"

        params = {
            "id": 1,
            "username": "",
            "icon": "http://XXXX/test.png",
            "displayname": "test user"
        }

        #API リクエストを実⾏ 
        response = self.client.post(target_url, params, format="json") 

        #レスポンスの内容を検証
        self.assertEqual(response.status_code, 400)

        #データベースの状態を検証
        self.assertEqual(AppUser.objects.count(), 0)

class TestUserGet(APITestCase):
    """
    UserGet テストクラス
    """

    def test_get_success(self):
        """ユーザー情報取得APIへのGETリクエスト（正常系） """

        factories.AppUserFactory()

        user = AppUser.objects.get()

        target_url = f"/api/user/{user.id}"

        #API リクエストを実⾏ 
        response = self.client.get(target_url, format="json") 

        #レスポンスの内容を検証
        self.assertEqual(response.status_code, 200)

        #データベースの状態を検証
        self.assertEqual(AppUser.objects.count(), 1)

        expected_json_dict = {
            "id": user.id,
            "username": user.username
        }

        self.assertJSONEqual(str(response.content, encoding="utf8"), expected_json_dict) 

    def test_cleate_bad_request(self):
        """ユーザー登録APIへのGETリクエスト（異常系） """
        
        target_url = f"/api/user/999"

        #API リクエストを実⾏ 
        response = self.client.get(target_url, format="json") 

        #レスポンスの内容を検証
        self.assertEqual(response.status_code, 404)

        #データベースの状態を検証
        self.assertEqual(AppUser.objects.count(), 0)

class TestUserUpdate(APITestCase):
    """
    UserUpdate テストクラス
    """

    def test_update_success(self):
        """ユーザー情報更新APIへのPUTリクエスト（正常系） """

        factories.AppUserFactory()

        user = AppUser.objects.get()

        target_url = f"/api/user/{user.id}/update"

        username = "test2"

        params = {
            "id": user.id,
            "username": username
        }

        #API リクエストを実⾏ 
        response = self.client.put(target_url, params, format="json") 

        #レスポンスの内容を検証
        self.assertEqual(response.status_code, 200)

        #データベースの状態を検証
        self.assertEqual(AppUser.objects.count(), 1)

        expected_json_dict = params

        self.assertJSONEqual(str(response.content, encoding="utf8"), expected_json_dict) 

    def test_update_bad_request(self):
        """ユーザー情報更新APIへのPUTリクエスト（異常系） """
        
        factories.AppUserFactory()

        user = AppUser.objects.get()

        target_url = f"/api/user/{user.id}/update"
        username = user.username
        params = {
            "id": user.id,
            "username": ""
        }

        #API リクエストを実⾏ 
        response = self.client.put(target_url, params, format="json") 

        #レスポンスの内容を検証
        self.assertEqual(response.status_code, 400)

        #データベースの状態を検証
        self.assertEqual(AppUser.objects.count(), 1)

        expected_json_dict = {
            "id": user.id,
            "username": user.username
        }

        self.assertEqual(user.username, username)
