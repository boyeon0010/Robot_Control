from pyevsim import BehaviorModelExecutor, SystemSimulator, Infinite
# from .DataClass import DataClassModel
from .UnityCommunication import CommunicationModel
from .Communication2 import Communication2Model
from .SendImageToUnity import SendImageToUnity
from .Tcp import Communication
import threading

class RemoteManager():
    def __init__(self,device, device_info) -> None:

        self.communication = Communication()
        print(f"{device}")

        self.device = device
        self.device_info = device_info

        
        print("start engine")

   
        self.start()

    def send_s(self):
        self.send = SystemSimulator()
        self.send.register_engine(self.device+"s", "VIRTUAL_TIME", 0.0001)
        self.send_model = self.send.get_engine(self.device+"s")
        self.send_model.insert_input_port("start")
        SendImageToUnity_m = SendImageToUnity(0, Infinite, "ImageConvert_m", self.device+"s", self.device_info,self.communication)
        self.send_model.register_entity(SendImageToUnity_m)
        self.send_model.coupling_relation(None, "start", SendImageToUnity_m, "start")

    def recv_s(self):
        self.recv = SystemSimulator()
        self.recv.register_engine(self.device+"r", "REAL_TIME", 1)
        self.recv_model = self.recv.get_engine(self.device+"r")
        self.recv_model.insert_input_port("start")
        Communication_m = CommunicationModel(0, Infinite, "Communication_m", self.device+"r", self.communication)
        Communication2_m = Communication2Model(0, Infinite, "Communication2_m", self.device+"r", self.device_info)
        self.recv_model.register_entity(Communication_m)
        self.recv_model.register_entity(Communication2_m)
        self.recv_model.coupling_relation(None, "start", Communication_m, "start")
        self.recv_model.coupling_relation(Communication_m, "control_data", Communication2_m, "start")
        self.recv_model.coupling_relation(Communication2_m, "re", Communication_m, "start")

    def start(self):
        # Create threads for send and recv simulations
        send_thread = threading.Thread(target=self.run_send)
        recv_thread = threading.Thread(target=self.run_recv)

        # Start the threads
        send_thread.start()
        recv_thread.start()

        # Optionally, wait for both threads to complete
        send_thread.join()
        recv_thread.join()

    def run_send(self):
        self.send_s()
        self.send_model.insert_external_event("start", "start")
        self.send_model.simulate()

    def run_recv(self):
        self.recv_s()
        self.recv_model.insert_external_event("start", "start")
        self.recv_model.simulate()
    
