async function predictCrop() {

    try {

        // Get values
        const nitrogen = parseFloat(document.getElementById("nitrogen").value);
        const phosphorus = parseFloat(document.getElementById("phosphorus").value);
        const potassium = parseFloat(document.getElementById("potassium").value);
        const temperature = parseFloat(document.getElementById("temperature").value);
        const humidity = parseFloat(document.getElementById("humidity").value);
        const ph = parseFloat(document.getElementById("ph").value);
        const rainfall = parseFloat(document.getElementById("rainfall").value);

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

        document.getElementById("result").innerHTML =
            `🌾 Recommended Crop:<br><h2>${data.recommended_crop}</h2>`;

    } catch (error) {

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

        // Press Enter → Move to next field
        if (e.key === "Enter") {

            e.preventDefault();

            if (index < inputs.length - 1) {
                inputs[index + 1].focus();
            } else {
                predictCrop();
            }

        }

        // Down Arrow → Next field
        if (e.key === "ArrowDown") {

            e.preventDefault();

            if (index < inputs.length - 1) {
                inputs[index + 1].focus();
            }

        }

        // Up Arrow → Previous field
        if (e.key === "ArrowUp") {

            e.preventDefault();

            if (index > 0) {
                inputs[index - 1].focus();
            }

        }

    });

});


// ======================================
// Auto Focus First Field
// ======================================

window.addEventListener("DOMContentLoaded", () => {
    document.getElementById("nitrogen").focus();
});