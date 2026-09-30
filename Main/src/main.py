#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain=Brain()
# Used ports:1, 6, 11, 12, 16, 17, 18, 19, 20
# Robot configuration code
mot_lf = Motor(Ports.PORT12, GearSetting.RATIO_18_1, True)
mot_rf = Motor(Ports.PORT16, GearSetting.RATIO_18_1, False)
mot_lb = Motor(Ports.PORT18, GearSetting.RATIO_18_1, True)
mot_rb = Motor(Ports.PORT17, GearSetting.RATIO_18_1, False)
mot_intake = Motor(Ports.PORT19, GearSetting.RATIO_18_1, False)
controller_1 = Controller(PRIMARY)
lift_inert = Inertial(Ports.PORT11)
mot_lift_l = Motor(Ports.PORT6, GearSetting.RATIO_18_1, True)
mot_lift_r = Motor(Ports.PORT20, GearSetting.RATIO_18_1, False)
drive_inert = Inertial(Ports.PORT1)
cam = AiVision(Ports.PORT2, AiVision.ALL_TAGS)



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

#endregion data

SPEED = 30
REFRESH_IN_HERTZ = 7 #--> 5 a second
REFRESH = 1/REFRESH_IN_HERTZ

#region classes
class Togglable():
    def __init__(self, status):
        self.status = status
    def toggle(self):
        self.status = not self.status

def push_toggle():
    if not push.status:
        mot_lf.set_stopping(HOLD)
        mot_rf.set_stopping(HOLD)
        mot_lb.set_stopping(HOLD)
        mot_rb.set_stopping(HOLD)
    else: 
        mot_lf.set_stopping(COAST)
        mot_rf.set_stopping(COAST)
        mot_lb.set_stopping(COAST)
        mot_rb.set_stopping(COAST)
    push.toggle()

balance = Togglable(False)
controller_1.buttonY.pressed(balance.toggle)

slow = Togglable(False)
controller_1.buttonB.pressed(slow.toggle)

backwards = Togglable(False)
controller_1.buttonX.pressed(backwards.toggle)

push = Togglable(False)
controller_1.buttonDown.pressed(push_toggle)
#endregion classes

#region motor config
mot_lf.set_velocity(0, PERCENT)
mot_lb.set_velocity(0, PERCENT)
mot_rf.set_velocity(0, PERCENT)
mot_rb.set_velocity(0, PERCENT)
mot_lift_l.set_velocity(0, PERCENT)
mot_lift_r.set_velocity(0, PERCENT)
mot_intake.set_velocity(0, PERCENT)

mot_lift_l.set_stopping(HOLD)
mot_lift_r.set_stopping(HOLD)


mot_lf.spin(FORWARD)
mot_lb.spin(FORWARD)
mot_rf.spin(FORWARD)
mot_rb.spin(FORWARD)
mot_lift_l.spin(FORWARD)
mot_lift_r.spin(FORWARD)
mot_intake.spin(FORWARD)


lift_inert.calibrate()
lift_inert.set_rotation(0, DEGREES)
lift_inert.calibrate()
lift_inert.set_rotation(0, DEGREES)
lift_inert.set_heading(0, DEGREES)
wait(30, MSEC)
#endregion motor config

#region display
def prt():
    while True:
        controller_1.screen.clear_screen()
        controller_1.screen.set_cursor(1, 1)
        controller_1.screen.print("BACKWARDS: " + str(backwards.status))
        controller_1.screen.set_cursor(2, 1)
        controller_1.screen.print("BALANCING: " + str(balance.status))
        controller_1.screen.set_cursor(3, 1)
        controller_1.screen.print("PUSH: " + str(push.status))

        wait(REFRESH/1.5, SECONDS)
Thread(prt)
#endregion display

#region display2
def prt2():
    brain.screen.set_font(FontType.PROP20)
    brain.screen.set_fill_color(Color.BLUE)
    while True:
        brain.screen.clear_screen(Color.BLUE)
        brain.screen.set_cursor(1, 1)
        brain.screen.print("BATTERY: " + str(brain.battery.capacity()))
        brain.screen.set_cursor(2, 1)
        brain.screen.print("BACKWARDS: " + str(backwards.status))
        brain.screen.set_cursor(3, 1)
        brain.screen.print("BALANCING: " + str(balance.status))
        brain.screen.set_cursor(4, 1)
        brain.screen.print("PUSH: " + str(push.status))
        brain.screen.set_cursor(5, 1)
        brain.screen.print("SLOW: " + str(slow.status))
        brain.screen.set_cursor(6, 1)
        brain.screen.print("TEMP LF: " + str(mot_lf.temperature(PERCENT)) + "   TORQ LF: " + str(mot_lf.torque(TorqueUnits.NM)))
        brain.screen.set_cursor(7, 1)
        brain.screen.print("TEMP LB: " + str(mot_lb.temperature(PERCENT)) + "   TORQ LF: " + str(mot_lf.torque(TorqueUnits.NM)))
        brain.screen.set_cursor(8, 1)
        brain.screen.print("TEMP RF: " + str(mot_rf.temperature(PERCENT)) + "   TORQ LF: " + str(mot_lf.torque(TorqueUnits.NM)))
        brain.screen.set_cursor(9, 1)
        brain.screen.print("TEMP RB: " + str(mot_rb.temperature(PERCENT)) + "   TORQ LF: " + str(mot_lf.torque(TorqueUnits.NM)))
        brain.screen.set_cursor(10, 1)
        brain.screen.print("TEMP LIFT L: " + str(mot_lift_l.temperature(PERCENT)) + "   TORQ LIFT L: " + str(mot_lift_l.torque(TorqueUnits.NM)))
        brain.screen.set_cursor(11, 1)
        brain.screen.print("TEMP LIFT R: " + str(mot_lift_r.temperature(PERCENT)) + "   TORQ LIFT R: " + str(mot_lift_r.torque(TorqueUnits.NM)))
        wait(REFRESH/1.5, SECONDS)
Thread(prt2)
#endregion display2

#region lift
def lift():
    while True:
        mot_lift_l_s = mot_lift_r_s = controller_1.axis2.position()*0.8
        deg = lift_inert.orientation(OrientationType.PITCH,DEGREES)
        
        if math.fabs(deg) > 1 and balance.status:
            mot_lift_r_s = max(-100, min(mot_lift_r_s-deg*2, 100))
            mot_lift_l_s = max(-100, min(mot_lift_l_s+deg*2, 100))

        mot_lift_l.set_velocity(mot_lift_l_s, PERCENT)
        mot_lift_r.set_velocity(mot_lift_r_s, PERCENT)

        wait(REFRESH, SECONDS)

Thread(lift)
#endregion lift

#region intake
def intake():
    while True:
        speed = 0
        if controller_1.buttonR1.pressing():
            speed = -100
        elif controller_1.buttonR2.pressing():
            speed = 100
        mot_intake.set_velocity(speed, PERCENT)
        wait(REFRESH, SECONDS)

Thread(intake)
#endregion intake

#region manual driving def
def forback(stat):
    a=1
    if stat: a=-1
    mot_l_s = mot_r_s = controller_1.axis3.position()*a
    return mot_l_s, mot_r_s
#
def turne(mot_l_s, mot_r_s):
    ax4 = controller_1.axis4.position()
    mot_l_s += ax4
    mot_r_s -= ax4
    return mot_l_s, mot_r_s
#
def valuecheck(mot_l_s, mot_r_s):
    mot_l_s = max(-100, min(mot_l_s, 100))
    mot_r_s = max(-100, min(mot_r_s, 100))
    return mot_l_s, mot_r_s
#endregion manual driving def

#region autonomous funcs
def aut_stop():
    mot_lf.set_velocity(0, PERCENT)
    mot_lb.set_velocity(0, PERCENT)
    mot_rf.set_velocity(0, PERCENT)
    mot_rb.set_velocity(0, PERCENT)

def aut_front(b, a=1):
    mot_lf.set_velocity(SPEED*a, PERCENT)
    mot_lb.set_velocity(SPEED*a, PERCENT)
    mot_rf.set_velocity(SPEED*a, PERCENT)
    mot_rb.set_velocity(SPEED*a, PERCENT)
    if b == -1:
        return
    """if b == -2:
        while not something:
            pass
        aut_stop()
        return"""

    wait(b, SECONDS)
    aut_stop()

def aut_turn(b):
    if drive_inert.orientation(OrientationType.YAW, DEGREES)<b:
        a = 1
    else:
        a = -1
    mot_lf.set_velocity(SPEED*a, PERCENT)
    mot_lb.set_velocity(SPEED*a, PERCENT)
    mot_rf.set_velocity(-1*SPEED*a, PERCENT)
    mot_rb.set_velocity(-1*SPEED*a, PERCENT)
    if a == 1:
        while drive_inert.orientation(OrientationType.YAW, DEGREES)+10<b:
            pass
    else:
        while drive_inert.orientation(OrientationType.YAW, DEGREES)-10>b:
            pass
    aut_stop()

#endregion autonomous funcs 


#not sure if works needs to be chcked
def autonomous(): 
    """for line in data1:
        mot_lf_s, mot_lb_s, mot_rf_s, mot_rb_s, mot_brings_s, mot_conv_s = line
        mot_lf.set_velocity(mot_lf_s,  PERCENT)
        mot_lb.set_velocity(mot_lb_s, PERCENT)
        mot_rf.set_velocity(mot_rf_s, PERCENT)
        mot_rb.set_velocity(mot_rb_s, PERCENT) #setting them to motos
        print(str([mot_lf_s, mot_lb_s, mot_rf_s, mot_rb_s, mot_brings_s, mot_conv_s])+",")
        wait(0.04, SECONDS)"""
    pass

    
def driver_control():
    while True:
        mot_l_s, mot_r_s = valuecheck(*turne(*forback(backwards.status))) # getting motor speeds

        #region slow
        if slow.status:
            mot_l_s *= 0.5
            mot_r_s *= 0.5
        #endregion slow
        
        #print(str([mot_lf_s, mot_lb_s, mot_rf_s, mot_rb_s, mot_brings_s, mot_conv_s])+",")

        mot_lf.set_velocity(mot_l_s,  PERCENT)
        mot_lb.set_velocity(mot_l_s, PERCENT)
        mot_rf.set_velocity(mot_r_s, PERCENT)
        mot_rb.set_velocity(mot_r_s, PERCENT) #setting them to motos

        controller_1.screen.set_cursor(1, 1)
        wait(0.04, SECONDS)


competition = Competition(driver_control, autonomous)
