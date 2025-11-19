import struct
import time
from enum import Enum
from typing import Optional

class PacketType(Enum):
    CMD = 1
    TLM = 0

class CCSDSPacketBuilder:
    """
    Constructs CCSDS packets with Primary Header, Secondary Header, and Payload.
    """
    
    def __init__(self, apid: int = 0x100):
        self.apid = apid
        self.sequence_count = 0

    def build_packet(self, cmd_payload: str, include_secondary_header: bool = True) -> bytes:
        """
        Builds a CCSDS packet.
        
        Structure:
        [Primary Header (6 bytes)]
        [Secondary Header (Timestamp - 8 bytes, optional)]
        [Payload (Command String)]
        
        Args:
            cmd_payload (str): The command string (e.g., "CMD: ADJUST_THRUST").
            include_secondary_header (bool): Whether to include a timestamp header.
            
        Returns:
            bytes: The raw packet bytes (excluding HMAC, which is added later).
        """
        # 1. Prepare Payload
        payload_bytes = cmd_payload.encode('utf-8')
        
        # 2. Prepare Secondary Header (Timestamp)
        # Using a simple 8-byte float timestamp for simulation purposes
        sec_header_bytes = b''
        if include_secondary_header:
            timestamp = time.time()
            sec_header_bytes = struct.pack('>d', timestamp)
            
        # 3. Calculate Length
        # Packet Length field = total bytes - 7 (Primary Header is 6 bytes, length field counts from byte after it?)
        # CCSDS 133.0-B-1: "The Packet Length field specifies the number of octets in the Packet Data Field minus 1."
        # Packet Data Field = Secondary Header + User Data
        packet_data_length = len(sec_header_bytes) + len(payload_bytes)
        length_field_value = packet_data_length - 1
        
        # 4. Build Primary Header
        # Version (3 bits) = 000
        # Type (1 bit) = 1 (Command)
        # Sec Header Flag (1 bit) = 1 if present
        # APID (11 bits)
        version = 0
        packet_type = 1 # Telecommand
        sh_flag = 1 if include_secondary_header else 0
        
        byte1_2 = (version << 13) | (packet_type << 12) | (sh_flag << 11) | (self.apid & 0x7FF)
        
        # Seq Flags (2 bits) = 11 (Unsegmented)
        # Seq Count (14 bits)
        seq_flags = 3 
        byte3_4 = (seq_flags << 14) | (self.sequence_count & 0x3FFF)
        
        # Increment sequence count
        self.sequence_count = (self.sequence_count + 1) % 16384
        
        primary_header = struct.pack('>HHH', byte1_2, byte3_4, length_field_value)
        
        return primary_header + sec_header_bytes + payload_bytes
