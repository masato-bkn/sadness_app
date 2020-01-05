# coding: utf-8

import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# 画像解析用バケット
BUCKET_NAME = os.environ.get('BUCKET_NAME')
# 画像解析用バケット URL
S3_URL = os.environ.get('S3_URL')