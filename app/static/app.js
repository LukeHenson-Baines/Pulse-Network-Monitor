async function updateMetrics() {
    try {
        const response = await fetch("/metrics");
        const data = await response.json();

        const health = data.health;
        const bandwidth = data.bandwidth;

        const status = document.getElementById("connection-status");

        status.textContent =
            health.status.charAt(0).toUpperCase() +
            health.status.slice(1);

        status.className = `status-badge ${health.status}`;

        document.getElementById("ping").textContent =
            health.ping.avg_latency_ms ?? "--";

        document.getElementById("packet-loss").textContent =
            health.ping.packet_loss_percent ?? "--";

        document.getElementById("download-rate").textContent =
            bandwidth.download_rate_mbps;

        document.getElementById("upload-rate").textContent =
            bandwidth.upload_rate_mbps;

        document.getElementById("total-received").textContent =
            `${bandwidth.total_megabytes_received} MB`;

        document.getElementById("total-sent").textContent =
            `${bandwidth.total_megabytes_sent} MB`;

        document.getElementById("packets-received").textContent =
            bandwidth.packets_received.toLocaleString();

        document.getElementById("packets-sent").textContent =
            bandwidth.packets_sent.toLocaleString();

    } catch (error) {
        const status = document.getElementById("connection-status");
        status.textContent = "Error";
        status.className = "status-badge offline";

        console.error("Failed to retrieve metrics:", error);
    }
}


async function runSpeedTest() {
    const button = document.getElementById("speed-test-button");

    button.disabled = true;
    button.textContent = "Testing...";

    try {
        const response = await fetch("/speed");
        const data = await response.json();

        if (data.status !== "success") {
            throw new Error(data.message || "Speed test failed");
        }

        document.getElementById("speed-download").textContent =
            `${data.download_mbps} Mbps`;

        document.getElementById("speed-upload").textContent =
            `${data.upload_mbps} Mbps`;

        document.getElementById("speed-ping").textContent =
            `${data.ping_ms} ms`;

        document.getElementById("speed-jitter").textContent =
            `${data.jitter_ms} ms`;

        document.getElementById("speed-server").textContent =
            `Test server: ${data.server}`;

    } catch (error) {
        document.getElementById("speed-server").textContent =
            `Speed test failed: ${error.message}`;
    } finally {
        button.disabled = false;
        button.textContent = "Run Speed Test";
    }
}


document
    .getElementById("speed-test-button")
    .addEventListener("click", runSpeedTest);


updateMetrics();

setInterval(updateMetrics, 5000);