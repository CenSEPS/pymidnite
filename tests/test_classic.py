import unittest
from midnite.classic import _msb, _lsb


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
