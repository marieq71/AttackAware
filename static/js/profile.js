// When the user selects a file to upload, the file input triggers a 'change' event
document.getElementById('profile-picture-upload').addEventListener('change', function(event) {
    // Call the function to preview the image
    previewImage(event);
});

// Function to preview the selected image before submitting the form
function previewImage(event) {
    var image = document.querySelector('#defaultProfilePic');  // Get the selected file from the input
    var file = event.target.files[0];  // Get the first file from the input element

    // Check if there is a file selected
    if (file) {
        var reader = new FileReader();

        reader.onload = function(e) {
            // Update the src of the defaultProfilePic with the selected image
            image.src = e.target.result;
        };

        // Read the file as a data URL (for image preview)
        reader.readAsDataURL(file);
    }
}

function showPasswordModal() {
    document.getElementById("passwordModal").style.display = "block";
  }
  
  function closePasswordModal() {
    document.getElementById("passwordModal").style.display = "none";
  }
  
  // Close the modal when the user clicks anywhere outside of it
  window.onclick = function(event) {
    const modal = document.getElementById("passwordModal");
    if (event.target === modal) {
      modal.style.display = "none";
    }
  };

  
  
