import streamlit as st
import hid
import contextlib


# Define the context manager for opening and closing the device
@contextlib.contextmanager
def open_device(vendor_id, product_id):
    device = None
    try:
        device = hid.device()
        device.open(vendor_id, product_id)
        yield device  # Yield the device for use within the context
    except Exception as e:
        st.error(f"Connection error: {e}")
    finally:
        if device:
            device.close()
            st.write("Device disconnected.")


st.title("pyCrafter 4500")

# Sidebar toggle for connection
with st.sidebar:
    on = st.toggle("CONNECT")

# Use the context manager to open and manage the device connection
if on:
    try:
        with open_device(0x0451, 0x6401) as device:
            st.write("Connected to device.")
            # Perform any device actions here
            # e.g., read/write commands using the `device` variable
            # st.write(f"Device details: {device}")
            st.success("Device is ready for operations.")
    except Exception as e:
        st.error(f"Error during operation: {e}")
else:
    st.write("Toggle to CONNECT to the device.")
