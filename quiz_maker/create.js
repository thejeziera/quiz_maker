document.getElementById('addQuestionBtn').addEventListener('click', addQuestion);
document.getElementById('quizForm').addEventListener('submit', finishQuiz);

let questionCount = 0;
let currentQuestion = null;

function addQuestion() {
    // Get the form data to save the current question before moving on to the next one
    if (currentQuestion) {
        saveCurrentQuestion();
    }

    questionCount++;
    const questionsContainer = document.getElementById('questionsContainer');
    questionsContainer.innerHTML = ''; // Clear previous questions view

    const questionDiv = document.createElement('div');
    questionDiv.classList.add('question');
    questionDiv.innerHTML = `
        <div class="input-group">
            <label>Question ${questionCount}:</label>
            <input type="text" id="questionText" name="question${questionCount}" required>
        </div>
        <div class="input-group">
            <label>Type:</label>
            <select id="questionType" name="type${questionCount}" onchange="changeQuestionType(event, ${questionCount})">
                <option value="radio">Single Choice</option>
                <option value="checkbox">Multiple Choice</option>
                <option value="text">Open Question</option>
            </select>
        </div>
        <div class="answers" id="answers${questionCount}">
            <!-- Answers will be added here based on question type -->
        </div>
    `;
    questionsContainer.appendChild(questionDiv);

    currentQuestion = { id: questionCount, element: questionDiv }; // Track current question

    addAnswers('radio', questionCount); // Default to radio
}

function changeQuestionType(event, questionId) {
    const type = event.target.value;
    addAnswers(type, questionId);
}

function addAnswers(type, questionId) {
    const answersDiv = document.getElementById(`answers${questionId}`);
    answersDiv.innerHTML = ''; // Clear previous answers

    if (type === 'text') {
        answersDiv.innerHTML = '<input type="text" id="answerText" name="answer' + questionId + '" required>';
    } else {
        const inputType = type === 'radio' ? 'radio' : 'checkbox';
        const mandatory = type === 'radio' ? ' required' : '';
        for (let i = 1; i <= 4; i++) {
            answersDiv.innerHTML += `
                <div class="input-group">
                    <input type="${inputType}" name="correct${questionId}" value="${i}"${mandatory}>
                    <input type="text" id="option${questionId}_${i}" name="option${questionId}_${i}"${mandatory}>
                </div>
            `;
        }
    }
}

function saveCurrentQuestion() {
    const formData = new FormData(document.getElementById('quizForm'));
    const questionId = currentQuestion.id;
    const question = {
        text: formData.get(`question${questionId}`),
        type: formData.get(`type${questionId}`),
        answers: []
    };

    if (question.type === 'text') {
        question.answer = formData.get(`answer${questionId}`);
    } else {
        for (let j = 1; j <= 4; j++) {
            question.answers.push({
                text: formData.get(`option${questionId}_${j}`),
                correct: formData.getAll(`correct${questionId}`).includes(String(j))
            });
        }
    }
    quizData.questions.push(question);
}

let quizData = { title: '', questions: [] };

function finishQuiz(event) {
    event.preventDefault();

    if (currentQuestion) {
        saveCurrentQuestion();
    }

    quizData.title = document.getElementById('quizTitle').value;

    downloadQuiz(quizData);
    alert("Please place the generated quiz JSON file inside the /quiz/ directory.");
    window.location.href = 'index.html'; // Redirect to main page
}

function downloadQuiz(quizData) {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(quizData));
    const downloadAnchorNode = document.createElement('a');
    downloadAnchorNode.setAttribute("href", dataStr);
    downloadAnchorNode.setAttribute("download", quizData.title + ".json");
    document.body.appendChild(downloadAnchorNode); // Required for Firefox
    downloadAnchorNode.click();
    downloadAnchorNode.remove();
}
