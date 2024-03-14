import numpy as np
import cv2

class Image:
    """图片模型
    """    
    def __init__(self, path):
        self.path = path
        self.format = self.get_format()
        self.content = self.get_content()

    def get_format(self):
        """获得图片后缀
        Returns:
            str: _description_
        """        
        # 获取文件格式
        return self.path.split('.')[-1]

    def get_content(self):
        '''读取图像内容为numpy数组
        '''

        image = cv2.imread(self.path)
        if image is not None:
            return image
        else:
            raise FileNotFoundError(f"Unable to read image at {self.path}")

    def display(self):
        # 显示图像
        cv2.imshow("Image", self.content)
        cv2.waitKey(0)
        cv2.destroyAllWindows()



        