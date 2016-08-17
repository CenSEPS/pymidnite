# -*- coding: utf-8 -*-
# Copyright (c) 2016, Regents of the University of California and the Center
# for Sustainable Energy and Power Systems (CenSEPS)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the University of California, Santa Cruz nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""midnite - interact with MidNite Solar power electronics

This module aids in data collection from MidNite Solar power electronics.
Currently, only the 'Classic' models are supported.

    - classic.MidniteClassicModbus is not fully implemented but is
    designed to allow easy reading and writing to the MidNite Classic modbus
    registers over Modbus/TCP.
    - classic.MidniteClassicUSB is designed to collect data over the usb port.
    The modbus register dump functionality is not implemented, instead the
    default behavior of sending, six specific values over 0.5 seconds is
    handled. The behavior is not implemented so that every piece of data is
    collected, it will flush all input, then proceed to read the first full
    line from the attached MidNite Classic.

    - USBMixin is specific to the CenSEPS group for our telemetry system.
    USBMixin will eventually be moved to a different module.
"""
# from classic import MidniteClassicUSB  # noqa

__author__ = "Zachary W. Graham"
__copyright__ = "Copyright 2016, Regents of the University of California"
__license__ = "BSD-new"
version_info = (0, 1, 0)
__version__ = "{}.{}.{}".format(
    version_info[0],
    version_info[1],
    version_info[2]
)
__maintainer__ = "Zachary W. Graham"
__email__ = "zwgraham@soe.ucsc.edu"
__status__ = "Beta"


__all__ = ['classic.MidniteClassicUSB']
