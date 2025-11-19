import pytest
from satellite_sim.channel.uplink import UplinkChannel


def test_uplink_perfect_transmission():
    """Test that uplink transmits packets without noise."""
    channel = UplinkChannel(noise_level=0.0)
    packet = b"TEST_PACKET_DATA"

    received = channel.transmit(packet)

    assert received == packet


def test_uplink_with_noise():
    """Test that uplink can lose packets with noise."""
    channel = UplinkChannel(noise_level=1.0)  # 100% packet loss
    packet = b"TEST_PACKET_DATA"

    # With 100% noise, should always return None
    received = channel.transmit(packet)
    assert received is None


def test_uplink_partial_noise():
    """Test uplink with partial noise (statistical)."""
    channel = UplinkChannel(noise_level=0.5)  # 50% packet loss
    packet = b"TEST_PACKET_DATA"

    # Run multiple times to test randomness
    results = [channel.transmit(packet) for _ in range(100)]

    # Some should succeed, some should fail
    successes = sum(1 for r in results if r is not None)
    failures = sum(1 for r in results if r is None)

    # With 50% noise, we expect roughly 50/50 split (allow some variance)
    assert 30 <= successes <= 70
    assert 30 <= failures <= 70
