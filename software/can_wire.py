"""Linux CAN FD socket structures and flags, independent of robot hardware."""
import struct

WIRE = struct.Struct('=IBBBB64s')
CAN_EFF_FLAG = 0x80000000
CAN_RTR_FLAG = 0x40000000
CAN_ERR_FLAG = 0x20000000
SO_RXQ_OVFL = 40
