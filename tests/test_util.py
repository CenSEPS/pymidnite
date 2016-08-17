import unittest
import mock

from midnite.util import USBMixin
from usb.core import Device


class TestUSBMixin(unittest.TestCase):

    @mock.patch('usb.core.find')
    @mock.patch('usb.util.get_string')
    def test_usb_init(self, mock_get_string, mock_find):
        # the order of get_string being called doesnt actually matter
        # so rather than an iterable for side effect the function below
        # is used. This will allow get_string calls to be issued in any order
        side_effect = [
            'fake_manufacturer',
            'fake_product',
            'fake_serialnumber'
        ]

        def t_get_string(_, index):
            return side_effect[index]

        mock_get_string.side_effect = t_get_string
        mock_dev = mock.Mock(spec=Device)
        mock_dev.iManufacturer = 0
        mock_dev.iProduct = 1
        mock_dev.iSerialNumber = 2
        mock_find.return_value = mock_dev
        u = USBMixin()
        t_idVendor = 0xDEAD
        t_idProduct = 0xBEEF
        u.usb_init(idVendor=t_idVendor, idProduct=t_idProduct)
        self.assertIs(u.usb_dev, mock_dev)
        mock_find.assert_called_once_with(
            idVendor=t_idVendor,
            idProduct=t_idProduct
        )
        self.assertEqual(u.manufacturer, side_effect[mock_dev.iManufacturer])
        self.assertEqual(u.product, side_effect[mock_dev.iProduct])
        self.assertEqual(u.serial_number, side_effect[mock_dev.iSerialNumber])
        self.assertEqual(mock_get_string.call_count, 3)
        self.assertIn(mock.call(mock_dev, mock_dev.iManufacturer),
                      mock_get_string.call_args_list)
        self.assertIn(mock.call(mock_dev, mock_dev.iProduct),
                      mock_get_string.call_args_list)
        self.assertIn(mock.call(mock_dev, mock_dev.iSerialNumber),
                      mock_get_string.call_args_list)
