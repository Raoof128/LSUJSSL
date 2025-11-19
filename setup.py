#!/usr/bin/env python
"""
Setup script for leo-satellite-sim package.
For modern build systems, prefer pyproject.toml, but this is included for compatibility.
"""

from setuptools import setup, find_packages

# Read requirements from requirements.txt
with open("requirements.txt") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

# Read long description from README
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="leo-satellite-sim",
    version="1.0.0",
    author="Raouf",
    author_email="raouf@example.com",
    description="LEO Satellite Command Link Security Simulator with CCSDS and HMAC Authentication",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/leo-satellite-sim",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering",
        "Topic :: Security",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "sat-sim=satellite_sim.cli.sat_cli:app",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
