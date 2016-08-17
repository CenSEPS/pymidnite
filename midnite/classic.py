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
from pymodbus.client.sync import ModbusTcpClient
from serial import Serial
from util import USBMixin
# import logging


def _msb(value):
    if type(value) != int:
        raise TypeError("Function _msb only takes arguments of type 'int'")
    bits = value.bit_length()
    byte_mod = bits % 8
    if byte_mod == 0:
        return (value >> (bits-8))
    else:
        return (value >> (bits/8)*8)
        # take advantage of integer division to
        # shift the appropriate ammount


def _lsb(value):
    if type(value) != int:
        raise TypeError("Function _lsb only takes arguments of type 'int'")
    return (value & 0xFF)

# TODO: Figure out how to make register decoding work from this class?
# Idea: Lambda functions functions for each register
# TODO: Mark which registers get saved to EEPROM


class MidniteClassicModbusRegisters(object):

    @classmethod
    def get_register_list(cls):
        return [key for key, value in cls.__dict__.items()
                if not key.startswith('__')
                and not callable(key)]

    UNIT_ID = {
        'address': 4101, 'count': 1,
        'readable': True, 'writeable': False,
        'decode': (lambda v: {
                   'pcb_revision': _msb(v[0]),
                   'unit_type': _lsb(v[0])})
    }

    UNIT_SW_DATE_RO = {
        'address': 4102, 'count': 2,
        'readable': True, 'writeable': False,
        'decode': (lambda v: {
                   'year': v[0],
                   'month': _msb(v[1]),
                   'day': _lsb(v[1])})
    }

    INFO_FLAG_BITS_3 = {'address': 4104, 'count': 1,
                        'readable': True, 'writeable': False}

    UNIT_MAC_ADDRESS = {
        'address': 4106, 'count': 3,
        'readable': True, 'writeable': False,
        'decode': (lambda v: {
            'mac_address': [hex(_msb(v[2])),
                            hex(_lsb(v[2])),
                            hex(_msb(v[1])),
                            hex(_lsb(v[1])),
                            hex(_msb(v[0])),
                            hex(_lsb(v[0]))]})
    }

    UNIT_DEVICE_ID = {'address': 4111, 'count': 2,
                      'readable': True, 'writeable': False}

    STATUS_ROLL = {'address': 4113, 'count': 1,
                   'readable': True, 'writeable': False}

    RESTART_TIMER_MS = {'address': 4114, 'count': 1,
                        'readable': True, 'writeable': False}

    DISP_AVG_VBATT = {'address': 4115, 'count': 1,
                      'readable': True, 'writeable': False}

    DISP_AVG_VPV = {'address': 4116, 'count': 1,
                    'readable': True, 'writeable': False}

    DISP_AVG_IBATT = {'address': 4117, 'count': 1,
                      'readable': True, 'writeable': False}

    DAILY_KWH = {'address': 4118, 'count': 1,
                 'readable': True, 'writeable': False}

    AVG_WATTS = {'address': 4119, 'count': 1,
                 'readable': True, 'writeable': False}

    COMBO_CHARGE_STAGE = {'address': 4120, 'count': 1,
                          'readable': True, 'writeable': False}

    AVG_PV_CURRENT = {'address': 4121, 'count': 1,
                      'readable': True, 'writeable': False}

    LAST_VOC = {'address': 4122, 'count': 1,
                'readable': True, 'writeable': False}

    HIGHEST_PV_VOLTS = {'address': 4123, 'count': 1,
                        'readable': True, 'writeable': False}

    MATCH_POINT_SHADOW = None  # no desire to expose wind power functionality

    DAILY_AMP_HOURS = {'address': 4125, 'count': 1,
                       'readable': True, 'writeable': False}

    LIFETIME_KWH = {'address': 4126, 'count': 2,
                    'readable': True, 'writeable': False}

    LIFETIME_AMP_HOURS = {'address': 4128, 'count': 2,
                          'readable': True, 'writeable': False}

    INFO_FLAG_BITS_2 = {'address': 4130, 'count': 2,
                        'readable': True, 'writeable': False}

    BATT_TEMPERATURE = {'address': 4132, 'count': 1,
                        'readable': True, 'writeable': False}

    FET_TEMPERATURE = {'address': 4133, 'count': 1,
                       'readable': True, 'writeable': False}

    PCB_TEMPERATURE = {'address': 4134, 'count': 1,
                       'readable': True, 'writeable': False}

    # SKIP A FEW

    LED_MODE = {'address': 4207, 'count': 1,
                'readable': True, 'writeable': True}


class MidniteClassicTCP(object):

    registers = MidniteClassicModbusRegisters.get_register_list()

    def _addr(self, addr):
        return addr-1

    def __init__(self, host, port):
        # check if host/port are none?
        super(MidniteClassicTCP, self).__setattr__(
            'client', ModbusTcpClient(host, port))
        # self.client = ModbusTcpClient(host, port)

    def __getattr__(self, name):
        if name in self.registers:
            register_dict = getattr(MidniteClassicModbusRegisters, name)
            if register_dict is None:
                raise AttributeError(
                    "Register {} is not implemented.".format(name))
            if register_dict['readable']:
                self.client.connect()
                result = self.client.read_holding_registers(
                    address=self._addr(register_dict['address']),
                    count=register_dict['count']
                )
                if 'decode' in register_dict.keys():
                    decoder = register_dict['decode']
                    result = decoder(result.registers)
                return result
            else:
                raise AttributeError(
                    "Register {} is not readable.".format(name))
        else:
            raise AttributeError("Register {} is invalid".format(name))

    def __setattr__(self, name, value):
        if name in self.registers:
            register_dict = getattr(MidniteClassicModbusRegisters, name)
            if register_dict is None:
                raise AttributeError(
                    "Register {} is not implemented".format(name))
            if register_dict['writable']:
                raise NotImplementedError(
                    "Write operations have not been implemented yet")
            else:
                raise AttributeError(
                    "Register {} is not writable".format(name))
        else:
            raise AttributeError("Register {} is invalid".format(name))


class MidniteClassicUSB(USBMixin, object):
    """USB Connected MidniteClassic
    Classic can dump all modbus registers or, by default,
    "PV Input Volts, Target Volts, Average batt volts,
    Averaget Batt amps, PV Input Amps, Average Batt Power (charging) Watts\r\n"
    twice per second
    """
    idVendor = 0xFFFF

    idProduct = 0x0005

    def __init__(self, port, baud=9600,
                 bytesize=8, parity='N',
                 stopbits=1, timeout=None):
        self.port = port
        self.baud = baud
        self.byte_size = bytesize
        self.parity = parity
        self.stop_bits = stopbits
        self.timeout = timeout
        self.ser = Serial(
            port=port,
            baudrate=baud,
            bytesize=bytesize,
            parity=parity,
            stopbits=stopbits,
            timeout=timeout)
        self.usb_init(idVendor=self.idVendor, idProduct=self.idProduct)

    @classmethod
    def _parse_usb_data_line(cls, line):
        values = line.split(',')
        if len(values) != 6:
            raise MidniteClassicDataError("Recieved Bad Line")
            # we need a custom exception to catch for a bad data line
        else:
            return {
                'PV_input_volts': float(values[0]),
                'Target_volts': float(values[1]),
                'Battery_volts_av': float(values[2]),
                'Battery_current_av': float(values[3]),
                'PV_input_amps': float(values[4]),
                'Battery_charging_power_watts': float(values[5])
            }

    def read_one_line(self):
        if self.ser.readable():
            self.ser.flushInput()
            while True:
                # self.ser.readline()     # throw away incomplete reading
                try:
                    l = self.ser.readline()
                    parsed_line = self._parse_usb_data_line(
                        l.strip('\r')
                    )
                except MidniteClassicDataError:
                    continue
                else:
                    break
            return parsed_line
        else:
            raise MidniteClassicUSBError("usb(serial) port not readable")


class MidniteClassicDataError(Exception):
    pass


class MidniteClassicUSBError(Exception):
    pass

if __name__ == "__main__":
    midnite = MidniteClassicTCP('192.168.1.10', 502)
    res = midnite.UNIT_ID
    print res
    res = midnite.UNIT_SW_DATE_RO
    print res
    res = midnite.UNIT_MAC_ADDRESS
    print res
