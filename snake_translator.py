#Beginning of snake_translator
'''
This is the code for the snake translator. For latest version go to:
https://github.com/the-dan-ya/spike_prime_python_translator/blob/main/snake_translator.py

Documentation -> README.md:
https://github.com/the-dan-ya/spike_prime_python_translator/blob/main/README.md

Change Log: 
9/28/2023 Initial Version
9/30/2023 Removed async functions for better alignment with word blocks
'''

from hub import light_matrix, port, motion_sensor, button, sound
import runloop, motor, motor_pair, color_sensor, color #from lego
import time #from micropython
from app import sound as appsound

default_movement_speed = 360

degrees_per_cm = 360/17.5

class unit:
    CM = 0
    IN = 1
    DEGREES = 2
    ROTATIONS = 3
    SECONDS = 4

class direction:
    FORWARD = 101
    BACKWARD = -101

default_motor_speeds = {
    
} 

def absolute_position_wb2py(wb_position:int):
    return ((wb_position+180) % 360) - 180

def unit_to_degrees(amount:float, in_unit:int, speed:int):
    if in_unit == unit.CM:
        return int(amount * degrees_per_cm)
    elif in_unit == unit.ROTATIONS:
        return int(amount*360)
    elif in_unit == unit.IN:
        return int(amount*degrees_per_cm*2.54)
    elif in_unit == unit.SECONDS:
        return int(amount*(speed))
    else:
        return int(amount)

def get_default_speed_for(motor_port):
    if motor_port in default_motor_speeds.keys():
        return default_motor_speeds[motor_port]
    else:
        return default_movement_speed

#MOTORS
def run_for(motor_port:int, orientation: int, amount: float, in_unit: int):
    start_position = motor.relative_position(motor_port)
    speed = get_default_speed_for(motor_port)
    if orientation == motor.COUNTERCLOCKWISE:
        speed = -speed
    while abs(motor.relative_position(motor_port)-(start_position)) < abs(unit_to_degrees(amount,in_unit, speed)):
        motor.run(motor_port, speed)
    motor.stop(motor_port)

def go_to_absolute_position(motor_port:int, orientation:int, wb_position:int):
    speed = get_default_speed_for(motor_port)
    target_position = absolute_position_wb2py(wb_position)
    current_position = motor.absolute_position(motor_port)
    if target_position != current_position:
        motor.run_to_absolute_position(motor_port,target_position,speed,direction = orientation)
        degrees_to_run = 0
        if orientation == motor.CLOCKWISE:
            if target_position > current_position:
                degrees_to_run = target_position-current_position
            else:
                degrees_to_run = 360-current_position+target_position
        elif orientation == motor.COUNTERCLOCKWISE:
            if target_position < current_position:
                degrees_to_run = current_position - target_position
            else:
                degrees_to_run = 360- target_position + current_position
        elif orientation == motor.SHORTEST_PATH:
            if target_position > current_position:
                degrees_to_run = target_position-current_position
            else:
                degrees_to_run = current_position-target_position
        time.sleep_ms(int(1000*((degrees_to_run)/speed)))

def start_motor(motor_port:int, orientation:int):
    motor_speed = get_default_speed_for(motor_port)
    if orientation == motor.COUNTERCLOCKWISE:
        motor_speed = -motor_speed
    motor.run(motor_port, motor_speed)

def stop_motor(motor_port:int):
    motor.stop(motor_port)

def set_speed_to(motor_port:int, speed_percent:int):
    default_motor_speeds[motor_port] = speed_percent*10

def absolute_position(motor_port:int):
    return motor.absolute_position(motor_port)

def motor_speed(motor_port:int):
    return abs(motor.velocity(motor_port))


#MOVEMENT
def move_for(steer_value: int, amount: float, in_unit: int):
    move_speed=default_movement_speed
    move_steer = steer_value
    if steer_value == direction.FORWARD:
        move_steer = 0
    elif steer_value == direction.BACKWARD:
        move_steer = 0
        move_speed = -default_movement_speed
    degrees= unit_to_degrees(amount, in_unit,move_speed)
    motor_pair.move_for_degrees(motor_pair.PAIR_1, degrees, move_steer, velocity= move_speed)
    time.sleep_ms(int((degrees/move_speed)*1000))

def start_moving(steer_value: int):
    start_move_speed = default_movement_speed
    start_steer = steer_value
    if steer_value == direction.FORWARD:
        start_steer = 0
    elif steer_value == direction.BACKWARD:
        start_steer = 0
        start_move_speed = -default_movement_speed
    motor_pair.move(motor_pair.PAIR_1, start_steer, velocity= start_move_speed)

def stop_moving():
    motor_pair.stop(motor_pair.PAIR_1)

def set_movement_speed_to(speed_percent:int):
    global default_movement_speed
    default_movement_speed=speed_percent*10

def set_movement_motors_to(left_drive:int, right_drive:int):
    motor_pair.unpair(motor_pair.PAIR_1)
    motor_pair.pair(motor_pair.PAIR_1,left_drive, right_drive)

def set_1_motor_rotation_to_cm(circumference:float):
    global degrees_per_cm
    degrees_per_cm=360/circumference

#LIGHT
#None for now and maybe never

#SOUND
def play_beep_for_seconds(key_number:int, duration:float, volume=75):
    #temporary translation, the frequency is not actually the keynote of word blocks
    sound.beep(int(key_number*5), int(duration*1000), volume)
    time.sleep_ms(int(duration*1000))

#EVENTS
#Please figure out on your own 
#See example in Competition Ready

#CONTROL
def wait_seconds(amount:float):
    time.sleep_ms(int(amount*1000))

def wait_until(function):
    while not function():
        pass
        
#Please learn basic python before coding in python

#SENSORS
def is_color(color_port:int, color_constant:int):
    return color_sensor.color(color_port) == color_constant

def get_color(color_port:int):
    return color_sensor.color(color_port)

#Use below and math :)

def reflection(color_port:int):
    return color_sensor.reflection(color_port)

def is_button_pressed(side:int):
    if side == button.LEFT:
        return button.pressed(button.LEFT) > 0
    else:
        return button.pressed(button.RIGHT) > 0

def start_moving_at_speed(left_speed: int, right_speed:int):
    motor_pair.move_tank(motor_pair.PAIR_1, left_speed*10, right_speed*10)

def set_yaw_angle_to_0():
    motion_sensor.reset_yaw(0)

def yaw_angle():
    return -int(motion_sensor.tilt_angles()[0]/10)

def pitch_angle():
    return int(motion_sensor.tilt_angles()[1]/10)

def roll_angle():
    return int(motion_sensor.tilt_angles()[2]/10)

def set_relative_position_to(motor_port:int, relative:int):
    motor.reset_relative_position(motor_port, relative)

def go_to_relative_position_at_speed(motor_port:int, target_position:int, speed:int):
    current_position = motor.relative_position(motor_port)
    motor.run_to_relative_position(motor_port, target_position, speed*10)
    time.sleep_ms(int(abs(target_position-current_position)/(speed*10)*1000))

def move_until(steer_value:int, function):
    start_moving(steer_value)
    wait_until(function)
    stop_moving()

def move_at_speed_until(left_speed:int,right_speed:int, function):
    start_moving_at_speed(left_speed,right_speed)
    wait_until(function)
    stop_moving()

#END OF LIBRARY