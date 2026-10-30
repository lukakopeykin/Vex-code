#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain=Brain()
# Used ports:1, 2, 6, 11, 12, 13, 16, 17, 18, 19, 20
# Robot configuration code
mot_lf = Motor(Ports.PORT20, GearSetting.RATIO_18_1, True)
mot_rf = Motor(Ports.PORT18, GearSetting.RATIO_18_1, False)
mot_lb = Motor(Ports.PORT19, GearSetting.RATIO_18_1, True)
mot_rb = Motor(Ports.PORT17, GearSetting.RATIO_18_1, False)
mot_intake = Motor(Ports.PORT9, GearSetting.RATIO_18_1, False)
controller_1 = Controller(PRIMARY)
lift_inert = Inertial(Ports.PORT11)
mot_lift_l = Motor(Ports.PORT16, GearSetting.RATIO_18_1, True)
mot_lift_r = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
drive_inert = Inertial(Ports.PORT5)
cam = AiVision(Ports.PORT6, AiVision.ALL_TAGS)
rot_sens = Rotation(Ports.PORT15, False)
mot_grab = Motor(Ports.PORT12, GearSetting.RATIO_18_1, True)
dist_f = Distance(Ports.PORT2)
dist_l = Distance(Ports.PORT3)




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
REFRESH_IN_HERTZ = 7 #--> 7 a second
REFRESH = 1/REFRESH_IN_HERTZ

#region classes
class Togglable():
    def __init__(self, status):
        self.status = status
    def toggle(self):
        self.status = not self.status

def push_toggle():
    push.toggle()
    if push.status:
        mot_lf.set_stopping(HOLD)
        mot_rf.set_stopping(HOLD)
        mot_lb.set_stopping(HOLD)
        mot_rb.set_stopping(HOLD)
    else: 
        mot_lf.set_stopping(COAST)
        mot_rf.set_stopping(COAST)
        mot_lb.set_stopping(COAST)
        mot_rb.set_stopping(COAST)
    

def tilt_toggle():
    tilt.toggle()
    if tilt.status:
        mot_intake.set_stopping(COAST)
    else: 
        mot_intake.set_stopping(COAST)
    

balance = Togglable(True)
controller_1.buttonY.pressed(balance.toggle)

slow = Togglable(False)
controller_1.buttonB.pressed(slow.toggle)

backwards = Togglable(False)
controller_1.buttonX.pressed(backwards.toggle)

parttime = Togglable(False)
controller_1.buttonUp.pressed(parttime.toggle)

push = Togglable(False)
controller_1.buttonDown.pressed(push_toggle)

tilt = Togglable(False)
controller_1.buttonLeft.pressed(tilt_toggle)
#endregion classes

#region device config
#velocity
mot_lf.set_velocity(0, PERCENT)
mot_lb.set_velocity(0, PERCENT)
mot_rf.set_velocity(0, PERCENT)
mot_rb.set_velocity(0, PERCENT)
mot_lift_l.set_velocity(0, PERCENT)
mot_lift_r.set_velocity(0, PERCENT)
mot_intake.set_velocity(0, PERCENT)
mot_grab.set_velocity(0, PERCENT)

#stopping
mot_lift_l.set_stopping(HOLD)
mot_lift_r.set_stopping(HOLD)
mot_grab.set_stopping(COAST)

#spin
mot_lf.spin(FORWARD)
mot_lb.spin(FORWARD)
mot_rf.spin(FORWARD)
mot_rb.spin(FORWARD)
mot_lift_l.spin(FORWARD)
mot_lift_r.spin(FORWARD)
mot_intake.spin(FORWARD)
mot_grab.spin(FORWARD)

#max torque
mot_grab.set_max_torque(40, PERCENT)

#sensors
lift_inert.calibrate()
lift_inert.set_rotation(0, DEGREES)
drive_inert.calibrate()
drive_inert.set_rotation(0, DEGREES)
drive_inert.set_heading(0, DEGREES)
rot_sens.reset_position()

wait(30, MSEC)
#endregion device config

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
    brain.screen.set_font(FontType.MONO20)
    brain.screen.set_fill_color(Color.BLUE)
    names = ["lf", "rf", "lb", "rb", "lfl", "lfr", "int", "grb"]
    motors = [mot_lf, mot_rf, mot_lb, mot_rb, mot_lift_l, mot_lift_r, mot_intake, mot_grab]
    while True:
        brain.screen.clear_screen(Color.BLUE)

        for i in motors:
            if i.temperature() > 50:
                brain.screen.clear_screen(Color.YELLOW)

        brain.screen.set_cursor(2, 1)
        brain.screen.print("temp:")
        brain.screen.set_cursor(3, 1)
        brain.screen.print("torq:")

        # Row 1: labels (starting after "temp:" which is 5 chars)
        for i in range(len(names)):
            brain.screen.set_cursor(1, 6 + i * 5)
            brain.screen.print(names[i])

        # Row 2: temperatures (aligned under the names)
        for i in range(len(motors)):
            brain.screen.set_cursor(2, 6 + i * 5)
            brain.screen.print(str(round(motors[i].temperature(), 1)))

        # Row 3: torques (rounded to 2 decimals)
        for i in range(len(motors)):
            brain.screen.set_cursor(3, 6 + i * 5)
            brain.screen.print(str(round(motors[i].torque(), 2)))


        brain.screen.set_cursor(4, 1)
        brain.screen.print("BATTERY: " + str(brain.battery.capacity()))
        brain.screen.set_cursor(5, 1)
        brain.screen.print("BACKWARDS: " + str(backwards.status))
        brain.screen.set_cursor(6, 1)
        brain.screen.print("BALANCING: " + str(balance.status))
        brain.screen.set_cursor(7, 1)
        brain.screen.print("PUSH: " + str(push.status))
        brain.screen.set_cursor(8, 1)
        brain.screen.print("SLOW: " + str(slow.status))
        brain.screen.set_cursor(9, 1)
        brain.screen.print("TILT: " + str(tilt.status))
        wait(REFRESH/1.5, SECONDS)
Thread(prt2)
#endregion display2

#region lift
def lift():
    while True:
        mot_lift_l_s = mot_lift_r_s = controller_1.axis2.position()* -1
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
        elif tilt.status and 355 > rot_sens.position()%360 > 5:
            speed = max(-100, -1*math.floor((360-rot_sens.position()%360)**2/1200))
        elif not tilt.status and (210 < rot_sens.position()%360 or rot_sens.position()%360 < 110):
            speed = -15
        mot_intake.set_velocity(speed, PERCENT)
        wait(REFRESH, SECONDS)

Thread(intake)
#endregion intake

#region grabber

def grabber():
    while True:
        speed = 0
        if controller_1.buttonL1.pressing():
            speed = -75
        elif controller_1.buttonL2.pressing():
            speed = 75
        mot_grab.set_velocity(speed, PERCENT)
        wait(REFRESH, SECONDS)

Thread(grabber)
#endregion grabber

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

def aut_front(b, a=1, c=0):
    mot_lf.set_velocity(SPEED*a, PERCENT)
    mot_lb.set_velocity(SPEED*a, PERCENT)
    mot_rf.set_velocity(SPEED*a, PERCENT)
    mot_rb.set_velocity(SPEED*a, PERCENT)
    if b == 0:
        return
    if b == 1:
        while not dist_f.object_distance()*a < c*a:
            wait(REFRESH, SECONDS)
        aut_stop()
        return


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
            wait(REFRESH, SECONDS)
    else:
        while drive_inert.orientation(OrientationType.YAW, DEGREES)-10>b:
            wait(REFRESH, SECONDS)
    aut_stop()

def aut_lift(pos):
    if mot_lift_l.position()<pos:
        a = 1
    else:
        a = -1
    
    mot_lift_l.set_velocity(SPEED*a, PERCENT)
    mot_lift_r.set_velocity(SPEED*a, PERCENT)
    if a == 1:
        while mot_lift_l.position()+10<pos:
            wait(REFRESH, SECONDS)
    else:
        while mot_lift_l.position()-10>pos:
            wait(REFRESH, SECONDS)

    mot_lift_l.set_velocity(0, PERCENT)
    mot_lift_r.set_velocity(0, PERCENT)
    
def aut_claw(a=1):
    if a == 1:
        mot_grab.set_velocity(-75)
    elif a == 0:
        mot_grab.set_velocity(75)
        wait(0.5, SECONDS)
        mot_grab.set_velocity(0)

        
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
    aut_claw(1)
    aut_front(2, -1, 100)#getting away from the wall
    aut_lift(50)#lifting the lift a bit
    aut_front(2, 2, 10)#toggling ppossibly a = 2
    aut_front(2, -1, 600)#getting away
    aut_turn(90)
    aut_front(2, 1, 1200)#going towards red tower
    aut_lift(10)#lowering the pin
    aut_claw(0)
    aut_front(2, -1, 2000)#going away from tower
    aut_turn(0)
    aut_front(2, -1, 1200)
    aut_turn(90)
    aut_front(2, 1, 1200)#going towards a pin # possibly until a sensor o the grabber, then b=3
    aut_claw(1)
    aut_lift(50)
    aut_front(2, 1, 1100)#a bit front
    aut_front(2, 1, 600)#going to the tower
    aut_lift(30)#lowering the lift on top of the tower
    aut_turn(0)
    aut_lift(50)#lifting the lift on top of the tower

    ### stop of the 15 sec

    aut_front(2, -1, 1200)
    aut_turn(45)
    


















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