from pyevsim import BehaviorModelExecutor, Infinite, SysMessage
import time
import cv2
import json
from config import *


class SendImageToUnity(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, device_class, conn):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.conn = conn
        
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Generate",0)

        self.insert_input_port("start")

        self.jsonfile_path = DEVICE_PATH
        self.jsone_nane = engine_name

        self.device_class = device_class
        self.camera = self.device_class.Camera_return()
        self.is_streaming = False  # 스트리밍 상태 관리를 위한 플래그
        self.frame_rate = 1/30  # 30 FPS에 해당하는 시간 간격
        self.count = 0
 
    def ext_trans(self, port, msg):
        if port == "start":
            print("Data class in")
            # self.camera.start_video_stream(display=False)
            self._cur_state = "Generate"

    def output(self):
        if self._cur_state == "Generate":
            start_time = time.time()
            self.image_data = self.camera.read_cv2_image(strategy="newest")  # 카메라에서 이미지 데이터 받기
            img = cv2.resize(self.image_data, (480, 300))  # 해상도를 640x480이 제일 적당함
            encoded_image = self.convert_image_to_bytes(img)
            
            self.conn.send(self.count, self.conn.time(), encoded_image, self.jsone_nane)
            # self.conn.send(self.count, self.conn.time(), self.jsone_nane)
            self.count += 1
            end_time = time.time()
            elapsed_time = end_time - start_time
            time_to_wait = self.frame_rate - elapsed_time

            if time_to_wait > 0:
                time.sleep(time_to_wait)  # 프레임 레이트를 맞추기 위해 대기
            

    def int_trans(self):
        if self._cur_state == "Generate":
            self._cur_state = "Generate"


    def convert_image_to_bytes(self,image_data):
        # 이미지를 PNG 형식으로 메모리 버퍼에 인코딩
        success, encoded_image = cv2.imencode('.png', image_data)
        if success:
            # 성공적으로 인코딩된 경우, 바이트 데이터를 반환
            return encoded_image.tobytes()
        else:
            # 인코딩 실패 시, None 반환
            return None

    