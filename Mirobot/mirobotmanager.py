from config import *
import asyncio
import re
import os
import time

class MirobotManager():
    def __init__(self, arm) -> None:
        self.arm = arm
        self.default_speed = 500

        init_data = asyncio.run(self.getCurrentAngle())

        self.first_wait = True

        print(f"초기 미로봇 각도 : {init_data}")
    async def AxisControl(self, key) -> None:
        """조종 데이터를 기반으로 머니퓰레이터 제어

        Args:
            key (str): Keyboard, Remote Control info
        """
        
        """
        조종 데이터를 기반으로 머니퓰레이터를 제어.
        """
        
        if await self.maxAngle(key):
            print("이동 가능 범위를 벗어났습니다!")
        
        else:
            if key == KUP_1:
                self.set_joint_angle({1:JOINT_ANGLE}, is_relative= True, speed= SPEED)        

            elif key == KDOWN_1:
                self.set_joint_angle({1:-JOINT_ANGLE}, is_relative=True, speed= SPEED)    
                    
            elif key == KUP_2:
                self.set_joint_angle({2:JOINT_ANGLE}, is_relative=True, speed= SPEED)
                
            elif key == KDOWN_2:
                self.set_joint_angle({2:-JOINT_ANGLE}, is_relative=True, speed= SPEED)            

            elif key == KUP_3:
                self.set_joint_angle({3:JOINT_ANGLE}, is_relative=True, speed= SPEED) 
                            
            elif key == KDOWN_3:
                self.set_joint_angle({3:-JOINT_ANGLE}, is_relative=True, speed= SPEED) 

            elif key == KUP_4:
                self.set_joint_angle({4:JOINT_ANGLE}, is_relative=True, speed= SPEED)
                                                    
            elif key == KDOWN_4:
                self.set_joint_angle({4:-JOINT_ANGLE}, is_relative=True, speed= SPEED)

            elif key == KUP_5:
                self.set_joint_angle({5:JOINT_ANGLE}, is_relative=True, speed= SPEED) 

            elif key == KDOWN_5:
                self.set_joint_angle({5:-JOINT_ANGLE}, is_relative=True, speed= SPEED) 

            elif key == KUP_6:
                self.set_joint_angle({6:JOINT_ANGLE}, is_relative=True, speed= SPEED)

            elif key == KDOWN_6:
                self.set_joint_angle({6:-JOINT_ANGLE}, is_relative=True, speed= SPEED)
                
            elif key == ENDEF_1:
                self.arm.pump_suction()
                print(f"endeffector 1, gripper open")
                # self.arm.gripper_open()
                
            elif key == ENDEF_2:
                self.arm.pump_blowing()
                print(f"endeffector 2, pump blowing")
                # self.arm.gripper_close()
                
            elif key == ENDEF_3:
                self.arm.pump_off()
                print(f"endeffector 3, gripper open")
                
            else:
                print("지정되지 않은 키입니다!") 

        if self.first_wait == True:
            time.sleep(1)
            self.first_wait = False
            print(f"{key} 키 입력됨, 현재 미로봇 각도 : {await self.getCurrentAngle()}")
        else:
            time.sleep(1)
            self.first_wait = False
            print(f"{key} 키 입력됨, 현재 미로봇 각도 : {await self.getCurrentAngle()}")

    def getCurrentPosition(self) -> str:
        """Mirobot Arm의 현재 좌표를 반환

        Returns:
            str: position = {"x": x, "y": y, "z": z, "roll": roll, "pitch": pitch, "yaw": yaw}
        """

        self.arm.get_status()
        position = {"x" : self.arm.status.cartesian.x, "y" : self.arm.status.cartesian.y, "z" : self.arm.status.cartesian.z,
                    "roll" : self.arm.status.cartesian.roll, "pitch" : self.arm.status.cartesian.pitch, "yaw" : self.arm.status.cartesian.yaw}
        
      
        text = f"Current Position : {position}"

        return text

    async def getCurrentAngle(self) -> str:
        """Mirobot Arm의 현재 관절 각도를 반환

        Returns:
            str: {"1": joint4, "2": joint5, "3": joint6, "4": joint1, "5": joint2, "6": joint3}
        """
        
        self.arm.get_status()
        angle = {"1" : self.arm.angle.joint4, "2" : self.arm.angle.joint5, "3" : self.arm.angle.joint6,
                    "4" : self.arm.angle.joint1, "5" : self.arm.angle.joint2, "6" : self.arm.angle.joint3}
        
        return angle
        
    async def maxAngle(self, key) -> bool:
        """미로봇이 가동할 수 있는 최대각도를 벗어나면 예외처리

        Args:
            key (str): Keyboard, Remote Control info

        Returns:
            bool: 각도 초과 여부 반환(True/False)
        """

        angle = await self.getCurrentAngle()
        
        
        if key == KUP_1:
            if angle['1'] > MAX_1:
                return True
            else:
                return False
        
        elif key == KDOWN_1:
            if angle['1'] < MIN_1:
                return True
            else:
                return False
        
        elif key == KUP_2:
            if angle['2'] > MAX_2:
                return True
            else:
                return False
                    
        elif key == KDOWN_2:
            if angle['2'] < MIN_2:
                return True
            else:
                return False
            
        elif key == KUP_3:
            if angle['3'] > MAX_3:
                return True
            else:
                return False
                    
        elif key == KDOWN_3:
            if angle['3'] < MIN_3:
                return True
            else:
                return False            

        elif key == KUP_4:
            if angle['4'] > MAX_4:
                return True
            else:
                return False
                    
        elif key == KDOWN_4:
            if angle['4'] < MIN_4:
                return True
            else:
                return False             
            
        elif key == KUP_5:
            if angle['5'] > MAX_5:
                return True
            else:
                return False
                    
        elif key == KDOWN_5:
            if angle['5'] < MIN_5:
                return True
            else:
                return False 

        elif key == KUP_6:
            if angle['6'] > MAX_6:
                return True
            else:
                return False
                    
        elif key == KDOWN_6:
            if angle['6'] < MIN_6:
                return True
            else:
                return False             
            
            
    def set_joint_angle(self, joint_angles, speed=None, is_relative=False, wait_ok=None):
        for joint_i in range(1, 8):
            
            # 각도 설정
            if joint_i not in joint_angles:
                joint_angles[joint_i] = None

        return self.go_to_axis(x=joint_angles[1], y=joint_angles[2], z=joint_angles[3], a=joint_angles[4], \
            b=joint_angles[5], c=joint_angles[6], d=joint_angles[7], is_relative=is_relative, speed=speed, wait_ok=wait_ok)  
        
    
    def go_to_axis(self, x=None, y=None, z=None, a=None, b=None, c=None, d=None, speed=None, is_relative=False, wait_ok=True):
        instruction = 'M21 G90'  # X{x} Y{y} Z{z} A{a} B{b} C{c} F{speed}
        if is_relative:
            instruction = 'M21 G91'
        if not speed:
            speed = SPEED
        if speed:
            speed = int(speed)

        pairings = {'X': x, 'Y': y, 'Z': z, 'A': a, 'B': b, 'C': c, 'D': d, 'F': speed}
        msg = self.arm.generate_args_string(instruction, pairings)

        return self.send_msg(msg, wait_ok=wait_ok)    
          
    def send_msg(self, msg, var_command=False, disable_debug=False, terminator=os.linesep, wait_ok=None, wait_idle=False):
        if self.arm.is_connected:
            # convert to str from bytes
            if isinstance(msg, bytes):
                msg = str(msg, 'utf-8')
            
            # remove any newlines
            msg = msg.strip()

            # check if this is supposed to be a variable command and fail if not
            # if var_command and not re.fullmatch(r'\$\d+=[\d\.]+', msg):
            #     self.logger.exception(MirobotVariableCommandError("Message is not a variable command: " + msg))

            if wait_ok is None:
                wait_ok = False
            
            # print(f"send_msg wait_ok = {wait_ok}")
            # actually send the message
            ret = self.arm.device.send(msg,
                                        disable_debug=disable_debug,
                                        terminator=os.linesep,
                                        wait_ok=wait_ok,
                                        wait_idle=wait_idle)

            return ret

        else:
            raise Exception('Mirobot is not Connected!')        


#remote 원격제어 로그로 -> 가상 원격제어 기기 탄생 -> 3d
                       # -> 기기 종류에 상관없이 형식만 맞추면 자동으로 추가가능하게 

                    # -> 고민중 실시간으로 나오는 로그로 하나씩 데입한다 1번
                    # -> 저장한 로그로 모델을 만든다 2번
        
# def jointControl(self, key) -> None:
#         """
#         키보드 이벤트를 입력받아 처리하는 함수
#         """

#         # if self.maxPosition(key):
#         #     print("Can't Move Out of Range!")
            
#         if self.maxAngle(key):
#             print("Can't Move Out of Angle!")            
        
#         else:
#             angle = self.getCurrentAngle()
#             print(f"{key} pressed, angle : {angle}")
            
#             if key == KUP_1:
#                 self.arm.set_joint_angle({1:JOINT_ANGLE}, is_relative=True)         
            
#             elif key == KDOWN_1:
#                 self.arm.set_joint_angle({1:-JOINT_ANGLE}, is_relative=True)    
                    
#             elif key == KUP_2:
#                 self.arm.set_joint_angle({2:JOINT_ANGLE}, is_relative=True)
                
#             elif key == KDOWN_2:
#                 self.arm.set_joint_angle({2:-JOINT_ANGLE}, is_relative=True)            

#             elif key == KUP_3:
#                 self.arm.set_joint_angle({3:JOINT_ANGLE}, is_relative=True) 
                            
#             elif key == KDOWN_3:
#                 self.arm.set_joint_angle({3:-JOINT_ANGLE}, is_relative=True) 

#             elif key == KUP_4:
#                 self.arm.set_joint_angle({4:JOINT_ANGLE}, is_relative=True)
                                                    
#             elif key == KDOWN_4:
#                 self.arm.set_joint_angle({4:-JOINT_ANGLE}, is_relative=True)

#             elif key == KUP_5:
#                 self.arm.set_joint_angle({5:JOINT_ANGLE}, is_relative=True) 

#             elif key == KDOWN_5:
#                 self.arm.set_joint_angle({5:-JOINT_ANGLE}, is_relative=True) 

#             elif key == KUP_6:
#                 self.arm.set_joint_angle({6:JOINT_ANGLE}, is_relative=True)

#             elif key == KDOWN_6:
#                 self.arm.set_joint_angle({6:-JOINT_ANGLE}, is_relative=True)
                
#             elif key == ENDEF_1:
#                 self.arm.pump_suction()
#                 # self.arm.gripper_open()
                
#             elif key == ENDEF_2:
#                 self.arm.pump_blowing()
#                 # self.arm.gripper_close()
             
#             elif key == ENDEF_3:
#                 self.arm.pump_off()
                
#             else:
#                 print("Unassigned key!")    

    # def maxPosition(self, key) -> bool:
    #     """
    #     미로봇이 가동할 수 있는 최대범위를 벗어나면 예외처리
    #     """
    #     self.arm.get_status()
    #     position = {"x" : self.arm.status.cartesian.x, "y" : self.arm.status.cartesian.y, "z" : self.arm.status.cartesian.z,
    #                 "roll" : self.arm.status.cartesian.roll, "pitch" : self.arm.status.cartesian.pitch, "yaw" : self.arm.status.cartesian.yaw}
        
    #     if key == "a" and position == A_MAX or key == "d" and position == D_MAX or \
    #         key == "w" and position == W_MAX or key == "s" and position == S_MAX:
    #         return True
    #     else:
    #         return False  