import logging
import random

logger = logging.getLogger(__name__)


class UplinkChannel:
    """
    Simulates the RF Uplink Channel.
    Can introduce noise or packet loss if desired.
    """

    def __init__(self, noise_level: float = 0.0):
        self.noise_level = noise_level

    def transmit(self, packet: bytes) -> bytes:
        """
        Transmits the packet to the satellite.

        Args:
            packet (bytes): The packet to transmit.

        Returns:
            bytes: The received packet (potentially corrupted or None if lost).
        """
        if random.random() < self.noise_level:
            logger.warning("Packet lost in transmission due to noise.")
            return None

        # In a real sim, we might bit-flip here.
        # For now, perfect transmission.
        return packet
