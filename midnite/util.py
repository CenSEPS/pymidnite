import usb


class USBMixin(object):
    """Exposes methods to get information about a USB Device

    The Deferrable Load Testbed can communicate with several different
    USB-connected power electronics. While they provide CDC-ACM
    communications, our dashboard management software needs to properly
    identify them. This mixin class provides the appropriate interface
    to connect with our MQTT-based management system.
    """

    def usb_init(self, idVendor, idProduct):
        self.usb_dev = usb.core.find(idVendor=idVendor, idProduct=idProduct)
        self.manufacturer = usb.util.get_string(
            self.usb_dev,
            self.usb_dev.iManufacturer
        )
        self.product = usb.util.get_string(
            self.usb_dev,
            self.usb_dev.iProduct
        )
        self.serial_number = usb.util.get_string(
            self.usb_dev,
            self.usb_dev.iSerialNumber
        )
