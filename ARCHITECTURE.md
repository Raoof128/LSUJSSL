# LEO Satellite Security Architecture

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        SATELLITE SIMULATION LAB                     │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────────┐                    ┌──────────────────────┐
│  Legitimate Ground   │                    │   Rogue Ground       │
│  Station (ALPHA)     │                    │   Station (X)        │
│  ┌────────────────┐  │                    │  ┌────────────────┐  │
│  │ CCSDS Builder  │  │                    │  │ CCSDS Spoofer  │  │
│  │ HMAC Signer    │  │                    │  │ (No Valid Key) │  │
│  └────────────────┘  │                    │  └────────────────┘  │
└──────────┬───────────┘                    └───────────┬──────────┘
           │                                            │
           │   TX: Signed Command Packets               │   TX: Malicious Packets
           │                                            │
           └──────────────────┐      ┌─────────────────┘
                              │      │
                              ▼      ▼
                    ┌──────────────────────┐
                    │  RF UPLINK CHANNEL   │
                    │  (Simulated Medium)  │
                    └──────────┬───────────┘
                               │
                               │ RX: All Incoming Traffic
                               ▼
               ┌────────────────────────────────────┐
               │        SATELLITE RECEIVER          │
               │  ┌──────────────────────────────┐  │
               │  │   SPACE FIREWALL             │  │
               │  │                              │  │
               │  │   1. Parse CCSDS Header      │  │
               │  │   2. Extract Timestamp       │  │
               │  │   3. Verify HMAC-SHA256      │  │
               │  │   4. Check Freshness         │  │
               │  │                              │  │
               │  │   ┌──────────┬──────────┐    │  │
               │  │   │  VALID   │ INVALID  │    │  │
               │  │   └────┬─────┴────┬─────┘    │  │
               │  └────────┼──────────┼──────────┘  │
               │           │          │             │
               │           ▼          ▼             │
               │    ┌──────────┐  ┌─────────────┐  │
               │    │ Execute  │  │   Reject &  │  │
               │    │ Command  │  │   Log Event │  │
               │    └──────────┘  └─────────────┘  │
               │                        │           │
               │                        ▼           │
               │              ┌──────────────────┐  │
               │              │ Telemetry System │  │
               │              │ - telemetry.log  │  │
               │              │ - events.json    │  │
               │              └──────────────────┘  │
               └────────────────────────────────────┘
```

## Security Controls

### 1. **Authentication Layer (HMAC-SHA256)**
- **Purpose**: Ensure commands originate from an authorized Ground Station
- **Implementation**: Every command packet is signed with a shared secret key
- **Strength**: SHA-256 provides 256-bit security level

### 2. **Integrity Protection**
- **Purpose**: Detect any tampering with command payloads
- **Implementation**: HMAC covers the entire CCSDS packet (headers + payload)
- **Detection**: Modified packets fail signature validation

### 3. **Replay Attack Prevention**
- **Purpose**: Prevent attackers from re-sending old commands
- **Implementation**: Timestamp validation (60-second freshness window)
- **Result**: Stale packets are automatically rejected

### 4. **CCSDS Protocol Compliance**
- **Primary Header**: 6 bytes (Version, Type, APID, Sequence)
- **Secondary Header**: 8 bytes (Timestamp for freshness validation)
- **Payload**: Variable length command string

## Threat Model

### Modeled Threats
1. **Command Spoofing**: Attacker sends fake commands
2. **Replay Attacks**: Re-transmission of valid commands
3. **Man-in-the-Middle**: Packet modification in transit
4. **Jamming/Flooding**: Channel saturation (simulated packet loss)

### Out of Scope
- Physical layer RF jamming
- Quantum computing attacks
- Side-channel attacks
- Social engineering

## Defense Effectiveness

| Attack Type | Detection Rate | Mitigation |
|------------|----------------|------------|
| Invalid Signature | 100% | Rejected, logged |
| Missing Signature | 100% | Rejected, logged |
| Replay (Stale) | 100% | Rejected, logged |
| Malformed CCSDS | 100% | Rejected, logged |

---

**Document Version**: 1.0  
**Last Updated**: 2024-11-20
