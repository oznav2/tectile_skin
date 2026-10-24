"""Deterministic synthetic packets exercise the production identity/freshness gate."""
from .skin_protocol import ANNOUNCE, SYNC_REPLY, VERSION, Frame


def announce_and_sync(observer, now=100.0):
    for p in observer.patches:
        key = (p.interface, p.node_id)
        observer.ingest(p.interface, 0x300 + p.node_id, ANNOUNCE.pack(
            VERSION, 0xa1, p.node_id, bytes.fromhex(p.uid), 1, p.config_crc, 7, 10, 0), now)
        gate = observer.gates[key]
        gate.request_sync(123, now)
        observer.ingest(p.interface, 0x380 + p.node_id, SYNC_REPLY.pack(
            VERSION, 0x52, p.node_id, 123, 1, 1000, 1001, p.config_crc, 0), now + .002)


def feed_demo(observer, sequence=1, capture_ms=1010, now=100.012):
    for index, p in enumerate(observer.patches):
        values = [0 if p.expected_mask & (1 << i) else 255 for i in range(28)]
        values[sequence % p.expected_mask.bit_count()] = 80 + index * 10
        f = Frame(15, sequence, 1, capture_ms, p.config_crc, tuple(values), (2450, 2600),
                  0, 0, p.expected_mask, 5, 0)
        observer.ingest(p.interface, 0x200 + p.node_id, f.encode(), now)


def demo_records(observer):
    announce_and_sync(observer)
    feed_demo(observer)
    yield observer.snapshot(100.012)
    yield observer.snapshot(100.080)
