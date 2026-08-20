const history = {
    timestamps: [],
    latency: [],
    download: [],
    upload: []
};

const MAX_HISTORY = 120;

function addHistorySample(health, bandwidth) {
    const now = new Date();

    history.timestamps.push(
        now.toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit"
        })
    );

    history.latency.push(
        health.ping.avg_latency_ms ?? 0
    );

    history.download.push(
        bandwidth.download_rate_mbps
    );

    history.upload.push(
        bandwidth.upload_rate_mbps
    );

    if (history.timestamps.length > MAX_HISTORY) {
        history.timestamps.shift();
        history.latency.shift();
        history.download.shift();
        history.upload.shift();
    }
}

function drawLineChart(canvasId, datasets, unit) {
    const canvas = document.getElementById(canvasId);
    const ctx = canvas.getContext("2d");

    const width = canvas.clientWidth;
    const height = canvas.clientHeight;

    const dpr = window.devicePixelRatio || 1;

    canvas.width = width * dpr;
    canvas.height = height * dpr;

    ctx.scale(dpr, dpr);

    ctx.clearRect(0, 0, width, height);

    const padding = {
        top: 20,
        right: 20,
        bottom: 30,
        left: 50
    };

    const chartWidth =
        width - padding.left - padding.right;

    const chartHeight =
        height - padding.top - padding.bottom;

    const allValues = datasets.flatMap(
        dataset => dataset.values
    );

    const maxValue = Math.max(
        ...allValues,
        1
    );

    // Grid lines and labels
    ctx.strokeStyle = "#252e3d";
    ctx.fillStyle = "#687386";
    ctx.font = "11px sans-serif";

    const gridLines = 4;

    for (let i = 0; i <= gridLines; i++) {
        const y =
            padding.top +
            (chartHeight / gridLines) * i;

        ctx.beginPath();
        ctx.moveTo(padding.left, y);
        ctx.lineTo(width - padding.right, y);
        ctx.stroke();

        const value =
            maxValue -
            (maxValue / gridLines) * i;

        ctx.fillText(
            `${value.toFixed(1)} ${unit}`,
            4,
            y + 4
        );
    }

    if (history.timestamps.length < 2) {
        ctx.fillStyle = "#687386";
        ctx.fillText(
            "Collecting data...",
            padding.left,
            padding.top + 20
        );

        return;
    }

    datasets.forEach(dataset => {
        ctx.strokeStyle = dataset.color;
        ctx.lineWidth = 2;
        ctx.beginPath();

        dataset.values.forEach((value, index) => {
            const x =
                padding.left +
                (index /
                    (history.timestamps.length - 1)) *
                    chartWidth;

            const y =
                padding.top +
                chartHeight -
                (value / maxValue) * chartHeight;

            if (index === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        });

        ctx.stroke();
    });

    // Current time labels
    const firstTimestamp = history.timestamps[0];
    const lastTimestamp =
        history.timestamps[
            history.timestamps.length - 1
        ];

    ctx.fillStyle = "#687386";

    ctx.fillText(
        firstTimestamp,
        padding.left,
        height - 8
    );

    const lastWidth =
        ctx.measureText(lastTimestamp).width;

    ctx.fillText(
        lastTimestamp,
        width - padding.right - lastWidth,
        height - 8
    );
}

function updateCharts() {
    drawLineChart(
        "latency-chart",
        [
            {
                values: history.latency,
                color: "#f4f7fb"
            }
        ],
        "ms"
    );

    drawLineChart(
        "bandwidth-chart",
        [
            {
                values: history.download,
                color: "#6ee7a8"
            },
            {
                values: history.upload,
                color: "#7aa2ff"
            }
        ],
        "Mbps"
    );
}

async function updateMetrics() {
    try {
        const response = await fetch("/metrics");
        const data = await response.json();

        const health = data.health;
        const bandwidth = data.bandwidth;

        addHistorySample(health, bandwidth);
        updateCharts();

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

window.addEventListener("resize", updateCharts);