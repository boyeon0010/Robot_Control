from pyevsim import BehaviorModelExecutor, Infinite, SysMessage
import json

class CommunicationModel(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, conn):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.conn = conn.conn
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Generate",0)

        self.insert_input_port("start")

        self.insert_output_port("control_data")
        
        

    def ext_trans(self, port, msg):
        if port == "start":
            self._cur_state = "Generate"


    def output(self):
        if self._cur_state == "Generate":
            self._cur_state = "Wait"


        if self._cur_state == "Wait" :
            print("unitycommunication start in")
            raw_data = self.conn.recv(4096).decode("utf-8")

            if raw_data is not None:
                # result = raw_data.split('|')
                
                
            
                msg = SysMessage(self.get_name(), "control_data")
                msg.insert([raw_data])
                return msg

     
    def int_trans(self):
        if self._cur_state == "Wait":
            self._cur_state = "Wait"

        
    

    
    