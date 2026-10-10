
const API_BASE_URL = "http://localhost:5000/api";

// ======================================
// Crop prediction
// ======================================

async function predictCrop() {
    const button = document.getElementById("predictBtn");
    const result = document.getElementById("result");

    const fields = [
        "nitrogen",
        "phosphorus",
        "potassium",
        "temperature",
        "humidity",
        "ph",
        "rainfall"
    ];

    const inputElements = fields.map(id => document.getElementById(id));

    inputElements.forEach(input => input.classList.remove("error"));

    const values = inputElements.map(input => input.value.trim());

    if (values.some(value => value === "" || !Number.isFinite(Number(value)))) {
        inputElements.forEach((input, index) => {
            if (values[index] === "" || !Number.isFinite(Number(values[index]))) {
                input.classList.add("error");
            }
        });

        result.textContent = "Please enter valid numbers in all fields.";
        return;
    }

    const [
        nitrogen,
        phosphorus,
        potassium,
        temperature,
        humidity,
        ph,
        rainfall
    ] = values.map(Number);

    if (
        nitrogen < 0 ||
        phosphorus < 0 ||
        potassium < 0 ||
        temperature < -20 ||
        humidity < 0 ||
        humidity > 100 ||
        ph < 0 ||
        ph > 14 ||
        rainfall < 0
    ) {
        result.textContent = "Please enter valid values.";
        return;
    }

    button.disabled = true;
    button.textContent = "Predicting...";

    try {
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                nitrogen,
                phosphorus,
                potassium,
                temperature,
                humidity,
                ph,
                rainfall
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Prediction request failed.");
        }

        const card = document.createElement("div");
        card.className = "result-card";

        const status = document.createElement("p");
        status.className = "success";
        status.textContent = "Prediction Complete";

        const heading = document.createElement("h3");
        heading.textContent = "Recommended Crop";

        const crop = document.createElement("h1");
        crop.textContent = data.recommended_crop;

        card.append(status, heading, crop);
        result.replaceChildren(card);

        // Refresh analytics after a prediction is recorded.
        await loadAnalytics();

    } catch (error) {
        result.textContent = error.message || "Unable to connect to the backend.";
        console.error("Prediction error:", error);
    } finally {
        button.disabled = false;
        button.textContent = "Predict Crop";
    }
}


// ======================================
// Analytics dashboard
// ======================================

function displayValue(value, digits = 2) {
    const number = Number(value);
    return Number.isFinite(number) ? number.toFixed(digits) : "—";
}

function addTextCell(row, value) {
    const cell = document.createElement("td");
    cell.textContent = value ?? "—";
    row.appendChild(cell);
    return cell;
}

function renderCropDistribution(distribution) {
    const container = document.getElementById("cropDistribution");
    container.replaceChildren();

    const entries = Object.entries(distribution || {})
        .sort((a, b) => b[1] - a[1]);

    if (entries.length === 0) {
        container.textContent = "No prediction history is available yet.";
        return;
    }

    const maxCount = Math.max(...entries.map(([, count]) => Number(count) || 0), 1);

    entries.forEach(([crop, count]) => {
        const item = document.createElement("div");
        item.className = "distribution-item";

        const heading = document.createElement("div");
        heading.className = "distribution-heading";

        const name = document.createElement("span");
        name.textContent = crop;

        const total = document.createElement("span");
        total.textContent = String(count);

        heading.append(name, total);

        const track = document.createElement("div");
        track.className = "distribution-track";

        const bar = document.createElement("div");
        bar.className = "distribution-bar";
        bar.style.width = `${Math.max(0, Math.min(100, (Number(count) / maxCount) * 100))}%`;

        track.appendChild(bar);
        item.append(heading, track);
        container.appendChild(item);
    });
}

function renderCropStatistics(statistics) {
    const tbody = document.getElementById("cropStatisticsBody");
    tbody.replaceChildren();

    if (!Array.isArray(statistics) || statistics.length === 0) {
        const row = document.createElement("tr");
        const cell = document.createElement("td");
        cell.colSpan = 8;
        cell.textContent = "No crop statistics are available.";
        row.appendChild(cell);
        tbody.appendChild(row);
        return;
    }

    statistics.forEach(crop => {
        const row = document.createElement("tr");

        addTextCell(row, crop.label);
        addTextCell(row, displayValue(crop.avg_nitrogen));
        addTextCell(row, displayValue(crop.avg_phosphorus));
        addTextCell(row, displayValue(crop.avg_potassium));
        addTextCell(row, displayValue(crop.avg_temperature));
        addTextCell(row, displayValue(crop.avg_humidity));
        addTextCell(row, displayValue(crop.avg_ph));
        addTextCell(row, displayValue(crop.avg_rainfall));

        tbody.appendChild(row);
    });
}

async function loadAnalytics() {
    const status = document.getElementById("analyticsStatus");
    const refreshButton = document.getElementById("refreshAnalyticsBtn");

    status.textContent = "Loading analytics...";
    refreshButton.disabled = true;

    try {
        const response = await fetch(`${API_BASE_URL}/analytics`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Analytics request failed.");
        }

        document.getElementById("totalPredictions").textContent =
            data.total_predictions ?? 0;

        document.getElementById("topCrop").textContent =
            data.most_recommended_crop ?? "—";

        document.getElementById("averageTemperature").textContent =
            `${displayValue(data.average_temperature)} °C`;

        document.getElementById("averageRainfall").textContent =
            `${displayValue(data.average_rainfall)} mm`;

        renderCropDistribution(data.crop_distribution);
        renderCropStatistics(data.crop_statistics);

        status.textContent = "Analytics updated successfully.";
    } catch (error) {
        status.textContent =
            `Could not load analytics: ${error.message}. Check that the Docker backend is running.`;

        console.error("Analytics error:", error);
    } finally {
        refreshButton.disabled = false;
    }
}


// ======================================
// Form and buttons
// ======================================

document.getElementById("predictionForm").addEventListener("submit", event => {
    event.preventDefault();
    predictCrop();
});

document.getElementById("clearBtn").addEventListener("click", () => {
    document.getElementById("predictionForm").reset();

    document.querySelectorAll(".form input").forEach(input => {
        input.classList.remove("error");
    });

    const result = document.getElementById("result");
    result.textContent = "Your crop recommendation will appear here.";

    document.getElementById("nitrogen").focus();
});

document.getElementById("refreshAnalyticsBtn").addEventListener("click", loadAnalytics);

document.addEventListener("DOMContentLoaded", loadAnalytics);
