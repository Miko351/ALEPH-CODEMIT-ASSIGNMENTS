"""Synthetic, offline packets; never a capture of the board or an HTTP input."""
import json
from pathlib import Path
from tempfile import gettempdir
from scapy.all import Ether, IP, UDP, Raw, wrpcap, rdpcap


def create_packets():
    packets = []
    for index, offset in enumerate((0, 0.5, 1, 2, 4.5, 5)):
        packet = Ether(src='02:00:00:00:00:01', dst='02:00:00:00:00:02') / IP(src='192.0.2.1', dst='198.51.100.20') / UDP(sport=12345, dport=9999) / Raw(b'x' * ((index + 1) * 10))
        packet.time = 1700000000 + offset
        packets.append(packet)
    return packets


def summarize(packets, seconds):
    if seconds <= 0:
        raise ValueError('seconds must be positive')
    if not packets:
        return {'seconds': seconds, 'packet_count': 0, 'byte_sum': 0}
    first = min(float(packet.time) for packet in packets)
    selected = [packet for packet in packets if 0 <= float(packet.time) - first < seconds]
    return {'seconds': seconds, 'packet_count': len(selected), 'byte_sum': sum(len(bytes(packet)) for packet in selected)}


def main():
    # The source learning/ folder is read-only in Compose; keep generated packets temporary.
    target = Path(gettempdir()) / 'mini-watch-educational' / 'educational.pcap'
    target.parent.mkdir(exist_ok=True)
    wrpcap(str(target), create_packets())
    packets = rdpcap(str(target))
    print(json.dumps({'source': 'synthetic_educational_pcap', 'is_board_capture': False, 'windows': [summarize(packets, 5), summarize(packets, 1)]}, indent=2))


if __name__ == '__main__':
    main()
