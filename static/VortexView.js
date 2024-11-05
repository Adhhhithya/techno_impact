function checkSizeAndOpenResultPage() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    if (file) {
        const fileSizeInMB = file.size / (1024 * 1024);
        if (fileSizeInMB > 20) {
            alert("File size exceeds 20 MB limit. Please upload a smaller file.");
            return;
        }

        window.location.href = "../templates/Resultpage.html";
    } else {
        alert("Please choose a file first.");
    }
}
