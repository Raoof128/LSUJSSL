import pytest
from satellite_sim.satellite.firewall import SpaceFirewall
from satellite_sim.satellite.telemetry import TelemetrySystem
from satellite_sim.ground_station.legit import LegitGroundStation
from satellite_sim.ground_station.rogue import RogueGroundStation

# Shared test secret
TEST_SECRET = b'TEST_SECRET_KEY_123'

@pytest.fixture
def telemetry():
    """Create a fresh telemetry system for each test."""
    return TelemetrySystem(log_file="test_telemetry.log", events_file="test_events.json")

@pytest.fixture
def firewall(telemetry):
    """Create a firewall instance with test telemetry."""
    return SpaceFirewall(TEST_SECRET, telemetry)

@pytest.fixture
def legit_station():
    """Create a legitimate ground station."""
    return LegitGroundStation(apid=0x100, secret_key=TEST_SECRET)

@pytest.fixture
def rogue_station():
    """Create a rogue ground station."""
    return RogueGroundStation(apid=0x100)

def test_firewall_accepts_valid_command(firewall, legit_station):
    """Test that the firewall accepts properly signed commands."""
    packet = legit_station.create_command("TEST_COMMAND")
    firewall.process_packet(packet)
    
    assert firewall.accepted_commands == 1
    assert firewall.rejected_commands == 0

def test_firewall_rejects_bad_signature(firewall, rogue_station):
    """Test that the firewall rejects commands with invalid signatures."""
    packet = rogue_station.create_attack_packet("MALICIOUS_CMD", "BAD_SIGNATURE")
    firewall.process_packet(packet)
    
    assert firewall.accepted_commands == 0
    assert firewall.rejected_commands == 1

def test_firewall_rejects_no_signature(firewall, rogue_station):
    """Test that the firewall rejects commands without signatures."""
    packet = rogue_station.create_attack_packet("MALICIOUS_CMD", "NO_SIGNATURE")
    firewall.process_packet(packet)
    
    assert firewall.accepted_commands == 0
    assert firewall.rejected_commands == 1

def test_firewall_rejects_short_packet(firewall):
    """Test that the firewall rejects packets that are too short."""
    short_packet = b'SHORT'
    firewall.process_packet(short_packet)
    
    assert firewall.accepted_commands == 0
    assert firewall.rejected_commands == 1

def test_multiple_commands(firewall, legit_station):
    """Test processing multiple legitimate commands."""
    for i in range(5):
        packet = legit_station.create_command(f"COMMAND_{i}")
        firewall.process_packet(packet)
    
    assert firewall.accepted_commands == 5
    assert firewall.rejected_commands == 0

def test_mixed_commands(firewall, legit_station, rogue_station):
    """Test processing a mix of legitimate and malicious commands."""
    # Send 2 legitimate
    for i in range(2):
        packet = legit_station.create_command(f"LEGIT_{i}")
        firewall.process_packet(packet)
    
    # Send 3 attacks
    for i in range(3):
        packet = rogue_station.create_attack_packet(f"ATTACK_{i}", "BAD_SIGNATURE")
        firewall.process_packet(packet)
    
    assert firewall.accepted_commands == 2
    assert firewall.rejected_commands == 3
