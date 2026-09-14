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