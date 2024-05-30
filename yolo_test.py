import torch
from PIL import Image
import matplotlib.pyplot as plt

# YOLOv5 모델 로드 (로컬 경로 사용)
model = torch.hub.load('./yolov5', 'custom', path='yolov5s.pt', source='local')

# 이미지 로드
img_path = '2.jpg'
img = Image.open(img_path)

# 탐지 임계값 조정 (기본값은 0.25)
# model.conf = 0.03  # 탐지 임계값을 낮추어 더 많은 객체를 탐지
model.conf = 0.25
# 객체 탐지 수행
results = model(img)

# 탐지된 객체 정보 출력 및 저장
results.print()  # 탐지된 객체 정보 출력
# results.save(save_dir='/mnt/data/')  # 결과 이미지를 저장합니다.
results.show()  # 결과를 시각적으로 보여줍니다.

# 탐지된 객체의 이미지 출력
img_result = plt.imread('/mnt/data/1.jpg')
plt.imshow(img_result)
plt.show()