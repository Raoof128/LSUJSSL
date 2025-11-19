import json
import logging
import time
from dataclasses import dataclass, asdict
from typing import Dict, Any

logger = logging.getLogger(__name__)

@dataclass
class SecurityEvent:
    timestamp: float
    event_type: str
    details: Dict[str, Any]
    severity: str

class TelemetrySystem:
    """
    Handles logging of security events and telemetry downlink.
    """
    def __init__(self, log_file: str = "telemetry.log", events_file: str = "security_events.json"):
        self.log_file = log_file
        self.events_file = events_file
        self.events = []
        
        # clear previous logs
        with open(self.log_file, 'w') as f:
            f.write("--- SATELLITE TELEMETRY STREAM START ---\n")

    def log_event(self, event_type: str, details: Dict[str, Any], severity: str = "INFO"):
        """
        Logs a security event to the telemetry stream.
        """
        event = SecurityEvent(
            timestamp=time.time(),
            event_type=event_type,
            details=details,
            severity=severity
        )
        
        self.events.append(asdict(event))
        
        # Write to text log
        log_entry = f"[{time.ctime(event.timestamp)}] [{severity}] {event_type}: {details}\n"
        with open(self.log_file, 'a') as f:
            f.write(log_entry)
            
        # Write to JSON dump (simulating a structured downlink)
        with open(self.events_file, 'w') as f:
            json.dump(self.events, f, indent=2)
            
        logger.info(f"Telemetry Sent: {event_type} - {severity}")

    def get_all_events(self):
        return self.events
