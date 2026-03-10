import math

def forward_colliision_warning(speed_ego, speed_infront, distance):

    relative_speed = speed_ego-speed_infront
    abs_rel= abs(relative_speed)
##CHECKING THE CASES IF VEHICE IS TOO FAR AWAY ORTHE RELATIVE SPEED IS 0 THEN THE CAHNCES OF COLLISON IS VERY LESS
    if distance >50:
        return "Both vehickles are at a safe distance"
    
    if abs_rel ==0:
        return "No chnances of collision"
    
    #CALCULATION OF TIME TO COLLISON (TTC)
    
    TTC = distance/abs_rel

    risk = ["safe","warning","critical"]
    advice = ["none","ready to apply brake","brake immediately"]

    if TTC >=6:
        return f"the risk level is {risk[0]}\nThe advice is {advice[0]}"
    if TTC >2 and TTC <5:
        return f"the risk level is {risk[1]}\nThe advice is {advice[1]}"
    if TTC < 2:
        return f"the risk level is {risk[3]}\nThe advice is {advice[3]}"
    

if __name__ == "__main__":
 print("Enter the speed of the ego vehicle")
speed_ego= int(input())
print("Enter the speed of the vehicle infront of us")
speed_infront = int(input())
print("Distance between the vehicle")
distance = int(input())
relative_speed = speed_ego - speed_infront
abs_rel = abs(relative_speed)

result = forward_colliision_warning(speed_ego, speed_infront, distance)
print(result)