document.getElementById("uploadForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    const contentImageFile = document.getElementById("contentImage").files[0];
    const styleImageFile = document.getElementById("styleImage").files[0];

    if (!contentImageFile || !styleImageFile) {
        alert("Please upload both a content image and a style image.");
        return;
    }

    const formData = new FormData();
    formData.append("content_image", contentImageFile);
    formData.append("style_image", styleImageFile);

    // Show loading message
    const outputSection = document.getElementById("outputSection");
    outputSection.classList.remove("hidden");
    outputSection.innerHTML = "<p>🔄 Transforming image... Please wait.</p>";

    try {
        const response = await fetch("http://localhost:5000/style-transfer", {
            method: "POST",
            body: formData,
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);

            // Update the output section with the transformed image
            const outputImage = document.createElement("img");
            outputImage.id = "outputImage";
            outputImage.src = url;
            outputImage.alt = "Transformed Image";
            outputImage.style.maxWidth = "100%";
            outputImage.style.marginTop = "20px";

            const downloadLink = document.createElement("a");
            downloadLink.id = "downloadLink";
            downloadLink.href = url;
            downloadLink.download = "stylized_image.png";
            downloadLink.textContent = "⬇️ Download Transformed Image";
            downloadLink.style.display = "block";
            downloadLink.style.marginTop = "10px";

            outputSection.innerHTML = ""; // Clear loading message
            outputSection.appendChild(outputImage);
            outputSection.appendChild(downloadLink);
        } else {
            const error = await response.json();
            outputSection.innerHTML = `<p>❌ Error: ${error.error || "Could not process the images."}</p>`;
        }
    } catch (error) {
        console.error("Error:", error);
        outputSection.innerHTML = "<p>❌ Something went wrong. Please try again later.</p>";
    }
});
