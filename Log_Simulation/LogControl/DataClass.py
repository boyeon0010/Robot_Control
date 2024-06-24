from pyevsim import BehaviorModelExecutor, Infinite, SysMessage
from datetime import datetime as dt
import json
import os



class DataClassModel(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Generate",1)
        self.insert_state("Next_D",1)
        self.insert_state("Next_W",1)

        self.insert_input_port("start")
        self.insert_input_port("next")

        self.insert_output_port("image_data")

        self.count_ = 0
 
    def ext_trans(self, port, msg):
        if port == "start":
            print("Data class in")
            self._cur_state = "Generate"
        
        if port == "next":
            self.w_count= msg.retrieve()[0][1]
            self.action_data = msg.retrieve()[0][0]
            print(f"next data class in ~~~~~~~~~~~")
            if self.action_data == "W":
                print(f"self.w_count {self.w_count}")
                self._cur_state = "Next_W"
            elif self.action_data == "D":
                self._cur_state = "Next_D"

    def output(self):
        if self._cur_state == "Generate":
            
            msg = SysMessage(self.get_name(), "image_data")
            # 현재 작업 디렉토리 출력
            print("현재 디렉토리:", os.getcwd())
            msg.insert([self.extract_images_post_before_w("LogControl/RobomasterControl/RobomasterrWS2.json","LogControl/RobomasterImage/RobomastersWS2.json")])
            self.action_data = None
            return msg
                
        if self._cur_state == "Next_W":
            print(f"self.w_count {self.w_count}")
            msg = SysMessage(self.get_name(), "image_data")
            if self.w_count <= 1:
                w1 = self.extract_images_post_w("LogControl/RobomasterControl/RobomasterrWS2.json","LogControl/RobomasterImage/RobomastersWS2.json")
                msg.insert([w1])
                self.action_data = None
            else:
                w2 = self.extract_images_post_w("LogControl/RobomasterControl/RobomasterrWS6.json","LogControl/RobomasterImage/RobomastersWS6.json")
                msg.insert([w2])
            return msg
        
        if self._cur_state == "Next_D":

            msg = SysMessage(self.get_name(), "image_data")
            d = self.extract_images_between_last_d_and_next_command("LogControl/RobomasterControl/RobomasterrAD3.json","LogControl/RobomasterImage/RobomastersAD3.json")
            msg.insert([d])
            self.action_data = None
            return msg

    def int_trans(self):
        if self._cur_state == "Generate":
            self._cur_state = "Wait"
        if self._cur_state == "Next_W":
            self._cur_state = "Wait"
        if self._cur_state == "Next_D":
            self._cur_state = "Wait"


    def extract_images_post_w(self,input_json_path, image_json_path):
        # 입력 JSON 로딩
        with open(input_json_path, 'r') as file:
            actions = json.load(file)

        # 'W' 명령이 입력된 시간 찾기
        w_times = []
        for action in actions:
            if action['action'] == 'W':
                time_str = action['time']
                # '오후'가 있으면 12시간을 더하고, '오전'이면 그대로 사용
                if '오후' in time_str:
                    hour_time = dt.strptime(time_str, "%Y-%m-%d 오후 %H:%M:%S")
                    hour_time = hour_time.replace(hour=(hour_time.hour % 12) + 12)
                else:
                    hour_time = dt.strptime(time_str, "%Y-%m-%d 오전 %H:%M:%S")
                w_times.append(hour_time)
        
        
        # 이미지 JSON 로딩
        with open(image_json_path, 'r') as file:
            images = json.load(file)

        # 필요한 이미지 데이터 추출
        results = []
        for w_time in w_times:
            for image in images:
                image_time = dt.strptime(image['time'], "%Y-%m-%d %H:%M:%S.%f")
                if image_time > w_time:
                    results.append(image['imageData'])

        return results
    
    def extract_images_post_before_w(self,input_json_path, image_json_path):
        # 입력 JSON 로딩
        with open(input_json_path, 'r') as file:
            actions = json.load(file)

        # 'W' 명령이 입력된 시간 찾기
        w_times = []
        for action in actions:
            if action['action'] == 'W':
                time_str = action['time']
                # '오후'가 있으면 12시간을 더하고, '오전'이면 그대로 사용
                if '오후' in time_str:
                    hour_time = dt.strptime(time_str, "%Y-%m-%d 오후 %H:%M:%S")
                    hour_time = hour_time.replace(hour=(hour_time.hour % 12) + 12)
                else:
                    hour_time = dt.strptime(time_str, "%Y-%m-%d 오전 %H:%M:%S")
                w_times.append(hour_time)
        
        
        # 이미지 JSON 로딩
        with open(image_json_path, 'r') as file:
            images = json.load(file)

        # 필요한 이미지 데이터 추출
        results = []
        for w_time in w_times:
            for image in images:
                image_time = dt.strptime(image['time'], "%Y-%m-%d %H:%M:%S.%f")
                if image_time < w_time:
                    results.append(image['imageData'])

        return results
        

    
    def extract_images_between_last_d_and_next_command(self, input_json_path, image_json_path):
        # 입력 JSON 로딩
        with open(input_json_path, 'r') as file:
            actions = json.load(file)

        # 'D' 명령과 다른 명령의 시간 찾기
        last_d_time = None
        post_d_command_time = None
        for action in reversed(actions):
            time_str = action['time']
            # '오후'가 있으면 12시간을 더하고, '오전'이면 그대로 사용
            if '오후' in time_str:
                action_time = dt.strptime(time_str, "%Y-%m-%d 오후 %I:%M:%S")
                action_time = action_time.replace(hour=(action_time.hour % 12) + 12)
            else:
                action_time = dt.strptime(time_str, "%Y-%m-%d 오전 %I:%M:%S")

            if action['action'] == 'D':
                last_d_time = action_time
                break
            else:
                post_d_command_time = action_time

        # 이미지 JSON 로딩
        with open(image_json_path, 'r') as file:
            images = json.load(file)

        # 조건에 맞는 이미지 데이터 추출
        results = []
        if last_d_time:
            for image in images:
                image_time = dt.strptime(image['time'], "%Y-%m-%d %H:%M:%S.%f")
                if not post_d_command_time:  # post_d_command_time이 None이면 'D' 이후의 모든 이미지를 추출
                    if image_time > last_d_time:
                        results.append(image['imageData'])
                elif post_d_command_time and last_d_time < image_time < post_d_command_time:
                    results.append(image['imageData'])

        return results