# -*- coding: utf-8 -*-
# TODO add copy of license here

"""midnite - interact with MidNite Solar power electronics

This module aids in data collection from MidNite Solar power electronics.
Currently, only the 'Classic' models are supported.

    - classic.MidniteClassicModbus is not fully implemented but is
    designed to allow easy reading and writing to the MidNite Classic modbus
    registers over Modbus/TCP.
iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
    - classic.MidniteClassicUSB is designed to collect data over the usb port.
    The modbus register dump functionality is not implemented, instead the
    default behavior of sending, six specific values over 0.5 seconds is
    handled. The behavior is not implemented so that every piece of data is
    collected, it will flush all input, then proceed to read the first full
    line from the attached MidNite Classic.

    - USBMixin is specific to the CenSEPS group for our telemetry system.
    USBMixin will eventually be moved to a different module.
"""

__author__ = "Zachary W. Graham"
version_info = (0, 1, 0)
__version__ = "{}.{}.{}".format(
    version_info[0],
    version_info[1],
    version_info[2]
)

from classic import MidniteClassicUSB

__all__ = ['classic']
