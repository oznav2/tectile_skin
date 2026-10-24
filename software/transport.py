"""SocketCAN FD transport owned exclusively by the skin observer process."""
import json
from pathlib import Path
import secrets
import select
import socket
import struct
import subprocess
import time

from .can_wire import WIRE, CAN_EFF_FLAG, CAN_RTR_FLAG, CAN_ERR_FLAG, SO_RXQ_OVFL


def check_interface(interface, expected_device=None):
    if expected_device is not None:
        actual = str((Path('/sys/class/net') / interface / 'device').resolve(strict=True))
        if actual != expected_device:
            raise ValueError(f'{interface}: physical adapter path changed; recommission interface mapping')
    result = subprocess.run(['ip', '-details', '-json', 'link', 'show', 'dev', interface],
                            text=True, capture_output=True, check=True, timeout=5)
    rows = json.loads(result.stdout)
    if len(rows) != 1:
        raise ValueError('cannot identify dedicated skin interface')
    row = rows[0]
    info = row.get('linkinfo', {})
    data = info.get('info_data', {})
    if (info.get('info_kind') != 'can' or row.get('mtu') != 72
            or 'UP' not in row.get('flags', [])
            or data.get('bittiming', {}).get('bitrate') != 1000000
            or data.get('data_bittiming', {}).get('bitrate') != 2000000
            or data.get('state') != 'ERROR-ACTIVE'):
        raise ValueError(f'{interface}: requires active CAN FD, MTU72, 1M arbitration / 2M data')
    return row


class Transport:
    def __init__(self, observer):
        self.observer = observer
        self.sockets = {}
        self.dropped = {}
        self.next_sync = {key: 0.0 for key in observer.gates}
        try:
            for interface in sorted({key[0] for key in observer.gates}):
                check_interface(interface, observer.interface_devices[interface])
                sock = socket.socket(socket.PF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
                self.sockets[interface] = sock
                sock.setsockopt(socket.SOL_CAN_RAW, 5, 1)
                sock.setsockopt(socket.SOL_CAN_RAW, 2, struct.pack('=I', 0x1fffffff))
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
                sock.setsockopt(socket.SOL_SOCKET, SO_RXQ_OVFL, 1)
                sock.setblocking(False)
                sock.bind((interface,))
                self.dropped[interface] = 0
        except Exception:
            self.close()
            raise

    def close(self):
        for interface, sock in self.sockets.items():
            self.observer.fail_region(interface, 'transport_closed')
            sock.close()
        self.sockets.clear()

    def poll(self, now=None):
        now = time.monotonic() if now is None else now
        for key, gate in self.observer.gates.items():
            timed_out = gate.pending is not None and now - gate.pending[1] >= .020
            if gate.boot is not None and (gate.sync is None or now >= self.next_sync[key] or timed_out):
                # One outstanding nonce; preserve bounded request/response timing.
                if gate.pending is not None and now - gate.pending[1] < .020:
                    continue
                payload = gate.request_sync(secrets.randbits(64), now)
                try:
                    self.sockets[key[0]].send(WIRE.pack(
                        0x100 + key[1], len(payload), 1, 0, 0, payload.ljust(64, b'\0')))
                except (BlockingIOError, OSError) as exc:
                    self.observer.fail_region(key[0], 'transmit_failure:' + str(exc))
                self.next_sync[key] = now + 2.0
        if not self.sockets:
            return
        readable, _, _ = select.select(list(self.sockets.values()), [], [], 0)
        by_socket = {v: k for k, v in self.sockets.items()}
        for sock in readable:
            interface = by_socket[sock]
            for _ in range(128):
                try:
                    raw, ancillary, flags, _ = sock.recvmsg(WIRE.size, 128)
                except BlockingIOError:
                    break
                except OSError as exc:
                    self.observer.fail_region(interface, 'receive_failure:' + str(exc))
                    break
                self.receive(interface, raw, ancillary, flags, time.monotonic())

    def receive(self, interface, raw, ancillary, flags, now):
        for level, kind, value in ancillary:
            if level == socket.SOL_SOCKET and kind == SO_RXQ_OVFL:
                if len(value) < 4:
                    self.observer.fail_region(interface, 'truncated_overflow_counter')
                    return
                count, = struct.unpack('=I', value[:4])
                if count != self.dropped[interface]:
                    self.dropped[interface] = count
                    self.observer.fail_region(interface, 'socket_overflow')
                    return
        if flags & (socket.MSG_TRUNC | socket.MSG_CTRUNC) or len(raw) < 4:
            self.observer.fail_region(interface, 'truncated_socket_message')
            return
        can_id, = struct.unpack_from('=I', raw)
        if can_id & CAN_ERR_FLAG:
            self.observer.fail_region(interface, 'CAN_error_frame')
            return
        if can_id & (CAN_EFF_FLAG | CAN_RTR_FLAG):
            return
        if len(raw) != 72:
            self.observer.fail_region(interface, 'expected_CAN_FD_frame')
            return
        can_id, length, fdflags, _, _, payload = WIRE.unpack(raw)
        if not fdflags & 1 or fdflags & 2 or length > 64:
            self.observer.fail_region(interface, 'invalid_FD_flags_or_length')
            return
        self.observer.ingest(interface, can_id, payload[:length], now)
