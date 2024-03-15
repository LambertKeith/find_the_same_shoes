import cv2
import numpy as np
from find_the_same_shoes.log.log_decorator import logger, log_exceptions_and_info
from find_the_same_shoes.models import Image


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

        Args:
            image1_path (str): 第一张图片
            image2_path (str): 第二张图片

        Returns:
            Image: _description_
        """        
        # 转化为cv2对象
        image1 = Image(image1_path)
        image2 = Image(image2_path)
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
    def remove_background(self, image):
        """
        背景移除 - 模拟方法
        在实际应用中，这个方法应该被替换为调用外部API来实现背景移除。
        """
        # 这里仅提供一个示例框架，具体实现应调用外部API
        # 假设结果是一个将背景替换为白色的图片
        # 这部分代码需要根据实际API进行修改
        
        placeholder_image = np.full_like(image, 255) # 创建一个全白的图片
        # TODO

        
        return placeholder_image

# 示例用法
# 加载图片（替换为实际路径）
# image1 = cv2.imread('path_to_image1.jpg')
# image2 = cv2.imread('path_to_image2.jpg')

# preprocessor = ImagePreprocessor()
# resized_image1, resized_image2 = preprocessor.resize_image(image1, image2)
# background_removed_image = preprocessor.remove_background(resized_image1)
