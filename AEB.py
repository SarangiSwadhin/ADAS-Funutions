import math
import time

print("Autonomous emergency braking system")
print("Enter the speed of ego vehicle")
speed_ego = int(input())
print("Enter the speed of lead vehicle")
speed_lead = int(input())
print("Enter the distance between the vehicles")
distance = int(input())

rel_speed = speed_ego - speed_lead
abs_rel = abs(rel_speed)

ttc = distance/abs_rel 

if ttc > 6:
    while True:
        speed_ego +=1
        distance -=1
        rel_speed = speed_ego - speed_lead
        abs_rel = abs(rel_speed)
        if abs_rel==0:
            abs_rel +=1           
        ttc = distance/abs_rel
        
        print(f"\r speed_ego: {speed_ego} lead_speed: {speed_lead} ttc : {ttc}")

        if ttc <= 1.5:
            speed_ego =0
            print("Breaks applied")
            break