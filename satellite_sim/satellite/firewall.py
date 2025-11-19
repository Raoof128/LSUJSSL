import struct
import logging
import time
from satellite_sim.crypto.verifier import HMACVerifier
from satellite_sim.satellite.telemetry import TelemetrySystem

logger = logging.getLogger(__name__)


class SpaceFirewall:
    """
    The 'Space Firewall' running on the satellite.
    Validates incoming CCSDS packets and enforces security policies.
    """

    def __init__(self, secret_key: bytes, telemetry: TelemetrySystem):
        self.verifier = HMACVerifier(secret_key)
        self.telemetry = telemetry
        self.accepted_commands = 0
        self.rejected_commands = 0

    def process_packet(self, packet_data: bytes):
        """
        Ingest a raw packet, validate it, and decide whether to execute or drop.

        Args:
            packet_data (bytes): The received byte stream.
        """
        logger.info(f"Received packet of size {len(packet_data)} bytes.")

        # 1. Basic Length Check
        # Min length: 6 (Primary) + 0 (Sec) + 1 (Payload) + 32 (HMAC) = 39 bytes approx
        if len(packet_data) < 38:
            self.telemetry.log_event(
                "PACKET_REJECTED", {"reason": "Packet too short", "size": len(packet_data)}, "HIGH"
            )
            self.rejected_commands += 1
            return

        # 2. Extract Components
        # Assuming HMAC-SHA256 is always the last 32 bytes
        signature_len = 32
        data_part = packet_data[:-signature_len]
        received_signature = packet_data[-signature_len:]

        # 3. Validate Signature
        if not self.verifier.verify(data_part, received_signature):
            self.telemetry.log_event(
                "SECURITY_VIOLATION",
                {
                    "reason": "Invalid HMAC Signature",
                    "signature_received": received_signature.hex()[:8] + "...",
                },
                "CRITICAL",
            )
            self.rejected_commands += 1
            return

        # 4. Parse Header (Simplified CCSDS parsing)
        try:
            # Primary Header is first 6 bytes
            primary_header = data_part[:6]
            # Unpack to check APID, etc if needed
            # byte1_2, byte3_4, length = struct.unpack('>HHH', primary_header)

            # Secondary Header (Timestamp) - next 8 bytes
            timestamp_bytes = data_part[6:14]
            packet_timestamp = struct.unpack(">d", timestamp_bytes)[0]

            # 5. Check Freshness (Anti-Replay / Freshness)
            current_time = time.time()
            if abs(current_time - packet_timestamp) > 60.0:  # 60 second window
                self.telemetry.log_event(
                    "PACKET_REJECTED",
                    {
                        "reason": "Timestamp stale",
                        "packet_time": packet_timestamp,
                        "current_time": current_time,
                    },
                    "MEDIUM",
                )
                self.rejected_commands += 1
                return

            # 6. Extract Payload
            payload_bytes = data_part[14:]
            command_str = payload_bytes.decode("utf-8")

            # 7. Execute Command
            self._execute_command(command_str)

        except Exception as e:
            self.telemetry.log_event("PARSING_ERROR", {"error": str(e)}, "HIGH")
            self.rejected_commands += 1

    def _execute_command(self, command_str: str):
        """
        Simulate command execution.
        """
        self.accepted_commands += 1
        self.telemetry.log_event("COMMAND_EXECUTED", {"command": command_str}, "INFO")
        logger.info(f"*** EXECUTING COMMAND: {command_str} ***")
