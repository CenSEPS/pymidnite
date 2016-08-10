from pymodbus.client.sync import ModbusTcpClient
import logging


def _msb(value):
    return (value >> 8)


def _lsb(value):
    return (value & 0xFF)

# TODO: Figure out how to make register decoding work from this class?
# Idea: Lambda functions functions for each register
# TODO: Mark which registers get saved to EEPROM


class MidniteClassicRegisters(object):

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


class MidniteClassic(object):

    registers = MidniteClassicRegisters.get_register_list()

    def _addr(self, addr):
        return addr-1

    def __init__(self, host, port):
        # check if host/port are none?
        super(MidniteClassic, self).__setattr__(
            'client', ModbusTcpClient(host, port))
        # self.client = ModbusTcpClient(host, port)

    def __getattr__(self, name):
        if name in self.registers:
            register_dict = getattr(MidniteClassicRegisters, name)
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
            register_dict = getattr(MidniteClassicRegisters, name)
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


if __name__ == "__main__":
    midnite = MidniteClassic('192.168.1.10', 502)
    res = midnite.UNIT_ID
    print res
    res = midnite.UNIT_SW_DATE_RO
    print res
    res = midnite.UNIT_MAC_ADDRESS
    print res
