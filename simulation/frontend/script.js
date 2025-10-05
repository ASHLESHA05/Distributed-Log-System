const nodes = [];
let simulationRunning = false;
let anomalyTimeout;

function layoutNodes() {
  const container = document.getElementById("nodesContainer");
  const svg = document.getElementById("connections");
  container.innerHTML = "";
  svg.innerHTML = "";

  // Get the actual size of the parent #circleContainer
  const circleContainer = document.getElementById("circleContainer");
  const size = circleContainer.clientWidth; // Since it's square (width == height)

  const centerX = size / 2;
  const centerY = size / 2;
  // Radius is based on the container size, leaving margin for the node circles (120/2 = 60)
  const radius = (size / 2) - 80; 

  nodes.forEach((node, i) => {
    const angle = (i / nodes.length) * 2 * Math.PI;
    const x = centerX + radius * Math.cos(angle);
    const y = centerY + radius * Math.sin(angle);

    node.x = x;
    node.y = y;

    const nodeSize = 120; // Matches the CSS .node width/height
    
    const div = document.createElement("div");
    div.className = `node ${node.active ? "active" : "stopped"}`;
    div.textContent = node.name;
    // Positioning: Subtract half the node's size to center it on the calculated (x, y) point
    div.style.left = `${x - (nodeSize / 2)}px`;
    div.style.top = `${y - (nodeSize / 2)}px`;
    div.onclick = () => toggleNode(node, div);

    container.appendChild(div);
  });

  drawConnections(svg);
}

function drawConnections(svg) {
  if (nodes.length < 2) return;

  nodes.forEach((from, i) => {
    const to = nodes[(i + 1) % nodes.length];
    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", from.x);
    line.setAttribute("y1", from.y);
    line.setAttribute("x2", to.x);
    line.setAttribute("y2", to.y);
    svg.appendChild(line);
  });
}

function createNode() {
  const name = prompt("Enter new node name:");
  if (!name) return;
  nodes.push({ name, active: false });
  layoutNodes();
  logMessage(`🟢 Node <b>${name}</b> created.`);
}

function toggleNode(node, el) {
  node.active = !node.active;
  el.classList.toggle("active", node.active);
  el.classList.toggle("stopped", !node.active);
  logMessage(`${node.active ? "▶ Started" : "⏹ Stopped"} node: <b>${node.name}</b>`);
  if (node.active) simulateNodeActivity(node);
}

function startSimulation() {
  if (simulationRunning || nodes.length === 0) return;
  simulationRunning = true;
  logMessage("🚀 Simulation started.");
  nodes.forEach(node => {
    node.active = true;
    simulateNodeActivity(node);
  });
  layoutNodes();
}

function stopAll() {
  simulationRunning = false;
  nodes.forEach(n => (n.active = false));
  // Clear any pending anomaly timeouts
  clearTimeout(anomalyTimeout);
  document.getElementById("anomalyBox").style.display = "none";
  layoutNodes();
  logMessage("🛑 All nodes stopped.");
}

function simulateNodeActivity(node) {
  if (!node.active || !simulationRunning) return; // Check global state too
  const randomDelay = Math.random() * 3000 + 1000;
  
  // Use a dedicated timeout property on the node to cancel it if the node is stopped individually
  node.activityTimeout = setTimeout(() => {
    if (!node.active) return;
    if (Math.random() < 0.15) { // Increased anomaly chance slightly for more action
      showAnomaly(node.name);
    }
    simulateNodeActivity(node);
  }, randomDelay);
}

function showAnomaly(nodeName) {
  const box = document.getElementById("anomalyBox");
  clearTimeout(anomalyTimeout);
  box.innerHTML = `⚠️ ANOMALY DETECTED IN <b>${nodeName}</b>!`;
  box.style.display = "block";
  anomalyTimeout = setTimeout(() => (box.style.display = "none"), 4000);
  logMessage(`<span style="color:var(--danger-color); font-weight:700;">⚠️ Anomaly detected in ${nodeName}</span>`);
}

function logMessage(msg) {
  const consoleBox = document.getElementById("console");
  const ts = new Date().toLocaleTimeString();
  consoleBox.innerHTML += `<span style="color:var(--text-muted);">[${ts}]</span> ${msg}<br>`;
  consoleBox.scrollTop = consoleBox.scrollHeight;
}

// === Initial Setup and Event Listeners ===
document.getElementById("createNodeBtn").onclick = createNode;
document.getElementById("startBtn").onclick = startSimulation;
document.getElementById("stopAllBtn").onclick = stopAll;

// Initial node creation
["Producer", "Kafka", "Backend", "AI Reporter", "Dashboard", "Database"].forEach(name =>
  nodes.push({ name, active: false })
);

// Rerender layout on window resize to keep nodes centered/circular
window.addEventListener('resize', layoutNodes);

// Initial layout call
layoutNodes();