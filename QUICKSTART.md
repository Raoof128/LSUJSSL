# ⚡ Quickstart Guide

Get up and running with the LEO Satellite Simulation Lab in **5 minutes**.

---

## 🚀 Installation (1 minute)

```bash
# Clone the repository
git clone https://github.com/your-username/leo-satellite-sim.git
cd leo-satellite-sim

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🎮 Run Your First Simulation (2 minutes)

### Option 1: Full Demo
```bash
python demo.py
```

This runs a complete scenario with legitimate commands and attack attempts.

### Option 2: Manual CLI Commands

**Send a legitimate command:**
```bash
python -m satellite_sim.cli.sat_cli send \
  --station legit \
  --cmd "ADJUST_THRUST"
```

**Launch a spoofing attack:**
```bash
python -m satellite_sim.cli.sat_cli send \
  --station rogue \
  --cmd "SHUTDOWN_REACTOR" \
  --attack-type BAD_SIGNATURE
```

**View telemetry logs:**
```bash
python -m satellite_sim.cli.sat_cli watch-telemetry
```

**Export security report:**
```bash
python -m satellite_sim.cli.sat_cli export-report
```

---

## 🧪 Run Tests (1 minute)

```bash
# Using Makefile
make test

# Or manually
pytest tests/ -v
```

---

## 📊 What You'll See

### Legitimate Command (✅ Accepted)
```
Initiating Uplink Transmission...
Legit Station sending: 'ADJUST_THRUST'
Packet received by satellite... processing...
Transmission Complete.
✅ Accepted: 1 | ❌ Rejected: 0
```

### Rogue Attack (❌ Blocked)
```
Initiating Uplink Transmission...
Rogue Station attacking with: 'SHUTDOWN_REACTOR' (Type: BAD_SIGNATURE)
Packet received by satellite... processing...
Signature verification failed! Expected f837a9c6..., got cf322996...
Transmission Complete.
✅ Accepted: 0 | ❌ Rejected: 1
```

---

## 🎯 Next Steps

1. **Read the docs**: Check out [README.md](README.md) for full documentation
2. **Explore the code**: Start with [`satellite_sim/satellite/firewall.py`](satellite_sim/satellite/firewall.py)
3. **Customize**: Modify commands, attack types, or add new scenarios
4. **Extend**: Add new features (see [CONTRIBUTING.md](CONTRIBUTING.md))

---

## 💡 Pro Tips

- Use `make help` to see all available commands
- Check `telemetry.log` and `security_events.json` for detailed logs
- Run `make clean` to remove generated log files
- Install dev dependencies with `pip install -r requirements-dev.txt`

---

**That's it! You're now running a Defence-grade satellite security simulator.** 🛰️🔒
