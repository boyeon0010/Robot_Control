import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

# 포인트 좌표
points = [(0, 0, 0), (32, 0, 80), (32, 0, 188), (182, 0, 198), (207, 0, 198)]

# 각 포인트를 x, y, z로 분리
x = [point[0] for point in points]
y = [point[1] for point in points]
z = [point[2] for point in points]

# 3D 그래프 생성
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 각 포인트를 그래프에 플로팅
ax.scatter(x, y, z, c='r', marker='o')

# 포인트들을 선으로 연결하여 플로팅
for i in range(len(points) - 1):
    ax.plot([points[i][0], points[i + 1][0]], 
            [points[i][1], points[i + 1][1]], 
            [points[i][2], points[i + 1][2]], 'b-')

# 각 선에 길이를 작성
for i in range(len(points) - 1):
    length = np.linalg.norm(np.array(points[i]) - np.array(points[i + 1]))
    ax.text((points[i][0] + points[i + 1][0]) / 2,
            (points[i][1] + points[i + 1][1]) / 2,
            (points[i][2] + points[i + 1][2]) / 2,
            f'{length:.2f}', color='green')

# 각 축의 라벨 설정
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

# 그래프 출력
plt.show()
