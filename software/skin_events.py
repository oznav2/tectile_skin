"""Send-on-delta scheduling, adapted from Cheng et al. (2019), Algorithm 1.

Reference logic only: it does not sample hardware or send CAN packets. Keep
100 Hz acquisition. Send absolute v2 snapshots, at least every 20 ms; active
contact/fault states retain 100 Hz reporting. Commit a proposal only on the
MCU's successful TX-completion indication, never merely on enqueue.
"""
from dataclasses import dataclass
from .skin_protocol import Frame, MASK, delta32


@dataclass(frozen=True)
class Proposal:
    frame: Frame
    contact_mask: int
    reason: str


class Reporter:
    def __init__(self, deltas=(4,) * 28, temperature_delta=50, mode='hybrid', expected_mask=MASK):
        if len(deltas) != 28 or any(type(d) is not int or not 1 <= d <= 254 for d in deltas):
            raise ValueError('28 positive integer intensity deltas required')
        if type(temperature_delta) is not int or temperature_delta < 1:
            raise ValueError('positive temperature delta in centi-degrees required')
        if mode not in ('periodic', 'hybrid'):
            raise ValueError('unknown reporting mode')
        if type(expected_mask) is not int or not 0 < expected_mask <= MASK:
            raise ValueError('nonempty 28-bit expected channel mask required')
        self.expected_mask = expected_mask
        self.deltas = tuple(deltas)
        self.temperature_delta = temperature_delta
        self.mode = mode
        self.last = None
        self.pending = None
        self.retry = False

    @staticmethod
    def health(f):
        return (f.flags, f.open_mask, f.overload_mask, f.valid_mask, f.diagnostics,
                tuple(not -2000 <= t <= 8500 for t in f.temperatures),
                f.temperature_age_ms >= 250)

    def consider(self, frame, contact_mask, now_ms):
        """Called once per completed acquisition, with a fresh immutable frame.

        contact_mask is local calibrated contact/candidate state, not a wire
        field. Sequence advances on EVERY acquisition, including suppression.
        A still-pending prior send is an explicit scheduling error: the MCU must
        resolve/abort its <=5 ms TX deadline before the next 10 ms scan.
        """
        # Freeze nested caller-owned lists too; a frozen dataclass alone does
        # not make mutable channel containers immutable.
        frame = Frame.decode(frame.encode())
        if contact_mask & ~self.expected_mask or contact_mask < 0:
            raise ValueError('contact mask exceeds enabled channels')
        if (frame.valid_mask | frame.open_mask | frame.overload_mask) & ~self.expected_mask:
            raise ValueError('measurement state includes disabled channels')
        if not 0 <= delta32(now_ms & 0xffffffff, frame.capture_ms) <= 10:
            raise ValueError('proposal is not a fresh acquisition')
        if self.pending is not None:
            raise RuntimeError('previous TX has not completed or timed out')
        reason = None
        previous = self.last
        if previous is not None and (frame.boot, frame.config_crc) == (
                previous.frame.boot, previous.frame.config_crc):
            if delta32(frame.capture_ms, previous.frame.capture_ms) <= 0:
                raise ValueError('nonadvancing acquisition')
        if self.mode == 'periodic':
            reason = 'periodic'
        elif previous is None or (frame.boot, frame.config_crc) != (
                previous.frame.boot, previous.frame.config_crc):
            reason = 'initial_or_new_epoch'
        elif self.retry:
            reason = 'retry_latest_snapshot'
        elif self.health(frame) != self.health(previous.frame):
            reason = 'health_transition'
        elif (frame.flags != 15 or frame.valid_mask != self.expected_mask or frame.open_mask
              or frame.overload_mask or frame.diagnostics
              or any(not -2000 <= t <= 8500 for t in frame.temperatures)
              or frame.temperature_age_ms >= 250):
            reason = 'ongoing_fault'
        elif contact_mask != previous.contact_mask:
            reason = 'contact_transition'
        elif contact_mask:
            reason = 'active_contact'
        elif any(frame.valid_mask & (1 << i) and abs(x - y) >= self.deltas[i]
                 for i, (x, y) in enumerate(zip(frame.intensity, previous.frame.intensity))):
            reason = 'touch_delta'
        elif any(abs(x - y) >= self.temperature_delta
                 for x, y in zip(frame.temperatures, previous.frame.temperatures)):
            reason = 'temperature_delta'
        elif delta32(frame.capture_ms, previous.frame.capture_ms) >= 20:
            reason = 'absolute_refresh'
        if reason is None:
            return None
        self.pending = Proposal(frame, contact_mask, reason)
        return self.pending

    def complete(self, proposal, success):
        if self.pending is None or proposal is not self.pending:
            raise ValueError('completion does not match in-flight proposal')
        if success:
            self.last = proposal
        self.retry = not success
        self.pending = None
