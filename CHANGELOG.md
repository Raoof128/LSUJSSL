# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-11-20

### Added
- Initial release of LEO Satellite Simulation Lab
- CCSDS packet builder for spacecraft command formatting
- HMAC-SHA256 signature generation and verification
- Legitimate Ground Station with command signing
- Rogue Ground Station for attack simulation
- Space Firewall with multi-layer packet validation
- Telemetry logging system (text + JSON)
- CLI tool for simulation control (`send`, `watch-telemetry`, `export-report`)
- RF uplink channel simulator
- Timestamp-based replay attack prevention
- Comprehensive test suite
- Professional documentation (README, CONTRIBUTING, SECURITY)
- Architecture diagrams and example packet formats

### Security
- Implemented HMAC-SHA256 authentication for all commands
- Added timestamp freshness validation (60-second window)
- Structured security event logging for intrusion detection

---

**Legend:**
- `Added`: New features
- `Changed`: Changes to existing functionality
- `Deprecated`: Features to be removed
- `Removed`: Removed features
- `Fixed`: Bug fixes
- `Security`: Security improvements
