import streamlit as st
import json
import socketio

from pycrafter4500.usb_drivers import DLCPWebHID

# Connect to the Flask server
sio = socketio.Client()
sio.connect("http://localhost:8765")
dlp = DLCPWebHID(sio)


# Function to emit data to the server
def send_to_usb(data):
    sio.emit("send_command", json.dumps(data))


# UI Components
st.title("USB Device Controller")

# Device Connection
if st.button("Connect to Device"):
    send_to_usb({"type": "connect"})

on = st.toggle("standby")
if on:
    buffer = [64, 0, 3, 0, 0, 2]
    send_to_usb({"type": "send_command", "buffer": buffer})
    dlp.set_power_mode(do_standby=False)
else:
    dlp.set_power_mode(do_standby=True)


# Other UI elements as needed
st.text("Status will be displayed below.")

# JavaScript injection for WebHID
with open("pycrafter4500/app/static/webhid.js", "r") as js_file:
    js_code = js_file.read()

html_code = f"""
<div id="status">Status: Not connected</div>
<script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>
<script>
{js_code}
</script>
"""

# Embed HTML and JavaScript in Streamlit
st.components.v1.html(html_code, height=300)
