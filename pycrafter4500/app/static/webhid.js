let device;
const socket = io("http://127.0.0.1:8765");

socket.on("connect", () => {
    console.log("Connected to WebSocket server");
});

socket.on("relay_to_client", async (event) => {
    const data = JSON.parse(event);

    if (data.type === "connect") {
        connectDevice();
    } else if (data.type === "send_command") {
        sendToDevice(data.buffer);
    }
});

async function connectDevice() {
    try {
        const devices = await navigator.hid.requestDevice({ filters: [{ vendorId: 0x0451 }] });
        if (devices.length > 0) {
            device = devices[0];
            await device.open();
            console.log("Connected to device:", device.productName);
            document.getElementById("status").innerText = "Connected to " + device.productName;
        } else {
            alert("No device selected.");
        }
    } catch (error) {
        console.error("Device connection failed:", error);
    }
}

async function sendToDevice(data) {
    if (device && device.opened) {
        try {
            const buffer = new Uint8Array(data);
            await device.sendReport(0x00, buffer);
            console.log("Sent data to device:", buffer);
        } catch (error) {
            console.error("Error sending data to device:", error);
        }
    } else {
        console.error("Device not connected.");
        document.getElementById("status").innerText = "Device not connected.";
    }
}
