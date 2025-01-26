// Function to show the popup
function showThankYouPopup() {
    // Create the popup element
    const popup = document.createElement("div");
    popup.classList.add("thank-you-popup");
    popup.innerHTML = `
        <p>Hey, thanks for getting in touch!<br>
        Our team is busy at the moment but we will get back to you ASAP.</p>
        <button onclick="closePopup()">Close</button>
    `;

    // Append it to the body
    document.body.appendChild(popup);
}

// Function to close the popup
function closePopup() {
    const popup = document.querySelector(".thank-you-popup");
    if (popup) {
        popup.remove();
    }
}

// Attach event listener to the form submission
document.querySelector(".contact-form form").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent actual form submission for now
    showThankYouPopup();
    // Optionally reset the form
    this.reset();
});
