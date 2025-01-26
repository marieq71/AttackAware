// Function for the alert popup to create an attack

// Check if the attack_created flag is passed from the server
const attackCreated = {{ attack_created|tojson }};

// Display an alert if a new attack was successfully created
if (attackCreated) {
    const alertPopup = document.getElementById("custom-alert");

    if (alertPopup) {
        alertPopup.classList.remove("hidden"); // Show the alert popup
    } else {
        alert("Attack created successfully!"); // Fallback alert if the popup doesn't exist
    }
}

// Optional: Add additional alert or confirmation logic
// For example, confirmations before removing an attack or resetting fields
document.addEventListener("DOMContentLoaded", () => {
    // Manage dynamic alert popup visibility
    const alertPopup = document.getElementById("custom-alert");
    if (alertPopup) {
        const closeAlertBtn = document.getElementById("close-alert-btn");

        // Add click event to close the alert popup
        closeAlertBtn.addEventListener("click", () => {
            alertPopup.classList.add("hidden"); // Hide the alert popup
        });
    }

    // Handle confirmation dialog for removing an attack
    const removeAttackButtons = document.querySelectorAll(".remove-attack-btn");

    removeAttackButtons.forEach(button => {
        button.addEventListener("click", (event) => {
            const confirmRemove = confirm("Are you sure you want to remove this attack?");
            if (!confirmRemove) {
                // Prevent the form from being submitted
                event.preventDefault();
            }
        });
    });
});
