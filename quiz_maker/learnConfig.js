document.getElementById('learnConfigForm').addEventListener('submit', startLearningSession);

function startLearningSession(event) {
    event.preventDefault();
    const quizFile = document.getElementById('quizFile').files[0];
    if (!quizFile) {
        alert("Please upload a quiz file.");
        return;
    }

    const numRepetitions = document.getElementById('numRepetitions').value;
    const additionalRepsOnError = document.getElementById('additionalRepsOnError').value;

    // Read the quiz file
    const reader = new FileReader();
    reader.onload = function(e) {
        const quizContent = e.target.result;
        // Assuming the quiz file is in correct JSON format
        try {
            const quiz = JSON.parse(quizContent);
            // Store the quiz and configuration in local storage
            localStorage.setItem('quiz', JSON.stringify(quiz));
            localStorage.setItem('learnConfig', JSON.stringify({
                numRepetitions,
                additionalRepsOnError
            }));
            // Navigate to the learning session page
            window.location.href = 'learnSession.html'; // This will be your learning session page
        } catch (error) {
            alert("Error reading the quiz file. Please ensure it's a valid JSON file.");
        }
    };
    reader.readAsText(quizFile);
}

function goBack() {
    window.location.href = 'index.html';
}
