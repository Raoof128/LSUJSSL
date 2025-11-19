import logging
import os
from satellite_sim.ground_station.packet_builder import CCSDSPacketBuilder

logger = logging.getLogger(__name__)


class RogueGroundStation:
    """
    Simulates a Rogue Ground Station attempting to spoof commands.
    """

    def __init__(self, apid: int):
        self.packet_builder = CCSDSPacketBuilder(apid=apid)
        self.station_id = "ROGUE_STATION_X"

    def create_attack_packet(self, command_str: str, attack_type: str = "BAD_SIGNATURE") -> bytes:
        """
        Creates a malicious packet based on the attack type.

        Args:
            command_str (str): The malicious command.
            attack_type (str): 'BAD_SIGNATURE', 'NO_SIGNATURE', 'REPLAY' (not fully impl here without state).

        Returns:
            bytes: The malicious packet.
        """
        logger.info(
            f"[{self.station_id}] constructing ATTACK packet: {command_str} [{attack_type}]"
        )

        raw_packet = self.packet_builder.build_packet(command_str)

        if attack_type == "BAD_SIGNATURE":
            # Append random bytes as signature
            fake_sig = os.urandom(32)
            return raw_packet + fake_sig

        elif attack_type == "NO_SIGNATURE":
            # Send without signature
            return raw_packet

        elif attack_type == "SHORT_SIGNATURE":
            # Send incomplete signature
            return raw_packet + os.urandom(10)

        else:
            # Default to bad signature
            return raw_packet + os.urandom(32)
