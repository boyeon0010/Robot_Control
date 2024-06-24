from pyevsim import BehaviorModelExecutor, SystemSimulator, Infinite
from .DataClass import DataClassModel
from .UnityCommunication import CommunicationModel
from .Tcp import Communication

class LogManager():
    def __init__(self, device) -> None:

        self.communication = Communication()

        self.log = SystemSimulator()

        self.log.register_engine("COM", "VIRTUAL_TIME", 1)

        self.log_model = self.log.get_engine("COM")

        self.log_model.insert_input_port("start")
        self.log_model.insert_input_port("next")
        
        print("start log engine")
        Communication_m = CommunicationModel(0, Infinite, "Communication_m", "COM", device, self.communication)
        DataClass_m = DataClassModel(0, Infinite, "DataClass_m", "COM")

        self.log_model.register_entity(Communication_m)
        self.log_model.register_entity(DataClass_m)

        self.log_model.coupling_relation(None, "start", DataClass_m, "start")
        self.log_model.coupling_relation(DataClass_m, "image_data", Communication_m, "start")
        self.log_model.coupling_relation(Communication_m, "need_next", DataClass_m, "next")
        self.log_model.coupling_relation(DataClass_m, "image_data", Communication_m, "start")
   
        self.start()


    def start(self) -> None:
        # pass
        self.log_model.insert_external_event("start","start")
        self.log_model.simulate()
