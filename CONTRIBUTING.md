# Contributing to LEO Satellite Simulation Lab

Thank you for considering contributing to this project! This simulation lab models critical satellite security scenarios and your contributions help make it more realistic and educational.

## 🚀 How to Contribute

### 1. Fork & Clone
```bash
git clone https://github.com/your-username/leo-satellite-sim.git
cd leo-satellite-sim
```

### 2. Set Up Development Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 4. Make Your Changes
- Follow PEP 8 style guidelines
- Add type hints to all functions
- Include docstrings for classes and methods
- Write tests for new functionality

### 5. Run Tests
```bash
python -m pytest tests/
```

### 6. Submit a Pull Request
- Ensure all tests pass
- Provide a clear description of your changes
- Reference any related issues

## 💡 Ideas for Contributions

- **New Attack Vectors**: Implement replay attacks, timing attacks, or packet flooding
- **GNU Radio Integration**: Add RF simulation using GNU Radio flowgraphs
- **Visualization**: Create real-time signal plots or network diagrams
- **Performance**: Optimize packet processing for high-throughput scenarios
- **Documentation**: Improve README, add tutorials, or create architecture diagrams

## 📋 Code Standards

- **Type Hints**: Required for all function signatures
- **Docstrings**: Google-style docstrings
- **Logging**: Use the `logging` module, not `print()`
- **Security**: Never commit secret keys or credentials

## 🛡️ Security

If you discover a security vulnerability, please email the maintainers directly rather than opening a public issue.

---

Thank you for helping make satellite security research more accessible! 🛰️
