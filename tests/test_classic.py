import unittest
from midnite.classic import _msb, _lsb, MidniteClassicModbusRegisters,\
    MidniteClassicUSB


class TestPrivateFunctions(unittest.TestCase):
    def test_msb(self):
        a = 0x5711
        self.assertEquals(_msb(a), 0x57)
        a = 0x57110
        self.assertEquals(_msb(a), 0x05)
        a = 0x57
        self.assertEquals(_msb(a), 0x57)
        a = 0x5
        self.assertEquals(_msb(a), 0x05)

    def test_msb_exceptions(self):
        a = 'a'
        self.assertRaises(TypeError, _msb, a)
        a = 3.4
        self.assertRaises(TypeError, _msb, a)

    def test_lsb_exceptions(self):
        a = 'a'
        self.assertRaises(TypeError, _lsb, a)
        a = 3.4
        self.assertRaises(TypeError, _lsb, a)

    def test_lsb(self):
        a = 0x5711
        self.assertEquals(_lsb(a), 0x11)
        a = 0x57011
        self.assertEquals(_lsb(a), 0x11)
        a = 0x1
        self.assertEquals(_lsb(a), 0x1)


class TestMidniteClassicUSB(unittest.TestCase):

    def test_constructor(self):
        pass

    def test_parse_usb_line(self):
        # we need to take advantage of setup and teardown stuff soon
        testLine = "   6.5,    6.4,   14.0,    0.0,    0.0,     0\n"
        expected = {
            'PV_input_volts': 6.5,
            'Target_volts': 6.4,
            'Battery_volts_av': 14.0,
            'Battery_current_av': 0.0,
            'PV_input_amps': 0.0,
            'Battery_charging_power_watts': 0.0
        }
        rv = MidniteClassicUSB._parse_usb_data_line(testLine)
        self.assertDictEqual(rv, expected)


class TestDecodeEncodeLambdas(unittest.TestCase):
    def test_unit_id_decode(self):
        """UNIT_ID Register Decoder
        [register[0]]msb=pcb revision
        [register[0]]lsb=unit type
        """
        pcb_revision = 0xAA
        unit_type = 0xCC
        decode = MidniteClassicModbusRegisters.UNIT_ID['decode']
        registers = []
        registers.append((pcb_revision << 8) | unit_type)
        expected = {
            'pcb_revision': pcb_revision,
            'unit_type': unit_type
        }
        self.assertDictEqual(expected, decode(registers))
        registers = ['a']
        self.assertRaises(TypeError, decode, registers)
        registers = []
        self.assertRaises(IndexError, decode, registers)

    def test_unit_mac_address_decode(self):
        """UNIT_MAC_ADDRESS Register Decoder
        [register[0]lsb=octet 0
        [register[0]]msb=octet 1
        [register[1]]lsb=octet 2
        [register[1]]msb=octet 3
        [register[2]]lsb=octet 4
        [register[2]]msb=octet 5
        """
        octet0 = 0xFF
        octet1 = 0xFE
        octet2 = 0xFB
        octet3 = 0xFA
        octet4 = 0xF7
        octet5 = 0xF6
        decode = MidniteClassicModbusRegisters.UNIT_MAC_ADDRESS['decode']
        registers = []
        registers.append((octet1 << 8) | octet0)
        registers.append((octet3 << 8) | octet2)
        registers.append((octet5 << 8) | octet4)
        expected = {
            'mac_address': [hex(octet5),
                            hex(octet4),
                            hex(octet3),
                            hex(octet2),
                            hex(octet1),
                            hex(octet0)]
        }
        self.assertDictEqual(expected, decode(registers))
        registers = ['A', 'B', 'C']
        self.assertRaises(TypeError, decode, registers)
        registers = []
        self.assertRaises(IndexError, decode, registers)
