import pytest
import time
from satellite_sim.satellite.telemetry import TelemetrySystem, SecurityEvent

def test_telemetry_initialization():
    """Test that telemetry system initializes correctly."""
    telemetry = TelemetrySystem(log_file="test_telem.log", events_file="test_events.json")
    assert len(telemetry.get_all_events()) == 0

def test_telemetry_logs_event():
    """Test that events are logged correctly."""
    telemetry = TelemetrySystem(log_file="test_telem.log", events_file="test_events.json")
    
    telemetry.log_event("TEST_EVENT", {"key": "value"}, "INFO")
    
    events = telemetry.get_all_events()
    assert len(events) == 1
    assert events[0]['event_type'] == "TEST_EVENT"
    assert events[0]['severity'] == "INFO"
    assert events[0]['details']['key'] == "value"

def test_telemetry_multiple_events():
    """Test logging multiple events."""
    telemetry = TelemetrySystem(log_file="test_telem.log", events_file="test_events.json")
    
    telemetry.log_event("EVENT_1", {"data": 1}, "INFO")
    telemetry.log_event("EVENT_2", {"data": 2}, "CRITICAL")
    telemetry.log_event("EVENT_3", {"data": 3}, "MEDIUM")
    
    events = telemetry.get_all_events()
    assert len(events) == 3
    assert events[0]['event_type'] == "EVENT_1"
    assert events[1]['event_type'] == "EVENT_2"
    assert events[2]['event_type'] == "EVENT_3"

def test_telemetry_timestamp():
    """Test that events have valid timestamps."""
    telemetry = TelemetrySystem(log_file="test_telem.log", events_file="test_events.json")
    
    before = time.time()
    telemetry.log_event("TIMESTAMP_TEST", {}, "INFO")
    after = time.time()
    
    events = telemetry.get_all_events()
    timestamp = events[0]['timestamp']
    
    assert before <= timestamp <= after
