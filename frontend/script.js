async function predictCrop() {

    const button = document.getElementById("predictBtn");

    // Disable button and start loading animation
    button.disabled = true;

    let dots = 0;

    button.innerHTML = "🌾 Predicting";

    const loadingAnimation = setInterval(() => {
        dots = (dots + 1) % 4;
        button.innerHTML = "🌾 Predicting" + ".".repeat(dots);
    }, 350);

    try {

        // Get values
        const nitrogen = parseFloat(document.getElementById("nitrogen").value);
        const phosphorus = parseFloat(document.getElementById("phosphorus").value);
        const potassium = parseFloat(document.getElementById("potassium").value);
        const temperature = parseFloat(document.getElementById("temperature").value);
        const humidity = parseFloat(document.getElementById("humidity").value);
        const ph = parseFloat(document.getElementById("ph").value);
        const rainfall = parseFloat(document.getElementById("rainfall").value);

        const values = [
            nitrogen,
            phosphorus,
            potassium,
            temperature,
            humidity,
            ph,
            rainfall
        ];

        const inputElements = document.querySelectorAll(".form input");

        // Remove previous error highlights
        inputElements.forEach(input => input.classList.remove("error"));

        // Empty field validation
        if (values.some(value => isNaN(value))) {

            values.forEach((value, index) => {
                if (isNaN(value)) {
                    inputElements[index].classList.add("error");
                }
            });

            throw new Error("Please fill in all fields.");

        }

        // Range validation
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

            throw new Error("Please enter valid values.");

        }

        const response = await fetch("http://127.0.0.1:5000/api/predict", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

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

        if (!response.ok) {
            throw new Error("Server returned an error.");
        }

        const data = await response.json();

        console.log(data);

        clearInterval(loadingAnimation);

        button.disabled = false;
        button.innerHTML = "🌾 Predict Crop";

        document.getElementById("result").innerHTML = `

            <div class="result-card">

                <div class="success">
                    ✅ Prediction Complete
                </div>

                <h3>Recommended Crop</h3>

                <h1>${data.recommended_crop}</h1>

            </div>

        `;

    } catch (error) {

        clearInterval(loadingAnimation);

        button.disabled = false;
        button.innerHTML = "🌾 Predict Crop";

        console.error(error);

        document.getElementById("result").innerHTML =
            `<span style="color:red;">${error.message}</span>`;

    }

}


// ======================================
// Keyboard Navigation
// ======================================

const inputs = document.querySelectorAll(".form input");

inputs.forEach((input, index) => {

    input.addEventListener("keydown", function (e) {

        if (e.key === "Enter") {

            e.preventDefault();

            if (index < inputs.length - 1) {

                inputs[index + 1].focus();
                inputs[index + 1].select();

            } else {

                predictCrop();

            }

        }

        if (e.key === "ArrowDown") {

            e.preventDefault();

            if (index < inputs.length - 1) {

                inputs[index + 1].focus();
                inputs[index + 1].select();

            }

        }

        if (e.key === "ArrowUp") {

            e.preventDefault();

            if (index > 0) {

                inputs[index - 1].focus();
                inputs[index - 1].select();

            }

        }

    });

});


// ======================================
// Auto Focus First Field
// ======================================

window.addEventListener("DOMContentLoaded", () => {

    const firstInput = document.getElementById("nitrogen");

    firstInput.focus();
    firstInput.select();

});


// ======================================
// Clear Button
// ======================================

document.getElementById("clearBtn").addEventListener("click", () => {

    document.querySelectorAll(".form input").forEach(input => {

        input.value = "";
        input.classList.remove("error");

    });

    document.getElementById("result").innerHTML =
        `<p class="result-placeholder">Your crop recommendation will appear here.</p>`;

    const firstInput = document.getElementById("nitrogen");

    firstInput.focus();
    firstInput.select();

});