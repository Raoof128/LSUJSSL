import hmac
import hashlib
import logging

logger = logging.getLogger(__name__)


class HMACVerifier:
    """
    Handles validation of HMAC-SHA256 signatures.
    """

    def __init__(self, secret_key: bytes):
        """
        Initialize the verifier with a secret key.

        Args:
            secret_key (bytes): The shared secret key for verification.
        """
        self.secret_key = secret_key

    def verify(self, data: bytes, received_signature: bytes) -> bool:
        """
        Verify the HMAC-SHA256 signature for the given data.

        Args:
            data (bytes): The data that was signed.
            received_signature (bytes): The signature to verify.

        Returns:
            bool: True if the signature is valid, False otherwise.
        """
        expected_signature = hmac.new(self.secret_key, data, hashlib.sha256).digest()
        is_valid = hmac.compare_digest(expected_signature, received_signature)

        if is_valid:
            logger.debug("Signature verification successful.")
        else:
            logger.warning(
                f"Signature verification failed! Expected {expected_signature.hex()[:8]}..., got {received_signature.hex()[:8]}..."
            )

        return is_valid
