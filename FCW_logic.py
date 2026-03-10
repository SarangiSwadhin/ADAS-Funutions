##Define all the input parameters
from math import fabs

print("Enter the speed of the ego vehicle")
speed_ego= int(input())
print("Enter the speed of the vehicle infront of us")
speed_infront = int(input())
print("Enter the speed of the ego vehicle")
print("Distance between the vehicle")
distance = int(input())
relative_speed = speed_ego - speed_infront
abs_rel = abs(relative_speed)

if distance >>200:
    print("Vehicles too far away for collision. Enter a vaild distnce")

TTC = distance/abs_rel
threat_level = ["safe", "warning", "critical"]
advice = ["none", "prepare to brake","brake immediately"]
##Computing the outputs

if TTC >6:
    print("the threat level is" + " " + threat_level[0])
    print("the advive is" + " " + advice[0])
elif TTC <=5 & TTC>=3:
    print("the threat level is" + " " + threat_level[1])
    print("the advive is" + " " + advice[1])
else:
    print("the threat level is" +" " + threat_level[2])
    print("the advive is" + " " + advice[2])
    
         
