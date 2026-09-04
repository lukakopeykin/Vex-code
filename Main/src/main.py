#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain=Brain()

# Robot configuration code
mot_lf = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
mot_rf = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
mot_lb = Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)
mot_rb = Motor(Ports.PORT20, GearSetting.RATIO_18_1, False)
controller_1 = Controller(PRIMARY)
lift_inert = Inertial(Ports.PORT2)
mot_lift_l = Motor(Ports.PORT5, GearSetting.RATIO_18_1, True)
mot_lift_r = Motor(Ports.PORT6, GearSetting.RATIO_18_1, False)



# wait for rotation sensor to fully initialize
wait(30, MSEC)


# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))
      
# Set random seed 
initializeRandomSeed()


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

#endregion VEXcode Generated Robot Configuration

# ------------------------------------------
# 
# 	Project:      VEXcode Project
#	Author:       VEX
#	Created:      Luka Kopeykin
#	Description:  VEXcode V5 Python Project
# 
# ------------------------------------------

from vex import *
#region data

data1 = [] 

#endregion dat

SPEED = 30
REFRESH_IN_HERTZ = 300 #--> 5 a second
REFRESH = 60/REFRESH_IN_HERTZ

#region classes
class Togglable():
    def __init__(self, status):
        self.status = status
    def toggle(self):
        self.status = not self.status
balance = Togglable(False)
controller_1.buttonY.pressed(balance.toggle)

slow = Togglable(False)
controller_1.buttonB.pressed(slow.toggle)
#endregion classes

#region motor config
mot_lf.set_velocity(0, PERCENT)
mot_lb.set_velocity(0, PERCENT)
mot_rf.set_velocity(0, PERCENT)
mot_rb.set_velocity(0, PERCENT)
mot_lift_l.set_velocity(0, PERCENT)
mot_lift_r.set_velocity(0, PERCENT)

mot_lf.set_stopping(HOLD)
mot_rf.set_stopping(HOLD)
mot_lb.set_stopping(HOLD)
mot_rb.set_stopping(HOLD)
mot_lift_l.set_stopping(HOLD)
mot_lift_r.set_stopping(HOLD)

mot_lf.spin(FORWARD)
mot_lb.spin(FORWARD)
mot_rf.spin(FORWARD)
mot_rb.spin(FORWARD)
mot_lift_l.spin(FORWARD)
mot_lift_r.spin(FORWARD)

lift_inert.calibrate()
lift_inert.set_rotation(0, DEGREES)
wait(30, MSEC)
#endregion motor config

#region display
def prt():
    while True:
        controller_1.screen.clear_screen()
        controller_1.screen.set_cursor(1, 1)
        controller_1.screen.print(lift_inert.orientation(OrientationType.PITCH,DEGREES))
        controller_1.screen.set_cursor(2, 1)
        controller_1.screen.print("BALANCING: "+ str(balance.status))
        controller_1.screen.set_cursor(3, 1)
        controller_1.screen.print("SLOW MODE: " + str(slow.status))

        wait(REFRESH/1.5, SECONDS)
Thread(prt)
#endregion display

#region manual driving def

#region lift
def loop():
    while True:
        mot_lift_l_s = mot_lift_r_s = controller_1.axis2.position()*0.8
        deg = lift_inert.orientation(OrientationType.PITCH,DEGREES)
        
        if math.fabs(deg) > 1 and balance.status:
            print(1)
            mot_lift_r_s = max(-100, min(mot_lift_r_s-deg*2, 100))
            mot_lift_l_s = max(-100, min(mot_lift_l_s+deg*2, 100))

        mot_lift_l.set_velocity(mot_lift_l_s, PERCENT)
        mot_lift_r.set_velocity(mot_lift_r_s, PERCENT)

        wait(REFRESH, SECONDS)

Thread(loop)
#endregion lift

def forback():
    mot_lf_s = mot_lb_s = mot_rf_s = mot_rb_s = controller_1.axis3.position()
    return mot_lf_s, mot_lb_s, mot_rf_s, mot_rb_s
#
def turne(mot_lf_s, mot_lb_s, mot_rf_s, mot_rb_s):
    ax4 = controller_1.axis4.position()
    mot_lf_s += ax4
    mot_lb_s += ax4
    mot_rf_s -= ax4
    mot_rb_s -= ax4
    return mot_lf_s, mot_lb_s, mot_rf_s, mot_rb_s
#
def valuecheck(mot_lf_s, mot_lb_s, mot_rf_s, mot_rb_s):
    mot_lf_s = max(-100, min(mot_lf_s, 100))
    mot_lb_s = max(-100, min(mot_lb_s, 100))
    mot_rf_s = max(-100, min(mot_rf_s, 100))
    mot_rb_s = max(-100, min(mot_rb_s, 100))
    return mot_lf_s, mot_lb_s, mot_rf_s, mot_rb_s
#endregion manual driving def

#region autonomous funcs
"""
def aut_stop():
    mot_lf.set_velocity(0, PERCENT)
    mot_lb.set_velocity(0, PERCENT)
    mot_rf.set_velocity(0, PERCENT)
    mot_rb.set_velocity(0, PERCENT)

def aut_front(b, a=1):
    if b == -1:
        mot_lf.set_velocity(SPEED*a, PERCENT)
        mot_lb.set_velocity(SPEED*a, PERCENT)
        mot_rf.set_velocity(SPEED*a, PERCENT)
        mot_rb.set_velocity(SPEED*a, PERCENT)
        return
    mot_lf.set_velocity(SPEED*a, PERCENT)
    mot_lb.set_velocity(SPEED*a, PERCENT)
    mot_rf.set_velocity(SPEED*a, PERCENT)
    mot_rb.set_velocity(SPEED*a, PERCENT)

    
        
    aut_stop()

def aut_turn(b):
    if inert.orientation(OrientationType.YAW, DEGREES)<b:
        a = 1
    else:
        a = -1
    mot_lf.set_velocity(SPEED*a, PERCENT)
    mot_lb.set_velocity(SPEED*a, PERCENT)
    mot_rf.set_velocity(-1*SPEED*a, PERCENT)
    mot_rb.set_velocity(-1*SPEED*a, PERCENT)
    if a == 1:
        while inert.orientation(OrientationType.YAW, DEGREES)+10<b:
            pass
    else:
        while inert.orientation(OrientationType.YAW, DEGREES)>10+b:
            pass
    aut_stop()
"""
#endregion autonomous funcs 



#not sure if works needs to be chcked
def autonomous(): 
    for line in data1:
        mot_lf_s, mot_lb_s, mot_rf_s, mot_rb_s, mot_brings_s, mot_conv_s = line
        mot_lf.set_velocity(mot_lf_s,  PERCENT)
        mot_lb.set_velocity(mot_lb_s, PERCENT)
        mot_rf.set_velocity(mot_rf_s, PERCENT)
        mot_rb.set_velocity(mot_rb_s, PERCENT) #setting them to motos
        print(str([mot_lf_s, mot_lb_s, mot_rf_s, mot_rb_s, mot_brings_s, mot_conv_s])+",")
        wait(0.04, SECONDS)

def driver_control():
    while True:
        mot_lf_s, mot_lb_s, mot_rf_s, mot_rb_s = valuecheck(*turne(*forback())) # getting motor speeds

        #region slow ##############CHANGE BUTTONS
        if slow.status:
            mot_lf_s *= 0.5
            mot_lb_s *= 0.5
            mot_rf_s *= 0.5
            mot_rb_s *= 0.5
        #endregion slow ##############CHANGE BUTTONS
        
        #print(str([mot_lf_s, mot_lb_s, mot_rf_s, mot_rb_s, mot_brings_s, mot_conv_s])+",")

        mot_lf.set_velocity(mot_lf_s,  PERCENT)
        mot_lb.set_velocity(mot_lb_s, PERCENT)
        mot_rf.set_velocity(mot_rf_s, PERCENT)
        mot_rb.set_velocity(mot_rb_s, PERCENT) #setting them to motos

        controller_1.screen.set_cursor(1, 1)
        wait(0.04, SECONDS)



competition = Competition(driver_control, autonomous)
