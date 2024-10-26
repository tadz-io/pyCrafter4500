from abc import ABC, abstractmethod
from contextlib import contextmanager
from pycrafter4500 import macos

import hid


class BaseConnector(ABC):
    def __init__(self):
        self.device = None

    @contextmanager
    def connect(self):
        """Connect to the USB device in a platform-specific way."""
        # Setup phase: Delegate to platform-specific connection setup
        lcr = self._setup_connection()

        try:
            # Yield the device for usage in the context block
            yield lcr
        finally:
            # Teardown phase: Delegate to platform-specific disconnection
            self._teardown_connection(self.device)

    @abstractmethod
    def _setup_connection(self):
        """Platform-specific connection setup (implemented by subclass)."""
        pass

    @abstractmethod
    def _teardown_connection(self, device):
        """Platform-specific disconnection (implemented by subclass)."""
        pass


class MacOSConnector(BaseConnector):
    def _setup_connection(self) -> macos.dlpc350:
        """Set up the USB device connection on macOS using hidapi."""
        device = hid.device()
        device.open(0x0451, 0x6401)  # Replace with actual vendor and product IDs
        self.device = device
        return macos.dlpc350(device)

    def _teardown_connection(self, device):
        """Teardown the USB device connection on macOS."""
        device.close()
        del self.device
