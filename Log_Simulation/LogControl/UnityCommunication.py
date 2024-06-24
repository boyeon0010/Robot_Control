from pyevsim import BehaviorModelExecutor, Infinite, SysMessage
import time

class CommunicationModel(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, device, conn):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.conn = conn
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Generate",1)

        self.insert_input_port("start")
        self.insert_input_port("next")

        self.insert_output_port("need_next")

        self.count = 0
        self.w_count = 0
        self.frame_rate = 1/30  # 30 FPS에 해당하는 시간 간격


    def ext_trans(self, port, msg):
        if port == "start":
            print("unitycommunication start in")
            self.image_data_one = msg.retrieve()[0][0]
            print(len(self.image_data_one))
            self._cur_state = "Generate"


    def output(self):
        if self._cur_state == "Generate":
            
            for img in self.image_data_one:
                
                start_time = time.time()
                self.conn.send(self.count, self.conn.time(), img)
                self.count += 1
                end_time = time.time()
                elapsed_time = end_time - start_time
                time_to_wait = self.frame_rate - elapsed_time

                if time_to_wait > 0:
                    time.sleep(time_to_wait)  # 프레임 레이트를 맞추기 위해 대기


            self._cur_state = "Wait"
            

        if self._cur_state == "Wait" :
            print("unitycommunication start in")
            
            raw_data = self.conn.conn.recv(4096).decode("utf-8")
            
            if raw_data is not None:
                self.action, self.time = self.data_split(raw_data)
                print(f"action {self.action} time {self.time}")
                if self.action == "W" or self.action == "D":
                    if self.action == "W":
                        self.w_count +=1
                    msg = SysMessage(self.get_name(), "need_next")
                    msg.insert([self.action,self.w_count])
                    raw_data = None
                    return msg

     
    def int_trans(self):
        if self._cur_state == "Generate":
            self._cur_state = "Wait"

    def data_split(self,data):
        result = data.split('|')
        print(result)
        return result[0],result[1]

    