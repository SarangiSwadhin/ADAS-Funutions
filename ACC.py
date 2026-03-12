##Adaptive cruise control

import math
import time

##initalise the inputs

print("enter the speed of the ego vehice")
ego_speed = int(input())
print("enter the speed of the lead vehicle")
speed_lead = int(input())
print("enter the distance between the vehicle")
distance = int(input())

##prepare the logic

while True:
    if distance > 10:
        # Accelerate
        ego_speed += 1
        distance -= 1
        speed_lead +=0.5
        print(f"Accel: Ego={ego_speed}, lead = {speed_lead}, Dist={distance}")
    else:
        # Brake drastically + increase distance
        ego_speed -= 10
        distance += 49
        print(f"Brake: Ego={ego_speed}, lead = {speed_lead}, Dist={distance}")
        
        if distance >= 50:  # Stop condition
            ego_speed += 1
            distance -= 1
            speed_lead +=1
            print(f"Accel: Ego={ego_speed}, lead = {speed_lead}, Dist={distance}")

        
    time.sleep(1)  # Slow for visibility
