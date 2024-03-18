import os
import cv2
import numpy as np
from find_the_same_shoes.log.log_decorator import logger, log_exceptions_and_info
from find_the_same_shoes.models import MyImage
import requests
from PIL import Image
from io import BytesIO
from find_the_same_shoes.config.get_config import read_yaml_file
config_info = read_yaml_file()


class ImagePreprocessor:
    """用于归一化的类
    """    
    def __init__(self):
        pass


    @log_exceptions_and_info(logger)        
    def resize_image(self, image1_path, image2_path):
        """归一化尺寸
        - 如果尺寸差距在10%以内，则将较大的图片边缘切去10%。
        - 如果差距超过10%，则不做处理。

        暂时用不到了

        Args:
            image1_path (str): 第一张图片
            image2_path (str): 第二张图片

        Returns:
            Image: _description_
        """        
        # 转化为cv2对象
        image1 = MyImage(image1_path)
        image2 = MyImage(image2_path)
        # print(image2.content.shape)

        # 获取两张图片的尺寸
        height1, width1 = image1.shape
        height2, width2 = image2.shape
        """ print("start", height1, width1)
        print("start", height2, width2) """

        # 计算尺寸差距百分比
        height_diff = abs(height1 - height2) / max(height1, height2)
        width_diff = abs(width1 - width2) / max(width1, width2)
        # print(height_diff, width_diff)

        # 判断尺寸差距是否在10%以内
        if height_diff * width_diff <= 0.1:
            # 选取较大图片进行缩放
            if height1*width1 > height2*width2:
                image1 = self._trim_edges(image1)
            elif height1*width1 < height2*width2:
                image2 = self._trim_edges(image2)
            else:
                # image2 = self._trim_edges(image2)
                # print(image2.content.shape)
                pass

            height1, width1 = image1.shape
            height2, width2 = image2.shape
            """ print(height1, width1)
            print(height2, width2)    """    
           
        else:
            return False

        return image1, image2
    

    def _trim_edges(self, image: Image):
        """将图片最外围一圈截除，使其面积为原来的90%

        Args:
            image (Image): 图片对象，Numpy数组

        Returns:
            array: 调整后的图片
        """        
        height, width = image.shape
        original_area = height * width
        new_area = original_area * 0.9

        # 计算原始图片和新图片的高度和宽度比例
        ratio = (original_area / new_area) ** 0.5

        # 计算要删除的边缘宽度
        height_diff = int((height - height / ratio) / 4)
        width_diff = int((width - width / ratio) / 4)

        content = image.content
        #print(content.shape)
        new_content = content[height_diff:height-height_diff, width_diff:width-width_diff]
        #print(new_content.shape)
        # 截取图片
        image.content = new_content
        return image


    @log_exceptions_and_info(logger) 
    def remove_background(self, file_path):
        """
        背景移除
        调用外部API来实现背景移除。
        """

        # 上传图像文件
        with open(file_path, "rb") as file:
            files = {"file": (file_path, file, "image/jpeg")}
            response = requests.post(config_info["rmbg_server_add"], files=files)

        # 检查响应是否成功
        if response.status_code == 200:
            # 从响应中获取图像数据并保存为图片文件
            image_bytes = BytesIO(response.content)
            image = Image.open(image_bytes)
            # 路径配置文件化
            # TODO
            image.save(f"{config_info['pic_without_bg_folder']}/{os.path.basename(file_path)}.png")
            return True
        else:
            print("请求失败:", response.text)
            return False
