# API Documentation

## Overview

The LEO Satellite Simulation Lab provides a clean, modular API for building satellite security simulations.

---

## Core Modules

### `satellite_sim.crypto`

#### `HMACSigner`

**Purpose**: Generate HMAC-SHA256 signatures for command packets.

```python
from satellite_sim.crypto import HMACSigner

signer = HMACSigner(secret_key=b'YOUR_SECRET_KEY')
signature = signer.sign(data=b'packet_data')
```

**Methods:**
- `__init__(secret_key: bytes)` - Initialize with a shared secret key
- `sign(data: bytes) -> bytes` - Compute HMAC-SHA256 signature

---

#### `HMACVerifier`

**Purpose**: Validate HMAC-SHA256 signatures.

```python
from satellite_sim.crypto import HMACVerifier

verifier = HMACVerifier(secret_key=b'YOUR_SECRET_KEY')
is_valid = verifier.verify(data=b'packet_data', received_signature=signature)
```

**Methods:**
- `__init__(secret_key: bytes)` - Initialize with a shared secret key
- `verify(data: bytes, received_signature: bytes) -> bool` - Verify signature

---

### `satellite_sim.ground_station`

#### `CCSDSPacketBuilder`

**Purpose**: Construct CCSDS-compliant command packets.

```python
from satellite_sim.ground_station import CCSDSPacketBuilder

builder = CCSDSPacketBuilder(apid=0x100)
packet = builder.build_packet(cmd_payload="ADJUST_THRUST")
```

**Methods:**
- `__init__(apid: int)` - Initialize with Application Process ID
- `build_packet(cmd_payload: str, include_secondary_header: bool = True) -> bytes` - Build packet

---

#### `LegitGroundStation`

**Purpose**: Simulate an authorized ground station sending authenticated commands.

```python
from satellite_sim.ground_station import LegitGroundStation

station = LegitGroundStation(apid=0x100, secret_key=b'SECRET')
signed_packet = station.create_command("DEPLOY_SOLAR_PANEL")
```

**Methods:**
- `__init__(apid: int, secret_key: bytes)` - Initialize station
- `create_command(command_str: str) -> bytes` - Create signed command packet

---

#### `RogueGroundStation`

**Purpose**: Simulate an attacker attempting to spoof commands.

```python
from satellite_sim.ground_station import RogueGroundStation

rogue = RogueGroundStation(apid=0x100)
attack_packet = rogue.create_attack_packet("SHUTDOWN", attack_type="BAD_SIGNATURE")
```

**Methods:**
- `__init__(apid: int)` - Initialize rogue station
- `create_attack_packet(command_str: str, attack_type: str) -> bytes` - Create malicious packet

**Attack Types:**
- `BAD_SIGNATURE` - Random bytes as signature
- `NO_SIGNATURE` - Packet without signature
- `SHORT_SIGNATURE` - Incomplete signature

---

### `satellite_sim.satellite`

#### `SpaceFirewall`

**Purpose**: Validate incoming packets and enforce security policies.

```python
from satellite_sim.satellite import SpaceFirewall, TelemetrySystem

telemetry = TelemetrySystem()
firewall = SpaceFirewall(secret_key=b'SECRET', telemetry=telemetry)
firewall.process_packet(packet_data)
```

**Methods:**
- `__init__(secret_key: bytes, telemetry: TelemetrySystem)` - Initialize firewall
- `process_packet(packet_data: bytes) -> None` - Validate and process packet

**Attributes:**
- `accepted_commands: int` - Count of accepted commands
- `rejected_commands: int` - Count of rejected commands

---

#### `TelemetrySystem`

**Purpose**: Log security events and telemetry data.

```python
from satellite_sim.satellite import TelemetrySystem

telemetry = TelemetrySystem(log_file="telemetry.log", events_file="security_events.json")
telemetry.log_event("COMMAND_EXECUTED", {"command": "TEST"}, "INFO")
events = telemetry.get_all_events()
```

**Methods:**
- `__init__(log_file: str, events_file: str)` - Initialize telemetry system
- `log_event(event_type: str, details: dict, severity: str)` - Log security event
- `get_all_events() -> list` - Retrieve all logged events

**Severity Levels:**
- `INFO` - Normal operations
- `MEDIUM` - Warnings
- `HIGH` - Serious issues
- `CRITICAL` - Security violations

---

### `satellite_sim.channel`

#### `UplinkChannel`

**Purpose**: Simulate RF uplink transmission with optional noise.

```python
from satellite_sim.channel import UplinkChannel

channel = UplinkChannel(noise_level=0.1)  # 10% packet loss
received_packet = channel.transmit(packet)
```

**Methods:**
- `__init__(noise_level: float)` - Initialize channel (0.0 = perfect, 1.0 = 100% loss)
- `transmit(packet: bytes) -> bytes | None` - Transmit packet (returns None if lost)

---

## Example: Complete Simulation

```python
from satellite_sim import (
    LegitGroundStation,
    RogueGroundStation,
    SpaceFirewall,
    TelemetrySystem,
    UplinkChannel
)

# Setup
SECRET_KEY = b'SHARED_SECRET'
telemetry = TelemetrySystem()
firewall = SpaceFirewall(SECRET_KEY, telemetry)
channel = UplinkChannel(noise_level=0.0)

legit_station = LegitGroundStation(apid=0x100, secret_key=SECRET_KEY)
rogue_station = RogueGroundStation(apid=0x100)

# Send legitimate command
legit_packet = legit_station.create_command("ADJUST_THRUST")
received = channel.transmit(legit_packet)
if received:
    firewall.process_packet(received)

# Attempt attack
attack_packet = rogue_station.create_attack_packet("SHUTDOWN", "BAD_SIGNATURE")
received = channel.transmit(attack_packet)
if received:
    firewall.process_packet(received)

# Check results
print(f"Accepted: {firewall.accepted_commands}")  # Output: 1
print(f"Rejected: {firewall.rejected_commands}")  # Output: 1
print(f"Events: {len(telemetry.get_all_events())}")  # Output: 2
```

---

## CLI Reference

See [README.md](README.md#-usage-cli) for CLI documentation.

---

**For more information, see the source code docstrings or contact the maintainers.**
