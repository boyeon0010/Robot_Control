from config import *
import keyboard
from mirobotmanager import MirobotManager
# from pynput import keyboard
import asyncio
file_path = 'key_inputs.txt'
class Keymanager(MirobotManager):
    async def _setAxis(self) -> None:
        """키보드 모드. 키보드 입력을 통해 Mirobot의 Joint Angle 이동
        """
        with open(file_path, 'a') as file:
            while True:
                key = keyboard.read_key()
                print(f"select key {key}")
                file.write(key + '\n')
                if key == "1": 
                    print("Exit, Bye!") 
                    self.arm.pump_off()
                    self.arm.go_to_zero()
                    break
                else:
                    await asyncio.create_task(self.AxisControl(key))
                
    # def _setJointAngle(self) -> None:
    #     """
    #     Keyboard Action Handler
    #     """
    #     while True:
    #         key = keyboard.read_key()
            
    #         if key == "1":
    #             print("Exit, Bye!")
    #             self.arm.pump_off()
    #             self.arm.go_to_zero()
    #             break
    #         else:
    #             self.jointControl(key)            
    #             # await self.AxisControl(key)

    # async def _read_key(self):
    #     key = keyboard.read_key()
    #     return key

    #     with keyboard.Listener(
    #             on_press=self.on_press,
    #             on_release=self.on_release) as listener:
    #         listener.join()
    
    # def on_press(key):
    #     try:
    #         print('Alphanumeric key pressed: {0} '.format(
    #             key.char))


    #     except AttributeError:
    #         print('special key pressed: {0}'.format(
    #             key))

    # def on_release(key):
    #     print('Key released: {0}'.format(
    #         key))
    #     if key == keyboard.Key.esc:
    #         # Stop listener
    #         return False
                   
                                                