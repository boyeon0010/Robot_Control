import asyncio
import keyboard
import time
from robomaster import robot
from robomaster import camera

# file_path = 'key_inputs.txt'

class Keymanager:
    def __init__(self, ep_robot):
        self.ep_robot = ep_robot
        self.ep_chassis = ep_robot.chassis
        self.ep_gimbal = ep_robot.gimbal

    async def AxisControl(self, key):
        # Define body movement based on key
        body_movement = {
            'w': (0.3, 0, 0),
            's': (-0.3, 0, 0),
            'a': (0, -0.3, 0),
            'd': (0, 0.3, 0),
            'q': (0, 0, 45),
            'e': (0, 0, -45)
        }

        # Define gimbal movement based on key
        gimbal_movement = {
            'i': (30, 0),
            'k': (-30, 0),
            'j': (0, -30),
            'l': (0, 30)
        }

        if key in body_movement:
            x, y, z = body_movement[key]
            self.ep_chassis.move(x=x, y=y, z=z, xy_speed=0.7, z_speed=45).wait_for_completed()
        elif key in gimbal_movement:
            pitch, yaw = gimbal_movement[key]
            self.ep_gimbal.move(pitch=pitch, yaw=yaw).wait_for_completed()

    async def _setAxis(self):
        # with open(file_path, 'a') as file:
        while True:
            key = keyboard.read_event().name
            print(f"select key {key}")
            # file.write(key + '\n')
            if key == "1" or key == "esc":
                print("Exit, Bye!")
                # Stop camera stream
                ep_camera.stop_video_stream()

                ep_robot.close()
                break
            else:
                await self.AxisControl(key)

if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta", sn="3JKCK980030EKR")

    # Start camera stream
    ep_camera = ep_robot.camera
    ep_camera.start_video_stream(display=True, resolution=camera.STREAM_360P)

    keymanager = Keymanager(ep_robot)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(keymanager._setAxis())
    except KeyboardInterrupt:
        print("Ctrl+C pressed. Exiting...")


    # Stop camera stream
    ep_camera.stop_video_stream()

    ep_robot.close()
