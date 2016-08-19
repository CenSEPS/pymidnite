import unittest
import mock

from midnite.classic import _msb, _lsb, MidniteClassicModbusRegisters,\
    MidniteClassicUSB, MidniteClassicDataError, MidniteClassicUSBError,\
    MidniteClassicTCP
from pymodbus.register_read_message import ReadHoldingRegistersResponse  # noqa


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


class TestMidniteClassicTCP(unittest.TestCase):

    @mock.patch('midnite.classic.ModbusTcpClient')
    def test_constructor(self, mock_modbus_client):
        t_host = 'fakehost'
        t_port = 500
        m = MidniteClassicTCP(t_host, t_port)
        self.assertIsNot(m.client, None)
        mock_modbus_client.assert_called_once_with(t_host, t_port)

    def test__addr(self):
        t_val = 4001
        expected = t_val - 1
        self.assertEqual(
            expected,
            MidniteClassicTCP._addr(t_val)
        )
        t_val = 4.0
        self.assertRaises(
            TypeError,
            MidniteClassicTCP._addr,
            t_val
        )
        t_val = 's'
        self.assertRaises(
            TypeError,
            MidniteClassicTCP._addr,
            t_val
        )

    @mock.patch('midnite.classic.ModbusTcpClient')
    def test_getattr_with_valid_input(self, mock_tcp_client):
        # prepare test variables
        t_host, t_port = 'fakehost', 500
        t_register = 'VALID_REGISTER'
        t_register_addr = 5000
        t_register_size = 1
        t_register_info_no_decoder = {
            'address': t_register_addr,
            'count': t_register_size,
            'readable': True,
            'writeable': False,
        }
        t_register_info_with_decoder = t_register_info_no_decoder
        t_register_info_with_decoder['decode'] = lambda v: {'mock': v}
        # prepare mock objects to return valid responses
        t_register_contents = ['coolmodbusstuff']
        t_modbus_response = mock.Mock()
        # sometimes the mock library confuses me vvv
        type(t_modbus_response).registers = \
            mock.PropertyMock(return_value=t_register_contents)
        mtc = mock_tcp_client.return_value
        mtc.read_holding_registers.return_value = t_modbus_response
        MidniteClassicTCP.registers = \
            mock.PropertyMock(return_value=[t_register])
        setattr(
            MidniteClassicModbusRegisters,
            t_register,
            mock.PropertyMock(return_value=t_register_info_no_decoder)
        )
        m = MidniteClassicTCP(t_host, t_port)
        expected = {'mock': t_register_contents}
        a = getattr(m, t_register)
        self.assertDictEqual(a, expected)


class TestMidniteClassicUSB(unittest.TestCase):

    @mock.patch('midnite.classic.Serial')
    @mock.patch.object(MidniteClassicUSB, 'usb_init')
    def test_constructor(self, mock_usb_init, mock_serial):
        serial_dev = '/dev/fakeserial'
        def_baud = 9600
        def_byte_size = 8
        def_parity = 'N'
        def_stop_bits = 1
        def_timeout = None
        m = MidniteClassicUSB(serial_dev)
        self.assertEqual(m.port, serial_dev)
        self.assertEqual(m.baud, def_baud)
        self.assertEqual(m.byte_size, def_byte_size)
        self.assertEqual(m.parity, def_parity)
        self.assertEqual(m.stop_bits, def_stop_bits)
        self.assertIs(m.timeout, def_timeout)
        mock_serial.assert_called_once_with(
            port=serial_dev,
            baudrate=def_baud,
            bytesize=def_byte_size,
            parity=def_parity,
            stopbits=def_stop_bits,
            timeout=def_timeout
        )
        mock_usb_init.assert_called_once_with(
            idVendor=MidniteClassicUSB.id_vendor,
            idProduct=MidniteClassicUSB.id_product
        )

        mock_serial.reset_mock()
        mock_usb_init.reset_mock()
        del m
        serial_dev = 'COMFAKE'
        t_baud = 38400
        t_byte_size = 5
        t_parity = 'E'
        t_stop_bits = 1.5
        t_timeout = 10
        m = MidniteClassicUSB(
            serial_dev,
            t_baud,
            t_byte_size,
            t_parity,
            t_stop_bits,
            t_timeout
        )
        self.assertEqual(m.port, serial_dev)
        self.assertEqual(m.baud, t_baud)
        self.assertEqual(m.byte_size, t_byte_size)
        self.assertEqual(m.parity, t_parity)
        self.assertEqual(m.stop_bits, t_stop_bits)
        self.assertEqual(m.timeout, t_timeout)
        mock_serial.assert_called_once_with(
            port=serial_dev,
            baudrate=t_baud,
            bytesize=t_byte_size,
            parity=t_parity,
            stopbits=t_stop_bits,
            timeout=t_timeout
        )
        mock_usb_init.assert_called_once_with(
            idVendor=MidniteClassicUSB.id_vendor,
            idProduct=MidniteClassicUSB.id_product
        )

    def test_parse_usb_line(self):
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
        testLine = "   6.5,    6.4,   14.0,\n"
        self.assertRaises(
            MidniteClassicDataError,
            MidniteClassicUSB._parse_usb_data_line,
            testLine
        )
        testLine = ""
        self.assertRaises(
            MidniteClassicDataError,
            MidniteClassicUSB._parse_usb_data_line,
            testLine
        )

    @mock.patch('midnite.classic.Serial')
    @mock.patch.object(MidniteClassicUSB, 'usb_init')
    def test_read_one_line(self, mock_usb_init, mock_serial):
        ms = mock_serial.return_value
        ms.readable.return_value = False
        m = MidniteClassicUSB(port="fakeport")
        self.assertRaises(MidniteClassicUSBError, m.read_one_line)
        ms.readline.assert_not_called()
        ms.flushInput.assert_not_called()
        ms.readable.assert_called_once()

        testLine = "   6.5,    6.4,   14.0,    0.0,    0.0,     0\n"
        expected = {
            'PV_input_volts': 6.5,
            'Target_volts': 6.4,
            'Battery_volts_av': 14.0,
            'Battery_current_av': 0.0,
            'PV_input_amps': 0.0,
            'Battery_charging_power_watts': 0.0
        }
        ms.reset_mock()
        ms.readable.return_value = True
        ms.readline.return_value = testLine
        self.assertDictEqual(expected, m.read_one_line())
        ms.readable.assert_called_once()
        ms.flushInput.assert_called()
        ms.readline.assert_called_once()

    @mock.patch('midnite.classic.Serial', autospec=True)
    @mock.patch.object(MidniteClassicUSB, 'usb_init')
    def test_read_one_line_with_bad_input_first(
        self,
        mock_usb_init,
        mock_serial
    ):
        ms = mock_serial.return_value
        t_serial_dev = 'fake'
        t_lines = [
            "\r   6.5,    6.4,   14.0,\n",
            "\r   6.5,    6.4,   14.0,    0.0,    0.0,     0\n"
        ]
        expected = {
            'PV_input_volts': 6.5,
            'Target_volts': 6.4,
            'Battery_volts_av': 14.0,
            'Battery_current_av': 0.0,
            'PV_input_amps': 0.0,
            'Battery_charging_power_watts': 0.0
        }
        ms.readline.side_effect = t_lines
        m = MidniteClassicUSB(t_serial_dev)
        self.assertDictEqual(m.read_one_line(), expected)
        ms.readable.assert_called_once()
        ms.flushInput.assert_called_once()
        self.assertEquals(ms.readline.call_count, 2)


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
