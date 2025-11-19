import hmac
import hashlib
import logging

logger = logging.getLogger(__name__)

class HMACSigner:
    """
    Handles HMAC-SHA256 signing of data.
    """
    def __init__(self, secret_key: bytes):
        """
        Initialize the signer with a secret key.
        
        Args:
            secret_key (bytes): The shared secret key for signing.
        """
        self.secret_key = secret_key

    def sign(self, data: bytes) -> bytes:
        """
        Compute the HMAC-SHA256 signature for the given data.
        
        Args:
            data (bytes): The data to sign.
            
        Returns:
            bytes: The computed HMAC signature.
        """
        signature = hmac.new(self.secret_key, data, hashlib.sha256).digest()
        logger.debug(f"Signed data of length {len(data)} with signature {signature.hex()[:8]}...")
        return signature
