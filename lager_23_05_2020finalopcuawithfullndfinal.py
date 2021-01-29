from opcua import Server, ua, uamethod, Client
from pyModbusTCP.client import ModbusClient
import time
from datetime import datetime
import uuid
import os, time
from OurProductDataType_Lib import OurProduct
from OurProductDataType_Lib import DataTypeDictionaryBuilder, get_ua_class

# assigning inputs to variables
safety_ok = False


# for assigning variables to inputs
def read_sensors():
    global reg, x_allowed, x_done, y_allowed, y_done, grip_up, grip_down, grip_open, grip_closed, grip_closed, product_detect, safety_ok
    reg = c.read_holding_registers(0, 1)
    x_allowed = (reg[0] & (1 << 0) == (1 << 0))
    x_done = ((reg[0] & (1 << 1)) == (1 << 1))
    y_allowed = ((reg[0] & (1 << 2)) == (1 << 2))
    y_done = ((reg[0] & (1 << 3)) == (1 << 3))
    grip_up = ((reg[0] & (1 << 4)) == (1 << 4))
    grip_down = ((reg[0] & (1 << 5)) == (1 << 5))
    grip_open = ((reg[0] & (1 << 6)) == (1 << 6))
    grip_closed = ((reg[0] & (1 << 7)) == (1 << 7))
    product_detect = ((reg[0] & (1 << 8)) == (1 << 8))
    safety_ok = ((reg[0] & (1 << 9)) == (1 << 9))


# assigning output to variables
light = 1 << 15
close_gripper = 1 << 13
open_gripper = 1 << 12
move_up = 1 << 10
move_down = 1 << 11
start_x = 1 << 4
start_y = 1 << 9
allow_xy = 1 << 14
X = [(0 << 0), (1 << 0), (1 << 1), (1 << 0) | (1 << 1), (1 << 2), (1 << 2) | (1 << 0), (1 << 2) | (1 << 1),
     (1 << 2) | (1 << 1) | (1 << 0), (1 << 3), (1 << 3) | (1 << 0), (1 << 3) | (1 << 1), (1 << 3) | (1 << 1) | (1 << 0),
     (1 << 3) | (1 << 2)]
Y = [(1 << 5), (1 << 6), (1 << 5) | (1 << 6), (1 << 7), (1 << 7) | (1 << 5), (1 << 7) | (1 << 6),
     (1 << 7) | (1 << 6) | (1 << 5), (1 << 8), (1 << 8) | (1 << 5), (1 << 8) | (1 << 6), (1 << 8) | (1 << 6) | (1 << 5),
     (1 << 8) | (1 << 7)]

# global variables used in functions
placesilver = False
home = False
red1 = [True] * 8
red2 = [True] * 8

black1 = [True] * 8
black2 = [True] * 8

silver1 = [True] * 8
silver2 = [True] * 8

red_wp = 0
black_wp = 0
silver_wp = 0

RED_STORE = False
BLACK_STORE = False
SILVER_STORE = False

orderid = uuid
delivery = "Warehouse"
ordertime = uuid
partclassid = uuid
Time = datetime.now()
partid = uuid
our_product=[delivery, orderid, ordertime, partclassid,partid,Time]

ORDERID1 = [uuid] * 8
DELIVERY1 = ["warehouse"] * 8
ORDERTIME1 = [datetime.now()] * 8
PARTCLASS1 = [uuid] * 8
TIME1 = [datetime.now()] * 8
PARTID1 = [uuid] * 8

ORDERID2 = [uuid] * 8
DELIVERY2 = ["warehouse"] * 8
ORDERTIME2 = [uuid] * 8
PARTCLASS2 = [uuid] * 8
TIME2 = [datetime.now()] * 8
PARTID2 = [uuid] * 8

BORDERID1 = [uuid] * 8
BDELIVERY1 = ["warehouse"] * 8
BORDERTIME1 = [datetime.now()] * 8
BPARTCLASS1 = [uuid] * 8
BTIME1 = [datetime.now()] * 8
BPARTID1 = [uuid] * 8

BORDERID2 = [uuid] * 8
BDELIVERY2 = ["warehouse"] * 8
BORDERTIME2 = [uuid] * 8
BPARTCLASS2 = [uuid] * 8
BTIME2 = [datetime.now()] * 8
BPARTID2 = [uuid] * 8

SORDERID1 = [uuid] * 8
SDELIVERY1 = ["warehouse"] * 8
SORDERTIME1 = [datetime.now()] * 8
SPARTCLASS1 = [uuid] * 8
STIME1 = [datetime.now()] * 8
SPARTID1 = [uuid] * 8

SORDERID2 = [uuid] * 8
SDELIVERY2 = ["warehouse"] * 8
SORDERTIME2 = [uuid] * 8
SPARTCLASS2 = [uuid] * 8
STIME2 = [datetime.now()] * 8
SPARTID2 = [uuid] * 8

STORAGE=True
# homing function
def homing():
    read_sensors()
    global home
    if safety_ok != home:
        c.write_multiple_registers(384, [allow_xy | light | open_gripper | move_up])
        time.sleep(10)
        read_sensors()
        if grip_up and grip_open:
            c.write_multiple_registers(384, [allow_xy | start_x | start_y | light])
            time.sleep(20)
            read_sensors()
    if grip_up and grip_open and x_allowed and y_allowed:
        home = True
    #wserver.status.set_value(True)


# Initial checking for the number of products
def product_count():
    for x in range(2):
        for y in range(8):
            read_sensors()
            if safety_ok and home:
                i = x + 1
                c.write_multiple_registers(384, [allow_xy | light | X[i] | Y[y]])
                time.sleep(1)
                c.write_multiple_registers(384, [allow_xy | light | X[i] | Y[y] | start_x | start_y])
                time.sleep(3)
                read_sensors()
                if product_detect:  # for getting the locations where the product is currently present
                    if x == 0 and product_detect:
                        red1[y] = False
                    elif x == 1 and product_detect:
                        red2[y] = False
                    else:
                        pass
                else:
                    pass
    for x in range(2):
        for y in range(8):
            read_sensors()
            i = x + 3
            if safety_ok:
                c.write_multiple_registers(384, [allow_xy | light | X[i] | Y[y]])
                time.sleep(1)
                c.write_multiple_registers(384, [allow_xy | light | X[i] | Y[y] | start_x | start_y])
                time.sleep(3)
                read_sensors()
                if product_detect:
                    if x == 0 and product_detect:
                        black1[y] = False
                    elif x == 1 and product_detect:
                        black2[y] = False
                    else:
                        pass
                else:
                    pass
    for x in range(2):
        for y in range(8):
            read_sensors()
            i = x + 6
            if safety_ok:
                c.write_multiple_registers(384, [allow_xy | light | X[i] | Y[y]])
                time.sleep(1)
                c.write_multiple_registers(384, [allow_xy | light | X[i] | Y[y] | start_x | start_y])
                time.sleep(3)
                read_sensors()
                if product_detect:
                    if x == 0 and product_detect:
                        silver1[y] = False
                    elif x == 1 and product_detect:
                        silver2[y] = False
                    else:
                        pass
                else:
                    pass


# function for getting the stock info
def get_stock():
    global red_wp, black_wp, silver_wp
    for x in range(8):
        if not red1[x]:
            red_wp += 1
        elif not red2[x]:
            red_wp += 1
        else:
            pass
    for y in range(8):
        if not black1[y]:
            black_wp += 1
        elif not black2[y]:
            black_wp += 1
        else:
            pass
    for z in range(8):
        if not silver1[z]:
            silver_wp += 1
        elif not silver2[z]:
            silver_wp += 1
        else:
            pass

    wserver.redstock.set_value(red_wp)
    wserver.silverstock.set_value(silver_wp)

    wserver.blackstock.set_value(black_wp)


# function for storing the Red workpiece

def store_red():
    global X, Y, red1, red2,our_product, PARTID1, PARTID2, ORDERID2, DELIVERY2, ORDERTIME2, PARTCLASS2, TIME2, ORDERID1, DELIVERY1, ORDERTIME1, PARTCLASS1, TIME1
    global STORAGE
    def store():
        c.write_multiple_registers(384, [allow_xy | light | X[10] | Y[9]])
        time.sleep(1)
        c.write_multiple_registers(384, [allow_xy | light | X[10] | Y[9] | move_up | open_gripper])
        time.sleep(3)
        read_sensors()
        if safety_ok and grip_open and grip_up and home:
            c.write_multiple_registers(384, [allow_xy | light | X[10] | Y[9] | start_x | start_y])
            time.sleep(3)
            c.write_multiple_registers(384, [allow_xy | move_down | light])
            time.sleep(2)
            read_sensors()
        if grip_down and home:
            c.write_multiple_registers(384, [allow_xy | close_gripper | light])
            time.sleep(2)
            read_sensors()
        if grip_closed and grip_down and home:
            c.write_multiple_registers(384, [allow_xy | move_up | light])
            time.sleep(3)
            read_sensors()
        if grip_up and home:
            c.write_multiple_registers(384, [allow_xy | X[i] | Y[x] | light])
            time.sleep(2)
            c.write_multiple_registers(384, [allow_xy | X[i] | Y[x] | light | start_x | start_y])
            time.sleep(5)
            c.write_multiple_registers(384, [allow_xy | light | move_down])
            time.sleep(3)
            read_sensors()
        if grip_down and home:
            c.write_multiple_registers(384, [allow_xy | light | open_gripper])
            time.sleep(3)
            read_sensors()
        if grip_down and grip_open and home:
            c.write_multiple_registers(384, [allow_xy | light | move_up | open_gripper])
            time.sleep(3)

    for x in range(8):
        if red1[x]:
            red1[x] = False
            STORAGE=False
            ORDERID1[x] = orderid
            DELIVERY1[x] = delivery
            ORDERTIME1[x] = ordertime
            PARTCLASS1[x] = partclassid
            TIME1[x] = Time
            PARTID1[x] = partid
            i = 2
            store()
            time.sleep(3)
            tclinet.piece_received(our_product)
            STORAGE=True
            break
        elif red2[x]:
            red2[x] = False
            STORAGE = False
            ORDERID2[x] = orderid
            DELIVERY2[x] = delivery
            ORDERTIME2[x] = ordertime
            PARTCLASS2[x] = partclassid
            TIME2[x] = Time
            PARTID2[x] = partid
            i = 3
            store()
            time.sleep(3)
            tclinet.piece_received(our_product)
            STORAGE = True
            break
        else:
            pass


# Function to store Black
def store_black():
    global X, Y, black1, black2,our_product, BPARTID1, BPARTID2, BORDERID2, BDELIVERY2, BORDERTIME2, BPARTCLASS2, BTIME2, BORDERID1, BDELIVERY1, BORDERTIME1, BPARTCLASS1, BTIME1
    global STORAGE
    def bstore():
        c.write_multiple_registers(384, [allow_xy | light | X[10] | Y[9]])
        time.sleep(1)
        c.write_multiple_registers(384, [allow_xy | light | X[10] | Y[9] | move_up | open_gripper])
        time.sleep(3)
        read_sensors()
        if safety_ok and grip_open and grip_up and home:
            c.write_multiple_registers(384, [allow_xy | light | X[10] | Y[9] | start_x | start_y])
            time.sleep(3)
            c.write_multiple_registers(384, [allow_xy | move_down | light])
            time.sleep(2)
            read_sensors()
        if grip_down and home:
            c.write_multiple_registers(384, [allow_xy | close_gripper | light])
            time.sleep(2)
            read_sensors()
        if grip_closed and grip_down and home:
            c.write_multiple_registers(384, [allow_xy | move_up | light])
            time.sleep(3)
            read_sensors()
        if grip_up and home:
            c.write_multiple_registers(384, [allow_xy | X[i] | Y[x] | light])
            time.sleep(2)
            c.write_multiple_registers(384, [allow_xy | X[i] | Y[x] | light | start_x | start_y])
            time.sleep(5)
            c.write_multiple_registers(384, [allow_xy | light | move_down])
            time.sleep(3)
            read_sensors()
        if grip_down and home:
            c.write_multiple_registers(384, [allow_xy | light | open_gripper])
            time.sleep(3)
            read_sensors()
        if grip_down and grip_open and home:
            c.write_multiple_registers(384, [allow_xy | light | move_up | open_gripper])
            time.sleep(3)

    for x in range(8):
        if black1[x]:
            black1[x] = False
            STORAGE = False
            BORDERID1[x] = orderid
            BDELIVERY1[x] = delivery
            BORDERTIME1[x] = ordertime
            BPARTCLASS1[x] = partclassid
            BTIME1[x] = Time
            BPARTID1[x] = partid
            i = 4
            bstore()
            time.sleep(3)
            tclinet.piece_received(our_product)
            STORAGE = True
            break
        elif black2[x]:
            black2[x] = False
            STORAGE = False
            BORDERID2[x] = orderid
            BDELIVERY2[x] = delivery
            BORDERTIME2[x] = ordertime
            BPARTCLASS2[x] = partclassid
            BTIME1[x] = Time
            BPARTID1[x] = partid
            i = 5
            bstore()
            time.sleep(3)
            tclinet.piece_received(our_product)
            STORAGE = True
            break
        else:
            pass


# Function for storing the Silver Workpiece
def store_silver():
    global X, Y, silver1, silver2, SPARTID1, SPARTID2, SORDERID2, SDELIVERY2, SORDERTIME2, SPARTCLASS2, STIME2, SORDERID1, SDELIVERY1, SORDERTIME1, SPARTCLASS1, STIME1, our_product
    global STORAGE
    def sstore():
        c.write_multiple_registers(384, [allow_xy | light | X[10] | Y[9]])
        time.sleep(1)
        c.write_multiple_registers(384, [allow_xy | light | X[10] | Y[9] | move_up | open_gripper])
        time.sleep(3)
        read_sensors()
        if safety_ok and grip_open and grip_up and home:
            c.write_multiple_registers(384, [allow_xy | light | X[10] | Y[9] | start_x | start_y])
            time.sleep(3)
            c.write_multiple_registers(384, [allow_xy | move_down | light])
            time.sleep(2)
            read_sensors()
        if grip_down and home:
            c.write_multiple_registers(384, [allow_xy | close_gripper | light])
            time.sleep(2)
            read_sensors()
        if grip_closed and grip_down and home:
            c.write_multiple_registers(384, [allow_xy | move_up | light])
            time.sleep(3)
            read_sensors()
        if grip_up and home:
            c.write_multiple_registers(384, [allow_xy | X[i] | Y[x] | light])
            time.sleep(2)
            c.write_multiple_registers(384, [allow_xy | X[i] | Y[x] | light | start_x | start_y])
            time.sleep(5)
            c.write_multiple_registers(384, [allow_xy | light | move_down])
            time.sleep(3)
            read_sensors()
        if grip_down and home:
            c.write_multiple_registers(384, [allow_xy | light | open_gripper])
            time.sleep(3)
            read_sensors()
        if grip_down and grip_open and home:
            c.write_multiple_registers(384, [allow_xy | light | move_up | open_gripper])
            time.sleep(3)


    for x in range(8):
        if silver1[x]:
            silver1[x] = False
            STORAGE = False
            SORDERID1[x] = orderid
            SDELIVERY1[x] = delivery
            SORDERTIME1[x] = ordertime
            SPARTCLASS1[x] = partclassid
            STIME1[x] = Time
            SPARTID1[x] = partid
            i = 6
            sstore()
            time.sleep(3)
            tclinet.piece_received(our_product)
            STORAGE = True
            break
        elif silver2[x]:
            silver2[x] = False
            STORAGE = False
            SORDERID2[x] = orderid
            SDELIVERY2[x] = delivery
            SORDERTIME2[x] = ordertime
            SPARTCLASS2[x] = partclassid
            STIME2[x] = Time
            SPARTID2[x] = partid
            i = 7
            sstore()
            time.sleep(3)
            tclinet.piece_received(our_product)
            STORAGE = True
            break
        else:
            pass


# function for taking red
def take_red():
    global X, Y, red1, red2

    def red():
        c.write_multiple_registers(384, [allow_xy | light | X[i] | Y[x]])
        time.sleep(1)
        c.write_multiple_registers(384, [allow_xy | light | X[i] | Y[x] | move_up | open_gripper])
        time.sleep(3)
        read_sensors()
        if safety_ok and grip_open and grip_up and home:
            c.write_multiple_registers(384, [allow_xy | light | X[i] | Y[x] | start_x | start_y])
            time.sleep(3)
            c.write_multiple_registers(384, [allow_xy | move_down | light])
            time.sleep(2)
            read_sensors()
        if grip_down and home:
            c.write_multiple_registers(384, [allow_xy | close_gripper | light])
            time.sleep(2)
            read_sensors()
        if grip_closed and grip_down and home:
            c.write_multiple_registers(384, [allow_xy | move_up | light])
            time.sleep(3)
            read_sensors()
        if grip_up and home:
            c.write_multiple_registers(384, [allow_xy | X[10] | Y[9] | light])
            time.sleep(2)
            c.write_multiple_registers(384, [allow_xy | X[10] | Y[9] | light | start_x | start_y])
            time.sleep(5)
            c.write_multiple_registers(384, [allow_xy | light | move_down])
            time.sleep(3)
            read_sensors()
        if grip_down and home:
            c.write_multiple_registers(384, [allow_xy | light | open_gripper])
            time.sleep(3)
            read_sensors()
        if grip_down and grip_open and home:
            c.write_multiple_registers(384, [allow_xy | light | move_up | open_gripper])
            time.sleep(3)

    for x in range(8):
        if not red1[x]:
            red1[x] = True
            i =2
            red()
            time.sleep(3)
            break
        elif not red2[x]:
            red2[x] = True
            i = 3
            red()
            time.sleep(3)
            break
        else:
            pass


# function for taking black
def take_black():
    global X, Y, black1, black2

    def black():
        c.write_multiple_registers(384, [allow_xy | light | X[i] | Y[x]])
        time.sleep(1)
        c.write_multiple_registers(384, [allow_xy | light | X[i] | Y[x] | move_up | open_gripper])
        time.sleep(3)
        read_sensors()
        if safety_ok and grip_open and grip_up and home:
            c.write_multiple_registers(384, [allow_xy | light | X[i] | Y[x] | start_x | start_y])
            time.sleep(3)
            c.write_multiple_registers(384, [allow_xy | move_down | light])
            time.sleep(2)
            read_sensors()
        if grip_down and home:
            c.write_multiple_registers(384, [allow_xy | close_gripper | light])
            time.sleep(2)
            read_sensors()
        if grip_closed and grip_down and home:
            c.write_multiple_registers(384, [allow_xy | move_up | light])
            time.sleep(3)
            read_sensors()
        if grip_up and home:
            c.write_multiple_registers(384, [allow_xy | X[10] | Y[9] | light])
            time.sleep(2)
            c.write_multiple_registers(384, [allow_xy | X[10] | Y[9] | light | start_x | start_y])
            time.sleep(5)
            c.write_multiple_registers(384, [allow_xy | light | move_down])
            time.sleep(3)
            read_sensors()
        if grip_down and home:
            c.write_multiple_registers(384, [allow_xy | light | open_gripper])
            time.sleep(3)
            read_sensors()
        if grip_down and grip_open and home:
            c.write_multiple_registers(384, [allow_xy | light | move_up | open_gripper])
            time.sleep(3)

    for x in range(8):
        if not black1[x]:
            black1[x] = True
            i = 4
            black()
            time.sleep(3)
            break
        elif not black2[x]:
            black2[x] = True
            i = 5
            black()
            time.sleep(3)
            break
        else:
            pass


# function for taking silver
def take_silver():
    global X, Y, silver1, silver2

    def silver():
        c.write_multiple_registers(384, [allow_xy | light | X[i] | Y[x]])
        time.sleep(1)
        c.write_multiple_registers(384, [allow_xy | light | X[i] | Y[x] | move_up | open_gripper])
        time.sleep(3)
        read_sensors()
        if safety_ok and grip_open and grip_up and home:
            c.write_multiple_registers(384, [allow_xy | light | X[i] | Y[x] | start_x | start_y])
            time.sleep(3)
            c.write_multiple_registers(384, [allow_xy | move_down | light])
            time.sleep(2)
            read_sensors()
        if grip_down and home:
            c.write_multiple_registers(384, [allow_xy | close_gripper | light])
            time.sleep(2)
            read_sensors()
        if grip_closed and grip_down and home:
            c.write_multiple_registers(384, [allow_xy | move_up | light])
            time.sleep(3)
            read_sensors()
        if grip_up and home:
            c.write_multiple_registers(384, [allow_xy | X[10] | Y[9] | light])
            time.sleep(2)
            c.write_multiple_registers(384, [allow_xy | X[10] | Y[9] | light | start_x | start_y])
            time.sleep(5)
            c.write_multiple_registers(384, [allow_xy | light | move_down])
            time.sleep(3)
            read_sensors()
        if grip_down and home:
            c.write_multiple_registers(384, [allow_xy | light | open_gripper])
            time.sleep(3)
            read_sensors()
        if grip_down and grip_open and home:
            c.write_multiple_registers(384, [allow_xy | light | move_up | open_gripper])
            time.sleep(3)

    for x in range(8):
        if not silver1[x]:
            silver1[x] = True
            i = 6
            silver()
            time.sleep(3)
            break
        elif not red2[x]:
            silver2[x] = True
            i = 7
            silver()
            time.sleep(3)
            break
        else:
            pass


def check_time():

    global red1, red2, TIME1, TIME2, ORDERID1, ORDERID2, PARTID1, PARTID2, DELIVERY1, DELIVERY2, PARTCLASS1, PARTCLASS2, ORDERTIME1, ORDERTIME2, BORDERID1, BORDERID2, BPARTID1, BPARTID2, BDELIVERY1, BDELIVERY2, BPARTCLASS1, BPARTCLASS2, BORDERTIME1, BORDERTIME2, SORDERID1, SORDERID2, SPARTID1, SPARTID2, SDELIVERY1, SDELIVERY2, SPARTCLASS1, SPARTCLASS2, SORDERTIME1, SORDERTIME2
    for x in range(8):
        if not red1[x]:
            if TIME1[x] <= (datetime.now()):

                if tclinet.askforfree():
                    take_red()
                    tclinet.call_CLIENT(ORDERID1[x], PARTID1[x], DELIVERY1[x], PARTCLASS1[x], TIME1[x], ORDERTIME1[x])
                break
            else:
                pass
        elif not red2[x]:
            if TIME2[x] <= (datetime.now()):
                if tclinet.askforfree():
                    take_red()
                    tclinet.call_CLIENT(ORDERID2[x], PARTID2[x], DELIVERY2[x], PARTCLASS2[x], TIME2[x], ORDERTIME2[x])
                break
            else:
                pass
        elif not black1[x]:
            if BTIME1[x] <= (datetime.now()):
                print("entered time IF")
                if tclinet.askforfree():
                    print(tclinet.askforfree())
                    take_black()
                    tclinet.call_CLIENT(BORDERID1[x], BPARTID1[x], BDELIVERY1[x], BPARTCLASS1[x], BTIME1[x], BORDERTIME1[x])
                break
            else:
                print(tclinet.askforfree())
                pass
        elif not black2[x]:
            if BTIME2[x] <= (datetime.now()):
                if tclinet.askforfree():
                    take_black()
                    tclinet.call_CLIENT(BORDERID2[x], BPARTID2[x], BDELIVERY2[x], BPARTCLASS2[x], BTIME2[x], BORDERTIME2[x])
                break
            else:
                pass
        elif not silver1[x]:
            if STIME1[x] <= (datetime.now()):
                print("entered time IF")
                if tclinet.askforfree():
                    take_silver()
                    time.sleep(2)
                    tclinet.call_CLIENT(SORDERID1[x], SPARTID1[x], SDELIVERY1[x], SPARTCLASS1[x], STIME1[x], SORDERTIME1[x])
                break
            else:
                pass
        elif not silver2[x]:
            if STIME2[x] <= (datetime.now()):
                if tclinet.askforfree():
                    take_silver()
                    time.sleep(2)
                    tclinet.call_CLIENT(SORDERID2[x], SPARTID2[x], SDELIVERY2[x], SPARTCLASS2[x], STIME2[x], SORDERTIME2[x])
                break
            else:
                pass


# OPCUA
@uamethod
def storageCheck(parent):
    global safety_ok, home, STORAGE
    if safety_ok and home and STORAGE:
        return "True"
    else:
        return "False"


@uamethod
def received_storage(parent, new_product):
    global orderid, delivery, ordertime, partclassid, Time, partid, RED_STORE, BLACK_STORE, SILVER_STORE,our_product
    print("dosomethingwithModule method called with parameters: ")
    print(new_product.DeliveryAddress)
    print(new_product.OrderID)
    print(new_product.OrderTime)
    print(new_product.PartClassID)
    print(new_product.PartID)
    print(new_product.PlannedDeliveryTime)
    print("*********************************************")
    print(new_product)
    our_product = new_product
    ncolor = new_product.PartClassID
    print(ncolor)
    orderid = new_product.OrderID
    delivery = new_product.DeliveryAddress
    ordertime = new_product.OrderTime
    partclassid = new_product.PartClassID
    Time = new_product.PlannedDeliveryTime
    partid = new_product.PartID

    if str(ncolor) == "d0a135f2-ac3a-485e-baff-b17f8ca32039":
        print('red')
        RED_STORE = True
        return "storing initiated"

    elif "e3d3e558-a086-48f3-8774-c103fe23fe6d" == str(ncolor):
        print('black')
        BLACK_STORE = True
        return "storing initiated"
    elif "1c2045df-a8aa-4899-bd7d-ed6dcedbc4ee" == str(ncolor):
        print('silver')
        SILVER_STORE = True
        return "storing initiated"
    return "done"


class OPCUA_Server(OurProduct):

    def __init__(self, endpoint, name):
        # Configuration
        print("Init", name, "...")
        self.name = name
        self.server = Server()
        self.my_namespace_name = 'http://hs-emden-leer.de/OurProduct/'
        self.my_namespace_idx = self.server.register_namespace(self.my_namespace_name)
        self.server.set_endpoint(endpoint)
        self.server.set_server_name(name)

        # Add new object - MyModule
        self.objects = self.server.get_objects_node()
        self.warehouse = self.objects.add_object(self.my_namespace_idx, "warehouse")

        # Specify input argument(s)
        self.create_our_product_type()
        inarg_ourproduct = ua.Argument()
        inarg_ourproduct.Name = "OurProduct"
        inarg_ourproduct.DataType = self.ourproduct_data.data_type
        inarg_ourproduct.ValueRank = -1
        inarg_ourproduct.ArrayDimensions = []
        inarg_ourproduct.Description = ua.LocalizedText("A new Product")

        # Specify output argument
        outarg_answer = ua.Argument()
        outarg_answer.Name = "Answer"
        outarg_answer.DataType = ua.NodeId(ua.ObjectIds.String)
        outarg_answer.ValueRank = -1
        outarg_answer.ArrayDimensions = []
        outarg_answer.Description = ua.LocalizedText("Here you can specify an answer")

        # Output Argument for status check
        outarg1_answer = ua.Argument()
        outarg1_answer.Name = "Answer"
        outarg1_answer.DataType = ua.NodeId(ua.ObjectIds.String)
        outarg1_answer.ValueRank = -1
        outarg1_answer.ArrayDimensions = []
        outarg1_answer.Description = ua.LocalizedText("Here you can specify an answer")

        # Add new method
        mymethod = self.warehouse.add_method(self.my_namespace_idx, "Received_store", received_storage,
                                             [inarg_ourproduct], [outarg_answer])
        fortransport = self.warehouse.add_method(self.my_namespace_idx, "storageCheck", storageCheck, [],
                                                 [outarg1_answer])
        self.redstock = self.warehouse.add_variable(self.my_namespace_idx, "fg_stockR",0)
        self.blackstock = self.warehouse.add_variable(self.my_namespace_idx, "fg_stockB",0)
        self.silverstock = self.warehouse.add_variable(self.my_namespace_idx, "fg_stockS",0)
        self.status = self.warehouse.add_variable(self.my_namespace_idx,"WH_status",False)

        self.redstock.set_read_only()
        self.blackstock.set_read_only()
        self.silverstock.set_read_only()
        self.status.set_read_only()


    def __enter__(self):
        # Start server
        global c
        print("Setup", self.name, "....")

        self.server.start()

        return self

    def __exit__(self, exc, exc_val, exc_tb):
        # Close server
        print("Closing", self.name, "....")
        self.server.stop()

class Transport_Client():

    def askforfree(self):
        client = Client("opc.tcp://192.168.200.160:40840")
        client.connect()
        mynamespace_idx = client.get_namespace_index("http://hs-emden-leer.de/OurProduct/")
        root = client.get_root_node()
        obj = root.get_child(["0:Objects", "{}:ForStorage".format(mynamespace_idx)])
        client.load_type_definitions()
        res = obj.call_method("{}:storageCheck".format(mynamespace_idx))
        client.disconnect()
        return res

    def piece_received(self,my_product):
        client = Client("opc.tcp://192.168.200.160:40840")
        client.connect()
        mynamespace_idx = client.get_namespace_index("http://hs-emden-leer.de/OurProduct/")
        root = client.get_root_node()
        obj = root.get_child(["0:Objects", "{}:ForStorage".format(mynamespace_idx)])
        client.load_type_definitions()
        t= obj.call_method("{}:storageReceived".format(mynamespace_idx), my_product)
        client.disconnect()
        return self

    def call_CLIENT(self,ORDER_ID, PART_ID, DELIVERY, PART_CLASS, TI_ME, ORDER_TIME):
        client = Client("opc.tcp://192.168.200.160:40840")
        client.connect()
        mynamespace_idx = client.get_namespace_index("http://hs-emden-leer.de/OurProduct/")
        root = client.get_root_node()
        obj = root.get_child(["0:Objects", "{}:ForStorage".format(mynamespace_idx)])
        client.load_type_definitions()
        data = get_ua_class('OurProduct')()

        data2 = get_ua_class('PathItem')()

        data2.NameOfStation = "Input"
        data2.PlannedStepNumber = 1
        data2.IsDoneSuccessful = True

        data3 = get_ua_class('PathItem')()

        data3.NameOfStation = "Machining"
        data3.PlannedStepNumber = 2
        data3.IsDoneSuccessful = True

        data.DeliveryAddress = DELIVERY
        data.OrderID = ORDER_ID
        data.OrderTime = ORDER_TIME
        data.PartClassID = PART_CLASS
        data.PartID = PART_ID
        data.PathStack = data2, data2
        data.PlannedDeliveryTime = TI_ME

        res = obj.call_method("{}:storagePass".format(mynamespace_idx), data)
        print("Method answer is: ", res)
        client.disconnect()


        return self



#class SubHandler(object):
#
#     def event_notification(self, event):
#         print("New event recieved: ", event)
#         hclient.alert = True
#
# class HMI_Client():
#
#
#     def __init__(self, endpoint):
#         self.client = Client(endpoint)
#
#
#     def __enter__(self):
#
#         while(True):
#             try:
#                 self.client.connect()
#                 print("HMI client connected")
#                 break
#             except:
#                 print("Failed to connect HMI client")
#                 time.sleep(0.5)
#         self.alert = False
#         root = self.client.get_root_node()
#
#
#         obj = root.get_child(["0:Objects", "2:AllStop"])
#
#         msclt = SubHandler()
#         sub = self.client.create_subscription(100, msclt)
#
#
#         handle = sub.subscribe_events(obj)
#
#
#         return self
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         print("Disconnecting....")
#         self.client.disconnect(


if __name__ == '__main__':

    server_name = "Warehouse OPCUA Server"
    endpoint_address = "opc.tcp://192.168.200.168:51993"
    t_endpoint = "opc.tcp://192.168.200.160:40840"
    c = ModbusClient(host="192.168.200.237", port=502, auto_open=True)
    homing()
    wserver = OPCUA_Server(endpoint_address,server_name)
    tclinet= Transport_Client()

    with wserver :

        try:
            wserver.status.set_value(True)

            #product_count()
            while True:
                time.sleep(2)
                #continuously check for the delivery time if exists
                check_time()
                #calling function for updating stock
                time.sleep(2)
                get_stock()
                time.sleep(2)
                #storing wp after calling method from transport client
                if RED_STORE:
                    RED_STORE = False

                    store_red()
                elif BLACK_STORE:
                    BLACK_STORE = False

                    store_black()
                elif SILVER_STORE:
                    SILVER_STORE = False

                    store_silver()
                else:
                    pass



        except KeyboardInterrupt:
            print("Goodbye")
