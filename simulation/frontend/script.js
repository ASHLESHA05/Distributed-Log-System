const logBox = document.getElementById("logBox");

function addLog(message, type = "") {
    const div = document.createElement("div");
    div.className = "log-line " + type;
    div.textContent = `[${new Date().toLocaleTimeString()}]  ${message}`;
    logBox.appendChild(div);
    logBox.scrollTop = logBox.scrollHeight;
}

async function trigger(path) {
    try {
        await fetch(path, { method: "POST" });
    } catch (e) {
        addLog("ERROR: " + e.message, "log-error");
    }
}

const wsProtocol = location.protocol === "https:" ? "wss:" : "ws:";
const ws = new WebSocket(wsProtocol + "//" + location.host + "/ws/logs");

ws.onopen = () => addLog("WebSocket Connected", "log-success");

ws.onmessage = (event) => {
    const msg = event.data;

    if (msg.includes("ERROR")) addLog(msg, "log-error");
    else if (msg.includes("WARN")) addLog(msg, "log-warn");
    else if (msg.includes("DEBUG")) addLog(msg, "log-debug");
    else if (msg.includes("INTERRUPT")) addLog("[HEARTBEAT INTERRUPTED]", "log-rabbit");
    else addLog(msg, "log-success");
};

ws.onclose = () => addLog("WebSocket Closed", "log-error");
ws.onerror = () => addLog("WebSocket Error", "log-error");
