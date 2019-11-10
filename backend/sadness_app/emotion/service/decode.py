import base64
import cv2
import numpy as np

def decode_img(file_name, encoded):
    img_binary = base64.b64decode(encoded)
    jpg=np.frombuffer(img_binary,dtype=np.uint8)

    img = cv2.imdecode(jpg, cv2.IMREAD_COLOR)

    cv2.imwrite(f"emotion/img/{file_name}", img)
