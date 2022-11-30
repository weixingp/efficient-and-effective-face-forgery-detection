import random

import cv2
import torch.nn as nn
import torch
from facenet_pytorch import InceptionResnetV1, fixed_image_standardization
from PIL import Image
from torchvision import transforms
import numpy as np
from facenet_pytorch import MTCNN


class FaceRecognitionCNN(nn.Module):
    def __init__(self):
        super(FaceRecognitionCNN, self).__init__()
        self.resnet = InceptionResnetV1(pretrained='vggface2')
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.5)
        self.fc = nn.Linear(512, 1)

    def forward(self, images):
        out = self.resnet(images)
        out = self.relu(out)
        out = self.dropout(out)
        out = self.fc(out)
        return out.squeeze()


class FaceForgeryDetector:

    def __init__(self, model_path="./model.pth", gpu=False):
        device_name = "cuda" if gpu else "cpu"
        self.device = torch.device(device_name)
        self.model = torch.load(model_path, map_location=self.device)

        self.transform = transforms.Compose([
            transforms.Resize((160, 160)),
            np.float32,
            transforms.ToTensor(),
            fixed_image_standardization
        ])

        self.face_detector = MTCNN(device=self.device, margin=16, select_largest=True)
        self.face_detector.eval()

    def load_image(self, image_path):
        """
        Load a single image into tensor format
        :return: A single tensor
        """
        image = Image.open(image_path)
        image = self.face_detector(image)  # Extract faces
        # transformed_image = self.transform(image)
        # transformed_image = transformed_image.to(self.device)
        return image.to(self.device)

    def extract_faces(self, video, count=100):
        """
        Extract faces from a video
        :param count: number of faces to extract
        :param video: the video
        :return: List of faces extracted, in tensor
        """
        print("extracting...")
        length = video.frame_cnt
        ids = random.sample(range(length), min(count, length))
        image_list = []

        for index in ids:
            image = Image.fromarray(cv2.cvtColor(video[index], cv2.COLOR_BGR2RGB))
            face = self.face_detector(image)
            # face = self.transform(image)
            if face is None:
                continue

            image_list.append(face.to(self.device))

        return image_list

    def predict(self, image_list):
        """
        Predict the image
        :param image_list: List of tensors of images
        :return: The label, 1 -> Real, 0 -> Fake
        """
        outputs = []
        with torch.no_grad():
            for item in image_list:
                image = item.unsqueeze(0)
                outputs.append(self.model(image))

        predictions = []
        for item in outputs:
            pred = 0 if item > 0.0 else 1
            predictions.append(pred)

        return predictions
