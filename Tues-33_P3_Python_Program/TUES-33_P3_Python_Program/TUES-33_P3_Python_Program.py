import time
import random
import sys
sys.path.append('../')

from Common_Libraries.p3b_lib import *

import os
from Common_Libraries.repeating_timer_lib import repeating_timer

def update_sim():
    try:
        my_table.ping()
    except Exception as error_update_sim:
        print (error_update_sim)

### Constants
speed = 0.2 #Qbot's speed

### Initialize the QuanserSim Environment
my_table = servo_table()
arm = qarm()
arm.home()
bot = qbot(speed)

##---------------------------------------------------------------------------------------
## STUDENT CODE BEGINS
##---------------------------------------------------------------------------------------

#Zareen and Sude
#this function dispenses the bottles onto the servo table
def dispense_container():
    bottle = random.randint(1,6)                            #a random container through 1-6 is chosen
    c_type = my_table.container_properties(bottle)          #the container properties are determined
    my_table.dispense_container()                           #and dispensed (as well as returned)    
    return c_type

#Zareen and Sude
#this function loads the container onto the Q-bot using the Q-arm
def load_container(counter):
    net_weight = 0
    p_bin_num = 0
    bottle_num = 0
    if counter == 0: 
        bot.forward_time(9.9)
    else:
        bot.forward_time(0.7)
    
    for bottle_num in range(1,4):                           #for loop that takes the container properties and 
        c_properties = dispense_container()                 #splits them into material, weight, and bin number
        print(c_properties)
        material, weight, bin_num = c_properties[0], c_properties[1], c_properties[2]
        net_weight += weight                                #calculates the total weight
        if bottle_num == 1:
            p_bin_num = bin_num                             #stores the first bin number, (meets the first constraint)
            pass
            print("Bottle number 1!")


        if p_bin_num != bin_num:                            #and if the bin number doesn't match the previous one,
            print("Different bin!")                         #the q-arm won't pick it up (meets the second constraint)
            break
        else:
            if net_weight > 90:                             #net weight can't surpass 90 grams (meets the last constraint)
                print("Too much weight")
                break
            else:
                arm.move_arm(0.644, 0.0, 0.2733)            #if it meets all of the previous conditions, the container is picked up 
                arm.control_gripper(45)                     #and placed on the hopper
                arm.move_arm(0.4064, 0.0, 0.4826)
                if bottle_num == 1:
                    arm.move_arm(-0.0956, -0.3567, 0.4107)
                elif bottle_num == 2:
                    arm.move_arm(0.0, -0.3926, 0.3774)
                else:
                    arm.move_arm(0.1016, -0.3792, 0.3774)
                arm.control_gripper(-25)
                arm.move_arm(0.0, -0.2874, 0.77)
                arm.home()
    return p_bin_num                                        #returns the first bin number


#Zareen and Sude
#this function transfers containers using bin_num while approaching the appropriate bin whilst following the trajectory of a line
def transfer_container(bin_num):
    bot.rotate(180)
    time.sleep(2)
    MIN_READING = 0.1                                       #defined variable for sensor reading of a bin proximity
    bot.activate_ultrasonic_sensor()
    lost_line = 0
    reading = bot.read_ultrasonic_sensor(bin_num)           #bot activates and reads the sensor for the correct bin
    while reading > MIN_READING:                            #while the designated bin is out of reach
                                                            #keep reading until it is in reach
        while lost_line < 2:                                #checks if the bot is on the line, and makes sure it stays on the line
            lost_line, velocity = bot.follow_line(0.1)
            bot.forward_velocity(velocity)
            reading = bot.read_ultrasonic_sensor(bin_num)
            if reading <= MIN_READING:                      #if the bot has approached the correct bin, stop the bot 
                bot.stop()                                  #and prepare for dumping
                bot.deactivate_ultrasonic_sensor()
                print("Coast is clear!!")
                return
            print(bin_num , reading)

#Zareen and Sude                    
#this function deposits the container into the designated bin
def deposit_container():                                    
    time.sleep(2)     
    bot.activate_actuator()                                 #activates the actuator to deposit the containers
    bot.dump()                                              #dumps the container
    
#Zareen and Sude
#this function returns both the Q-arm and Q-bot to their appropriate home positions
def return_home():
    arm.home()
    lost_line = 0
    while lost_line < 2:                                    #follows the trajectory of the line around the loop
        lost_line, velocity = bot.follow_line(0.1)
        bot.forward_velocity(velocity)
        print(lost_line)
    bot.stop()                                              #stops at home position :)

#Zareen and Sude
#this function is the main function (all the other functions are called within it)
def main():
    counter = 0                                             #the variable counts how many times the simulation runs           
    while True:
        bin_num = load_container(counter)                   #counter is sent into load_container
        transfer_container(bin_num)                     
        deposit_container()
        my_table.rotate_table_angle(45)                     #servo table rotates 45 degrees after each iteration of the program
        return_home()
            
        counter += 1                                        #1 is added to the counter so the loop occurs another time

                                                        
main()

