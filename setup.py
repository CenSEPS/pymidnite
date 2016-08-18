from setuptools import setup, find_packages

setup(
    name="pymidnite",
    version="0.1.0",
    author="Zachary W. Graham",
    description="A library for interacting with MidNite Solar\
        power electronics",
    keywords="modbus, MidNite Solar, usb",
    license="BSD",
    packages=find_packages(exclude=["tests"]),
    platforms=["Linux"],
    install_requires=[
        "pymodbus >= 1.2.0",
        "pyserial >= 3.1.1",
        "Twisted >= 16.3.0",
        "pyusb >= 1.0.0"
    ],
    extras_require={
        "develop": ["mock>=2.0.0", "nose2>=0.6.5", "flake8>=3.0.4"]
    },
    test_suite="nose2.collector.collector"
)
