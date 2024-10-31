import hid
import time

from pycrafter4500.dlpc import DLPCBase


class BaseConnector:
    def __init__(
        self, vendor=0x0451, product_id=0x6401, max_retries=5, retry_delay=1.0
    ):
        self.device = None
        self.vendor = vendor
        self.product_id = product_id
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def connect_to_device(self):
        """Actual device connection logic to be implemented by subclasses."""
        raise NotImplementedError(
            "Subclasses must implement the connect_to_device method."
        )

    def connect(self):
        """Attempts to connect with retry mechanism."""
        for attempt in range(1, self.max_retries + 1):
            try:
                self.connect_to_device()
                print("Device connected.")
                return self.device  # Return device if connection is successful
            except Exception as e:
                print(f"Connection attempt {attempt} failed: {e}")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)
                else:
                    print("Max retries reached. Connection failed.")
                    raise

    def disconnect(self):
        """Actual device disconnect logic to be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement the disconnect method.")

    def __enter__(self):
        # hidapi seems not to work with context manager protocol
        # try contextlib's contextmanager instead
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        # hidapi seems not to work with context manager protocol
        # try contextlib's contextmanager instead
        pass


class MacOSConnector(BaseConnector):
    def connect_to_device(self):
        """Open the USB connection using hid."""
        if self.device is not None:
            print("Already connected to device.")
            return

        self.device = hid.device()
        self.device.open(
            self.vendor, self.product_id
        )  # Using inherited vendor and product ID

    def disconnect(self):
        """Closes the connection to the USB device."""
        if self.device:
            self.device.close()
            self.device = None
            print("Device disconnected.")


class DLPCPyUSB(DLPCBase):
    def write(self, buffer):
        self.dlpc.write(1, buffer)

    def read(self, buffer):
        return self.dlpc.read(0x81, buffer)


class DLPCHydAPI(DLPCBase):
    def write(self, buffer):
        self.dlpc.write(buffer)

    def read(self, buffer):
        return self.dlpc.read(buffer)
