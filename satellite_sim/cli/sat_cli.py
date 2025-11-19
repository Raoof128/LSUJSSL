import typer
import logging
import os
from rich.console import Console
from rich.table import Table
from satellite_sim.ground_station.legit import LegitGroundStation
from satellite_sim.ground_station.rogue import RogueGroundStation
from satellite_sim.satellite.firewall import SpaceFirewall
from satellite_sim.satellite.telemetry import TelemetrySystem
from satellite_sim.channel.uplink import UplinkChannel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = typer.Typer()
console = Console()

# Shared Secret for the simulation
SHARED_SECRET = b'TOP_SECRET_SATELLITE_KEY_2024'

# Initialize components (Global state for simple CLI simulation)
telemetry = TelemetrySystem()
firewall = SpaceFirewall(SHARED_SECRET, telemetry)
uplink = UplinkChannel()

@app.command()
def send(
    station: str = typer.Option(..., help="Station type: 'legit' or 'rogue'"),
    cmd: str = typer.Option(..., help="Command string to send"),
    attack_type: str = typer.Option("BAD_SIGNATURE", help="Attack type for rogue station (BAD_SIGNATURE, NO_SIGNATURE)")
):
    """
    Send a command to the satellite from a Ground Station.
    """
    console.print(f"[bold blue]Initiating Uplink Transmission...[/bold blue]")
    
    packet = None
    
    if station.lower() == "legit":
        gs = LegitGroundStation(apid=0x100, secret_key=SHARED_SECRET)
        packet = gs.create_command(cmd)
        console.print(f"[green]Legit Station[/green] sending: '{cmd}'")
        
    elif station.lower() == "rogue":
        rogue = RogueGroundStation(apid=0x100)
        packet = rogue.create_attack_packet(cmd, attack_type=attack_type)
        console.print(f"[red]Rogue Station[/red] attacking with: '{cmd}' (Type: {attack_type})")
        
    else:
        console.print("[bold red]Unknown station type![/bold red]")
        return

    # Transmit
    received_packet = uplink.transmit(packet)
    
    if received_packet:
        console.print("[italic]Packet received by satellite... processing...[/italic]")
        firewall.process_packet(received_packet)
        console.print("[bold]Transmission Complete.[/bold]")
        console.print(f"\n✅ Accepted: {firewall.accepted_commands} | ❌ Rejected: {firewall.rejected_commands}")
    else:
        console.print("[bold red]Transmission Failed (Signal Lost).[/bold red]")

@app.command()
def watch_telemetry():
    """
    View the latest telemetry logs.
    """
    console.print("[bold cyan]--- SATELLITE TELEMETRY LOG ---[/bold cyan]")
    
    if os.path.exists("telemetry.log"):
        with open("telemetry.log", "r") as f:
            console.print(f.read())
    else:
        console.print("No telemetry log found.")

@app.command()
def export_report():
    """
    Export a security report summary.
    """
    events = telemetry.get_all_events()
    
    table = Table(title="Security Events Report")
    table.add_column("Timestamp", justify="right", style="cyan", no_wrap=True)
    table.add_column("Severity", style="magenta")
    table.add_column("Event Type", style="green")
    table.add_column("Details", style="white")

    for event in events:
        table.add_row(
            str(event['timestamp']), 
            event['severity'], 
            event['event_type'], 
            str(event['details'])
        )

    console.print(table)
    console.print(f"[bold green]Report exported with {len(events)} events.[/bold green]")

if __name__ == "__main__":
    app()
