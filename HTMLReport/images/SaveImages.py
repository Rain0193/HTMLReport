import base64
import os
import random
import threading
import time

report_path = ""
imageList = {}


def AddImage(base64_data: base64, alt="", name: str = "image"):
    """添加截图到报告

    :param base64_data:base64格式的图片文本
    :param alt:图片提示
    :param name:图片命名前缀
    :return:None
    """
    if base64_data and report_path:
        current_id = str(threading.current_thread().ident)
        if current_id not in imageList:
            imageList[current_id] = []

        random_name = '{}_{}_{}_{}.jpg'.format(name, current_id, time.strftime('%Y_%m_%d_%H_%M_%S'),
                                               random.randint(1, 999))

        image_path = os.path.join(report_path, "images")
        if not os.path.exists(image_path):
            os.makedirs(image_path)

        image_file = os.path.join(image_path, random_name)
        with open(image_file, "wb") as f:
            f.write(base64.b64decode(base64_data))
            imageList[current_id].append((os.path.join('images', random_name).replace("\\", "/"), alt))
