# coding: utf-8

import boto3

import emotion.config.setting as st
from emotion.exception.not_found_face_exception import NotFoundFaceException


def rekoginition_face(image):
    """
    face_rekoginitionAPIで画像を解析する。


    Parameters
    ----------
    image_path : str
        ファイルパス

    Returns
    -------
    result : dict
        解析結果
    """

    try:
        print("==  rekoginition_face start==")
        
        BUCKET= st.BUCKET_NAME
        client = boto3.client('rekognition','ap-northeast-1')
        response = client.detect_faces(Image={'S3Object': {'Bucket': BUCKET, 'Name': image}}, Attributes=['ALL'])

        details = response["FaceDetails"]

        # 解析に失敗した場合。
        if len(details) == 0:
            raise NotFoundFaceException

        # 解析結果
        results = []
        
        for detail in details:
            result = {}
            emotions = [emotion for emotion in detail["Emotions"]]

            for emotion in emotions:
                if emotion["Type"] == "SAD":
                    # 得点
                    score = int(emotion["Confidence"])
                    result["score"] = score

            # 画像形成
            result["file"] = image
            results.append(result)
            result["boundingBox"] = detail["BoundingBox"]
        
        print("==  rekoginition_face end==")

        return results

    except NotFoundFaceException as e:
        print("== Invalid_image_exception ==")
        print("==  rekoginition_face end==")

        raise e


    except Exception as e:
        print("==  rekoginition_face end==")

        raise e
