import socket
import json
from datetime import datetime
import os
import base64

class Communication():
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("0.0.0.0", 11013))
        self.socket.listen(5)
        print("Waiting for client connection...")
        self.conn, self.addr = self.socket.accept()
        print(f"Connected to {self.addr}")
        self._senddatalist = []

    def send(self, id, timestamp, image_data, devicename):
    # def send(self, id, timestamp, devicename):

        packet = {
            "id": id,
            "time": timestamp,
            "imageData": base64.b64encode(image_data).decode('utf-8'),  # base64 인코
        }
        json_data = json.dumps(packet) + '\n'  # 패킷 구분을 위한 '\n' 추가

        self.conn.send(json_data.encode('utf-8'))

        # 패킷 저장
        self._senddatalist.append(packet)

        self.data_to_json(devicename)

        print(f"send id {id}")

    def data_to_json(self, devicename):
        filename = f"{devicename}.json"
        
        # 파일에 새 데이터를 덮어쓰기
        with open(filename, 'w') as json_file:
            json.dump(self._senddatalist, json_file, indent=1)

    def close(self):
        self.conn.close()
        self.socket.close()

    
    def time(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # 밀리초 포함
