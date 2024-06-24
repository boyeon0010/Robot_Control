import argparse
from wlkata_mirobot import WlkataMirobot, WlkataMirobotTool
from keymanager import Keymanager
from remotemanager import Remotemanager
from config import *
import asyncio

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mirobot Control")
    parser.add_argument("mode", choices=["keyboard", "remote"])    
    
    args = parser.parse_args()
    
    print("Instantiate the Mirobot Arm instance")
    try:
        arm = WlkataMirobot(portname=PORTNAME)
        # Mirobot Arm Multi-axis executing
        print("Homing start")

        arm.home()

        print("Homing finish")    
        arm.set_tool_type(WlkataMirobotTool.FLEXIBLE_CLAW)

        if args.mode == "keyboard":
            print("Keyboard Control Mode")
            # Keymanager(arm)._setJointAngle()
            asyncio.run(Keymanager(arm)._setAxis())
            
        elif args.mode == "remote":
            print("Remote Control Mode")   
            # Default Remote
            # Remotemanager(arm).remoteRecv() 
            
            # Asyncio Remote
            asyncio.run(Remotemanager(arm)._remoteRecv())
    except:
        print("Mirobot is not connected")