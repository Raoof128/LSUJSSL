import pytest
import struct
from satellite_sim.ground_station.packet_builder import CCSDSPacketBuilder


def test_packet_structure():
    builder = CCSDSPacketBuilder(apid=0x123)
    payload = "TEST_CMD"
    packet = builder.build_packet(payload)

    # Check Primary Header (6 bytes)
    primary_header = packet[:6]
    # Version (3 bits) = 0
    # Type (1 bit) = 1
    # Sec Header (1 bit) = 1
    # APID (11 bits) = 0x123

    # 0001 1001 0010 0011 -> 0x1923
    byte1_2 = struct.unpack(">H", primary_header[:2])[0]
    assert (byte1_2 & 0x07FF) == 0x123

    # Check Payload
    # Header (6) + Timestamp (8) = 14 bytes offset
    assert packet[14:] == b"TEST_CMD"
