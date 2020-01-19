from django.test import TestCase
from django.utils import timezone
from emotion.models import AppUser, Image
from emotion.serializer import AppUserSerializer, ImageRegistSerializer, ImageSerializer
from emotion.tests import factories

class TestAppUserSerializer(TestCase):
    """AppUserSerializer テストクラス"""
    
    def test_input_valid(self):
        """⼊⼒データのバリデーション （OK） """
        #シリアライザを作成
        input_data = {
            'id': 'aaa',
            'username' : 'test user',
            'displayName' : 'Test User',
            'icon' : 'http:XXXX.png'
        }
        
        serializer = AppUserSerializer(data=input_data)
        
        #バリデーションの結果を検証 
        self.assertEqual(serializer.is_valid(), True) 
    
    def test_input_invalid_if_title_is_blank(self):
        """⼊⼒データのバリデーション （NG： username が空⽂字） """
        #シリアライザを作成
        input_data = {
            'id': '1',
            'username': '',
            'displayName' : 'Test User',
            'icon' : 'http:XXXX.png'
        }
        serializer = AppUserSerializer(data=input_data)
        
        #バリデーションの結果を検証
        self.assertEqual(serializer.is_valid(), False)
        self.assertCountEqual(serializer.errors.keys(), ['username'])
        self.assertCountEqual(
            [x.code for x in serializer.errors['username']],['blank'],
        ) 

class TestImageRegistSerializer(TestCase):
    """ImageRegistSerializer テストクラス"""
    
    def test_input_valid(self):
        """⼊⼒データのバリデーション （OK） """
        #シリアライザを作成
        input_data = {
            'id' :'1',
            'user' : 1,
            'name': 'test.png',
            'score' : 50,
            'comment': 'test',
            'created_at' : timezone.now()
        }

        factories.AppUserFactory()

        # ユーザーデータ作成
        serializer = ImageRegistSerializer(data=input_data)

        #バリデーションの結果を検証 
        self.assertEqual(serializer.is_valid(), True) 

class TestImageSerializer(TestCase):
    """ImageRegistSerializer テストクラス"""
    
    def test_input_valid(self):
        """⼊⼒データのバリデーション （OK） """
        #シリアライザを作成
        input_data = {
            'id' :'1',
            'user' : {
                'id': '1',
                'username': 'test user',
                'displayName' : 'Test User',
                'icon' : 'http:XXXX.png'
            },
            'name': 'test.png',
            'score' : 50,
            'comment': 'test',
            'created_at' : timezone.now()
        }
        
        serializer = ImageSerializer(data=input_data)

        #バリデーションの結果を検証 
        self.assertEqual(serializer.is_valid(), True)
           
