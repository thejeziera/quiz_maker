document.getElementById('examConfigForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const quizFile = document.getElementById('quizFile').files[0];
    if (!quizFile) {
        alert("Please upload a quiz file.");
        return;
    }
    
    const numQuestions = document.getElementById('numQuestions').value;
    const timeLimit = document.getElementById('timeLimit').value;
    const passPercentage = document.getElementById('passPercentage').value;

    // Read and save the quiz file content
    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const quizContent = JSON.parse(e.target.result);
            // Save configuration and quiz content to local storage
            localStorage.setItem('examQuiz', JSON.stringify(quizContent));
            localStorage.setItem('examConfig', JSON.stringify({
                numQuestions,
                timeLimit,
                passPercentage
            }));
            // Navigate to the exam session page
            window.location.href = 'examSession.html'; // This will be your exam session page
        } catch (error) {
            alert("Error reading the quiz file. Please ensure it's a valid JSON file.");
        }
    };
    reader.readAsText(quizFile);
});

function goBack() {
    window.location.href = 'index.html';
}
