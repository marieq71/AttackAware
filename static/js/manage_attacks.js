
manage_attacks.js
// JavaScript for handling YouTube video links
document.getElementById('add-video-btn').addEventListener('click', function() {
    var videoLink = document.getElementById('video-link').value;
    if (videoLink) {
        // Create a new div for the video link
        var videoDiv = document.createElement('div');
        videoDiv.classList.add('video-item');

        // Create a span for the video link URL
        var videoUrl = document.createElement('span');
        videoUrl.textContent = videoLink;

        // Create a remove button
        var removeButton = document.createElement('button');
        removeButton.textContent = 'Remove';
        removeButton.classList.add('remove-video-btn');

        removeButton.addEventListener('click', function() {
            videoDiv.remove();
        });

        // Append the video link and remove button to the div
        videoDiv.appendChild(videoUrl);
        videoDiv.appendChild(removeButton);

        // Append the video div to the video list
        document.getElementById('video-list').appendChild(videoDiv);

        // Clear the input field after adding the video
        document.getElementById('video-link').value = '';
    }
});

// JavaScript for handling Scenario Creation and Removal
document.getElementById('scenario-type').addEventListener('change', function() {
    var scenarioType = document.getElementById('scenario-type').value;
    var correctAnswer = document.getElementById('correct-answer').value;
    var incorrectAnswer = document.getElementById('incorrect-answer').value;
    var extraNotes = document.getElementById('extra-notes').value;

    if (scenarioType && correctAnswer && incorrectAnswer) {
        // Create a new scenario item
        var scenarioDiv = document.createElement('div');
        scenarioDiv.classList.add('scenario-item');

        // Create a span for scenario type
        var scenarioDetails = document.createElement('span');
        scenarioDetails.textContent = `${scenarioType} - Correct: ${correctAnswer}, Incorrect: ${incorrectAnswer}`;

        // Create a remove button
        var removeButton = document.createElement('button');
        removeButton.textContent = 'Remove Scenario';
        removeButton.classList.add('remove-scenario-btn');

        removeButton.addEventListener('click', function() {
            scenarioDiv.remove();
        });

        // Append scenario details and remove button to the div
        scenarioDiv.appendChild(scenarioDetails);
        scenarioDiv.appendChild(removeButton);

        // Append the scenario div to the scenario list
        document.getElementById('scenario-list').appendChild(scenarioDiv);

        // Clear the form inputs after adding the scenario
        document.getElementById('scenario-type').value = '';
        document.getElementById('correct-answer').value = '';
        document.getElementById('incorrect-answer').value = '';
        document.getElementById('extra-notes').value = '';
    }
});