import numpy as np
import cv2

class MyImage:
    def __init__(self, path):
        self.path = path
        self.format = self.get_format()
        self.content = self.get_content()

    def get_format(self):
        # 获取文件格式
        return self.path.split('.')[-1]

    def get_content(self):
        # 读取图像内容为numpy数组
        image = cv2.imread(self.path)
        if image is not None:
            return image
        else:
            raise FileNotFoundError(f"Unable to read image at {self.path}")

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, new_content):
        # 设置图像内容，并同时更新相关属性
        self._content = new_content
        #self.format = self.get_format()


    @property
    def width(self):
        # 返回图像宽度
        return self.content.shape[1] if self.content is not None else None

    @property
    def height(self):
        # 返回图像高度
        return self.content.shape[0] if self.content is not None else None

    @property
    def size(self):
        # 返回图像尺寸
        return (self.width, self.height)

    @property
    def channels(self):
        # 返回图像通道数
        return self.content.shape[2] if self.content is not None and len(self.content.shape) > 2 else None

    @property
    def shape(self):
        # 返回图像形状
        return self.content.shape[0], self.content.shape[1] if self.content is not None else None


       