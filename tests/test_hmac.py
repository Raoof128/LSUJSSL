import pytest
from satellite_sim.crypto.hmac_signer import HMACSigner
from satellite_sim.crypto.verifier import HMACVerifier

def test_hmac_signing_and_verification():
    secret = b'TEST_KEY'
    signer = HMACSigner(secret)
    verifier = HMACVerifier(secret)
    
    data = b'Hello Satellite'
    signature = signer.sign(data)
    
    assert len(signature) == 32 # SHA256 is 32 bytes
    assert verifier.verify(data, signature) == True

def test_hmac_tampering():
    secret = b'TEST_KEY'
    signer = HMACSigner(secret)
    verifier = HMACVerifier(secret)
    
    data = b'Hello Satellite'
    signature = signer.sign(data)
    
    # Tamper with data
    tampered_data = b'Hello Hacker'
    assert verifier.verify(tampered_data, signature) == False
    
    # Tamper with signature
    tampered_sig = signature[:-1] + b'\x00'
    assert verifier.verify(data, tampered_sig) == False
