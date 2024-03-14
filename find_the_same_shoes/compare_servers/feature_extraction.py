import numpy as np
import cv2
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing import image

class ShoeFeatureExtractor:
    def __init__(self):
        # 加载预训练的ResNet50模型，不包括顶部的全连接层
        self.base_model = ResNet50(weights='imagenet', include_top=False)
        # 添加全局平均池化层以获得特征向量
        self.model = Model(inputs=self.base_model.input, outputs=self.base_model.output)

    def preprocess_image(self, img_array):
        """
        预处理图像，使其符合ResNet50的要求。
        """
        # 将图片缩放到模型期望的尺寸
        img_array_resized = cv2.resize(img_array, (224, 224))
        # 使用ResNet50的预处理函数
        img_array_preprocessed = preprocess_input(img_array_resized)
        return img_array_preprocessed

    def extract_features(self, img_array):
        """
        从给定的图片中提取特征。
        """
        img_array_preprocessed = self.preprocess_image(img_array)
        # 添加一个新的维度来符合模型的输入要求
        img_array_expanded = np.expand_dims(img_array_preprocessed, axis=0)
        features = self.model.predict(img_array_expanded)
        # 将特征向量展平
        features_flattened = features.flatten()
        return features_flattened

# 你可以像这样使用这个类
# extractor = ShoeFeatureExtractor()
# features = extractor.extract_features(your_cv2_image_array)
# 这里的 `your_cv2_image_array` 应该是一个通过cv2读取的图片数组
