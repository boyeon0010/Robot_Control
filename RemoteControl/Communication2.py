from pyevsim import BehaviorModelExecutor, Infinite, SysMessage
import json

class Communication2Model(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, device):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.device = device
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Generate",1)

        self.insert_input_port("start")

        self.insert_output_port("re")

        self.jsone_name = engine_name

        self._recvdatalist = []

    def ext_trans(self, port, msg):
        if port == "start":
            self.action_data = msg.retrieve()[0][0]
            self.action, self.time = self.data_split(self.action_data)
            print(f"action {self.action} time {self.time}")

            action_savedata = {
                "action": self.action ,
                "time": self.time,
            }

            self._recvdatalist.append(action_savedata)
            self.data_to_json(self.jsone_name)

            self._cur_state = "Generate"


    def output(self):
        if self._cur_state == "Generate":
            if self.action in ["Q","W","E","A","S","D"]:
                self.device.Move(self.action)
            elif self.action in ["I","J","K","L"]:
                self.device.Rotation(self.action)

            msg = SysMessage(self.get_name(), "re")
            return msg


    def data_split(self,data):
        result = data.split('|')
        print(result)
        return result[0],result[1]
    
    def data_to_json(self, devicename):
        filename = f"{devicename}.json"
        
        # 파일에 새 데이터를 덮어쓰기
        with open(filename, 'w') as json_file:
            json.dump(self._recvdatalist, json_file, indent=1)