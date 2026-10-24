"""Run the dependency-free skin observer. The demo never opens hardware."""
import argparse
import json
from pathlib import Path
import time

from .observer import Observer
from .demo import demo_records
from .transport import Transport


def main():
    parser = argparse.ArgumentParser(description='Independent tactile-skin observer; no actuator commands')
    parser.add_argument('--config', default=str(Path(__file__).with_name('config') / 'limb_skin.example.json'))
    parser.add_argument('--demo', action='store_true', help='synthetic fresh and expired records; no devices opened')
    args = parser.parse_args()
    with open(args.config, encoding='utf-8') as handle:
        config = json.load(handle)
    observer = Observer(config, demo=args.demo)
    if args.demo:
        for record in demo_records(observer):
            print(json.dumps(record, allow_nan=False))
        return
    transport = Transport(observer)
    try:
        deadline = time.monotonic()
        while True:
            transport.poll()
            now = time.monotonic()
            if now >= deadline:
                print(json.dumps(observer.snapshot(now), allow_nan=False), flush=True)
                deadline = now + .010
            time.sleep(.002)
    except KeyboardInterrupt:
        pass
    finally:
        transport.close()


if __name__ == '__main__':
    main()
