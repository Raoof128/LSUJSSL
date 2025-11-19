import logging
from satellite_sim.ground_station.packet_builder import CCSDSPacketBuilder
from satellite_sim.crypto.hmac_signer import HMACSigner

logger = logging.getLogger(__name__)


class LegitGroundStation:
    """
    Simulates a legitimate Ground Station that sends authenticated commands.
    """

    def __init__(self, apid: int, secret_key: bytes):
        self.packet_builder = CCSDSPacketBuilder(apid=apid)
        self.signer = HMACSigner(secret_key)
        self.station_id = "STATION_ALPHA"

    def create_command(self, command_str: str) -> bytes:
        """
        Creates a signed CCSDS command packet.

        Args:
            command_str (str): The command to send.

        Returns:
            bytes: The full packet with HMAC signature appended.
        """
        logger.info(f"[{self.station_id}] Generating command: {command_str}")

        # Build the raw packet (Header + Payload)
        raw_packet = self.packet_builder.build_packet(command_str)

        # Sign the packet
        signature = self.signer.sign(raw_packet)

        # Append signature
        signed_packet = raw_packet + signature

        logger.info(f"[{self.station_id}] Packet signed. Total length: {len(signed_packet)} bytes.")
        return signed_packet
