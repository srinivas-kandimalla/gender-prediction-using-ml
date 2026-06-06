const nameInput = document.getElementById("nameInput");
const predictButton = document.getElementById("predictButton");
const clearButton = document.getElementById("clearButton");
const resultCard = document.getElementById("resultCard");
const resultGender = document.getElementById("resultGender");
const resultConfidence = document.getElementById("resultConfidence");
const resultStatus = document.getElementById("resultStatus");
const themeToggle = document.getElementById("themeToggle");

function setResult({ gender = "—", confidence = "—", status = "Waiting" }) {
    resultGender.textContent = gender;
    resultConfidence.textContent = `Confidence: ${confidence}`;
    resultStatus.textContent = `Status: ${status}`;
    resultCard.classList.add("visible");
    resultCard.classList.remove("hidden");
}

function resetResult() {
    setResult({ gender: "—", confidence: "—", status: "Waiting" });
}

function updateButton(isLoading) {
    if (isLoading) {
        predictButton.disabled = true;
        predictButton.innerHTML = `Predicting <span class="spinner"></span>`;
    } else {
        predictButton.disabled = false;
        predictButton.textContent = "Predict";
    }
}

async function predictName() {
    const name = nameInput.value.trim();
    if (!name) {
        nameInput.focus();
        return;
    }

    updateButton(true);
    setResult({ gender: "—", confidence: "—", status: "Predicting" });

    try {
        const response = await fetch("/api/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ name }),
        });

        if (!response.ok) {
            const payload = await response.json().catch(() => ({}));
            throw new Error(payload.error || "Prediction request failed.");
        }

        const payload = await response.json();
        const gender = payload.predicted_gender || "Unknown";
        const confidence = payload.confidence || 0;
        setResult({
            gender,
            confidence: `${(confidence * 100).toFixed(1)}%`,
            status: "Prediction Complete",
        });
    } catch (error) {
        setResult({ gender: "Error", confidence: "—", status: error.message || "Failed" });
    } finally {
        updateButton(false);
    }
}

function clearInput() {
    nameInput.value = "";
    nameInput.focus();
    resetResult();
}

function toggleTheme() {
    document.body.classList.toggle("dark");
    const isDark = document.body.classList.contains("dark");
    themeToggle.textContent = isDark ? "Light mode" : "Dark mode";
}

predictButton.addEventListener("click", predictName);
clearButton.addEventListener("click", clearInput);
nameInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        event.preventDefault();
        predictName();
    }
});
themeToggle.addEventListener("click", toggleTheme);

resetResult();
