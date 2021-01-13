import time
import random
import struct
import machine

from uac_anchor.main.utm.conversion import to_latlon, from_latlon
from uac_anchor.main.misc.utils import distance
from uac_modem.main.unm3driver import Nm3


# SOME GLOBAL CONSTANTs
SOUND_SPEED = 1530.0  # m/s
FLUID_DENSITY = 1029.0  # kg/m^3

# =============== Virtual Anchors ======================= #
# Anchor locations in Lat/Lon and anchor_depth (m)
anchor_depth = 1.0  # m
M1 = [56.38547, -4.22764]
A11 = [56.39012, -4.22906]
A12 = [56.38967, -4.23279]
A13 = [56.38886, -4.23593]
sg1 = [M1, A11, A12, A13]
# Convert to UTM
SG1 = []
while sg1:
    anchor = sg1.pop(0)
    x, y, zone, zone_letter = from_latlon(anchor[0], anchor[1])
    SG1.append([x, y, anchor_depth, zone, zone_letter])

M2 = [56.38583, -4.22755]
A21 = [56.3876, -4.23768]
A22 = [56.38632, -4.23893]
A23 = [56.3848, -4.23953]
sg2 = [M2, A21, A22, A23]
# Convert to UTM
SG2 = []
while sg2:
    anchor = sg2.pop(0)
    x, y, zone, zone_letter = from_latlon(anchor[0], anchor[1])
    SG2.append([x, y, anchor_depth, zone, zone_letter])

M3 = [56.38537, -4.22747]
A31 = [56.38309, -4.23871]
A32 = [56.38176, -4.23704]
A33 = [56.38071, -4.23344]
sg3 = [M3, A31, A32, A33]
# Convert to UTM
SG3 = []
while sg3:
    anchor = sg3.pop(0)
    x, y, zone, zone_letter = from_latlon(anchor[0], anchor[1])
    SG3.append([x, y, anchor_depth, zone, zone_letter])

M4 = [56.38596, -4.22716]
A41 = [56.38012, -4.22979]
A42 = [56.38, -4.22563]
A43 = [56.38119, -4.22138]
sg4 = [M4, A41, A42, A43]
# Convert to UTM
SG4 = []
while sg4:
    anchor = sg4.pop(0)
    x, y, zone, zone_letter = from_latlon(anchor[0], anchor[1])
    SG4.append([x, y, anchor_depth, zone, zone_letter])

M5 = [56.38535, -4.22733]
A51 = [56.38302, -4.21781]
A52 = [56.38535, -4.21704]
A53 = [56.38775, -4.2173]
sg5 = [M5, A51, A52, A53]
# Convert to UTM
SG5 = []
while sg5:
    anchor = sg5.pop(0)
    x, y, zone, zone_letter = from_latlon(anchor[0], anchor[1])
    SG5.append([x, y, anchor_depth, zone, zone_letter])

M6 = [56.38543, -4.22781]
A61 = [56.38955, -4.2191]
A62 = [56.39022, -4.22314]
A63 = [56.39031, -4.22588]
sg6 = [M6, A61, A62, A63]
# Convert to UTM
SG6 = []
while sg6:
    anchor = sg6.pop(0)
    x, y, zone, zone_letter = from_latlon(anchor[0], anchor[1])
    SG6.append([x, y, anchor_depth, zone, zone_letter])


M7 = [53.332648, -3.146757]
A71 = [53.380672, -3.204791]
A72 = [53.349420, -3.302614]
A73 = [53.301487, -3.206313]
sg7 = [M7, A71, A72, A73]
# Convert to UTM
SG7 = []
while sg7:
    anchor = sg7.pop(0)
    x, y, zone, zone_letter = from_latlon(anchor[0], anchor[1])
    SG7.append([x, y, anchor_depth, zone, zone_letter])
    # print("x:", x, "y:", y, "zone:", zone, "letter:", zone_letter)

# Form List of Anchors for Beacon Segments
beacon_segments = [SG1, SG2]  #, SG3, SG4, SG5, SG6]

# ==================== Virtual Sensors ============================= #
# Sensor locations in Lat/Lon and anchor_depth(m)
S1 = [56.38587, -4.23374]
S2 = [56.38264, -4.22751]
S3 = [56.38585, -4.22069]
S4 = [56.38893, -4.22799]
S5 = [56.38808, -4.23198]
S6 = [56.38335, -4.23344]
S7 = [56.38392, -4.22275]
S8 = [56.38817, -4.22395]

S9 = [53.336405, -3.211040]

sensor_loc = S1  # in Lat/Lon
sensor_depth = 100.0  # in meters
x, y, zone, zone_letter = from_latlon(sensor_loc[0], sensor_loc[1])
sensor_loc = [x, y, sensor_depth, zone, zone_letter]
# print("x:", x, "y:", y, "zone:", zone, "letter:", zone_letter)

# =============== Configure Hardware to use Nanomodem ============== #
# Switch ON internal 3V3 LDO to supply to RS232 driver
ldo_3V3 = machine.Pin('EN_3V3', mode=machine.Pin.OUT, value=1)

# Switch OFF the External LDO-2 3.3V to Sensor Payload
ldo2 = machine.Pin('Y5', mode=machine.Pin.OPEN_DRAIN, pull=None, value=0)

# Serial Port/UART is opened with a 100ms timeout for reading - non-blocking.
uart = machine.UART(1, 9600, bits=8, parity=None, stop=1, timeout=1)
nm3 = Nm3(input_stream=uart, output_stream=uart)

# ====================== Generate Beacon Signals ==================== #

# Broadcast some Global Parameters
# Sound Speed
msg_bytes = b'ULMP' + b'S' + struct.pack('f', SOUND_SPEED)
start_time = time.ticks_us()
msg_length = nm3.send_broadcast_message(msg_bytes)
end_time = time.ticks_us()
if len(msg_bytes) == msg_length:
    print("Sound Speed broadcasted in ", time.ticks_diff(end_time, start_time), " us.")

# Wait for few seconds
time.sleep(1)

# Fluid Density
msg_bytes = b'ULMP' + b'D' + struct.pack('f', FLUID_DENSITY)
start_time = time.ticks_us()
msg_length = nm3.send_broadcast_message(msg_bytes)
end_time = time.ticks_us()
if len(msg_bytes) == msg_length:
    print("Fluid density broadcasted in ", time.ticks_diff(end_time, start_time), " us.")

# Wait for few seconds
time.sleep(1)

# Broadcast "Start of Beacon Cycle"
msg_bytes = b'ULMS'
start_time = time.ticks_us()
msg_length = nm3.send_broadcast_message(msg_bytes)
end_time = time.ticks_us()
if len(msg_bytes) == msg_length:
    print("Msg Bytes:", msg_bytes)

# Wait for few seconds
time.sleep(1)

# Loop for Beacon Segments
for i, segment in enumerate(beacon_segments):
    # Loop within the beacon segment
    beacon_signals = []
    travel_time_to_anchors = []  # Lead anchor to the Asst. anchors
    travel_time_to_sensor = []   # Anchors to the sensor
    wait_times = []  # Delay at Asst. anchors before broadcasting beacon signal

    # Prepare Beacon Signals for the Anchors
    for j in range(len(segment)):
        m = len(segment)
        n = i
        lat, lon = to_latlon(segment[j][0], segment[j][1], segment[j][3], segment[j][4])
        lat = struct.pack('f', lat)
        lon = struct.pack('f', lon)
        anchor_depth = struct.pack('f', segment[j][2])
        if j == 0:
            # Start of Beacon Segment
            travel_time_to_sensor.append(distance(segment[0][0:3], sensor_loc[0:3]) / SOUND_SPEED)
            msg_bytes = b'ULMB' + struct.pack('B', n) + struct.pack('B', m) + b'L' + lat + lon + anchor_depth
        else:
            travel_time_to_anchors.append(distance(segment[0][0:3], segment[j][0:3]) / SOUND_SPEED)
            travel_time_to_sensor.append(distance(segment[j][0:3], sensor_loc[0:3]) / SOUND_SPEED)
            wait_times.append(random.random() + 5.0 + travel_time_to_anchors[j-1])
            # Continue of Beacon Segment
            msg_bytes = b'ULAB' + struct.pack('B', n) + b'L' + lat + lon + anchor_depth
        # collect beacon signal
        beacon_signals.append(msg_bytes)

    print("Travel time to the Anchors:", travel_time_to_anchors)
    print("Travel time to the Sensor:", travel_time_to_sensor)
    print("Wait Times:", wait_times)

    # Broadcast the beacon signals
    time.read_ticks()  # Get Timestamp from SysTick
    t0 = time.ticks_seconds() + (time.ticks_millis()/1E3) + (time.ticks_micros()/1E6)
    for j in range(len(segment)):
        if j == 0:
            # start_time = time.ticks_us()
            time.sleep_us(int(travel_time_to_sensor[j]*1E6))
            msg_length = nm3.send_broadcast_message(beacon_signals[j])
            # end_time = time.ticks_us()
            print("Lead Broadcast at: \t \t \t", t0)
            print("Msg bytes: ", beacon_signals[j])
            # print("Lead beacon signal took ", time.ticks_diff(end_time, start_time), " us.")
        else:
            toa = t0 + travel_time_to_anchors[j-1]
            time.sleep_us(int(wait_times[j-1]*1E6))
            time.read_ticks()  # Get Timestamp from SysTick
            t = time.ticks_seconds() + time.ticks_millis() / 1E3 + time.ticks_micros() / 1E6
            deltaT = t - toa
            msg_bytes = beacon_signals[j] + b'D' + struct.pack('f', deltaT)
            # start_time = time.ticks_us()
            time.sleep_us(int(travel_time_to_sensor[j]*1E6))
            msg_length = nm3.send_broadcast_message(msg_bytes)
            # end_time = time.ticks_us()
            print(j, "th anchor received Lead's Beacon at: \t", toa)
            print(j, "th anchor broadcasted at \t \t", t, "with deltaT =", deltaT)
            print("Msg bytes: ", msg_bytes)
            # print("Asst. beacon signal took ", time.ticks_diff(end_time, start_time), " us")

# Wait for few seconds
time.sleep(1)
msg_bytes = b'ULME'
time.read_ticks()  # Get Timestamp from SysTick
t = time.ticks_seconds() + (time.ticks_millis()/1E3) + (time.ticks_micros()/1E6)
# start_time = time.ticks_us()
msg_length = nm3.send_broadcast_message(msg_bytes)
# end_time = time.ticks_us()
print("Lead anchor broadcasted at \t \t", t)
print("Msg bytes: ", msg_bytes)
# print("Asst. beacon signal took ", time.ticks_diff(end_time, start_time), " us")
# ================ Beacon Cycle Completed =================== #

# Disable power supply to RS232 driver
# machine.Pin.board.EN_3V3.off()
ldo_3V3.off()
