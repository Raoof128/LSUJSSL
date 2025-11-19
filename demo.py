#!/usr/bin/env python3
"""
Comprehensive Demonstration Script for LEO Satellite Simulation Lab
Runs a full scenario: Legit commands + Multiple attack attempts
"""

import subprocess
import time


def run_command(cmd):
    """Execute a CLI command and display output."""
    print(f"\n{'='*80}")
    print(f"EXECUTING: {cmd}")
    print(f"{'='*80}")
    result = subprocess.run(cmd, shell=True, capture_output=False)
    time.sleep(1)
    return result.returncode


def main():
    print(
        """
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║                                                                       ║
    ║   LEO SATELLITE COMMAND LINK INTRUSION SIMULATION DEMO                ║
    ║                                                                       ║
    ║   Demonstrates: CCSDS Packet Processing, HMAC Authentication,        ║
    ║                 Spoofing Detection, and Security Logging              ║
    ║                                                                       ║
    ╚═══════════════════════════════════════════════════════════════════════╝
    """
    )

    # Scenario 1: Legitimate Operations
    print("\n🛰️  SCENARIO 1: LEGITIMATE GROUND STATION OPERATIONS")
    print("-" * 80)
    run_command("python -m satellite_sim.cli.sat_cli send --station legit --cmd 'ADJUST_THRUST'")
    run_command(
        "python -m satellite_sim.cli.sat_cli send --station legit --cmd 'UPDATE_ORBIT_PARAMETERS'"
    )
    run_command(
        "python -m satellite_sim.cli.sat_cli send --station legit --cmd 'DEPLOY_SOLAR_PANEL'"
    )

    # Scenario 2: Attack Attempts
    print("\n\n⚠️  SCENARIO 2: ROGUE STATION ATTACK ATTEMPTS")
    print("-" * 80)
    run_command(
        "python -m satellite_sim.cli.sat_cli send --station rogue --cmd 'SHUTDOWN_REACTOR' --attack-type BAD_SIGNATURE"
    )
    run_command(
        "python -m satellite_sim.cli.sat_cli send --station rogue --cmd 'DISABLE_ATTITUDE_CONTROL' --attack-type NO_SIGNATURE"
    )
    run_command(
        "python -m satellite_sim.cli.sat_cli send --station rogue --cmd 'CHANGE_ORBIT' --attack-type SHORT_SIGNATURE"
    )

    # View Results
    print("\n\n📊 TELEMETRY & SECURITY LOGS")
    print("-" * 80)
    run_command("python -m satellite_sim.cli.sat_cli watch-telemetry")

    print("\n\n📈 SECURITY REPORT")
    print("-" * 80)
    run_command("python -m satellite_sim.cli.sat_cli export-report")

    print(
        """
    \n╔═══════════════════════════════════════════════════════════════════════╗
    ║                                                                       ║
    ║   ✅ DEMONSTRATION COMPLETE                                           ║
    ║                                                                       ║
    ║   Results: Check 'telemetry.log' and 'security_events.json'          ║
    ║                                                                       ║
    ╚═══════════════════════════════════════════════════════════════════════╝
    """
    )


if __name__ == "__main__":
    main()
