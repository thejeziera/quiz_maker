document.addEventListener('DOMContentLoaded', function() {
    const quiz = JSON.parse(localStorage.getItem('examQuiz'));
    const config = JSON.parse(localStorage.getItem('examConfig'));
    let currentQuestionIndex = 0;
    let displayedQuestions = quiz.questions
        .sort(() => 0.5 - Math.random()) // Shuffle questions
        .slice(0, Number(config.numQuestions)); // Select the first 'numQuestions' questions
    let answers = new Array(displayedQuestions.length).fill(null); // Adjusted to the actual number of questions displayed

    // Timer setup
	let timer; // Declare the timer variable in an accessible scope
    const timeLimit = Number(config.timeLimit) * 60 * 1000; // Convert minutes to milliseconds
    startTimer(timeLimit);

    function displayQuestion(index) {
        const question = displayedQuestions[index];
        const container = document.getElementById('examContainer');
        container.innerHTML = `
			<div class="question">
                <p>${question.text}</p>
                ${getAnswerInputHTML(question, index)}
            </div>
            ${index > 0 ? '<button id="previousButton">Previous</button>' : ''}
            ${index < displayedQuestions.length - 1 ? '<button id="nextButton">Next</button>' : ''}
            ${index === displayedQuestions.length - 1 ? '<button id="submitButton">Submit</button>' : ''}
        `;

        // Attach event listeners to the buttons
		attachEventListeners();
        prepopulateAnswers(index);
    }
	
    function attachEventListeners() {
        const nextButton = document.getElementById('nextButton');
        if (nextButton) {
            nextButton.addEventListener('click', () => navigateQuestion(1));
        }
        
        const previousButton = document.getElementById('previousButton');
        if (previousButton) {
            previousButton.addEventListener('click', () => navigateQuestion(-1));
        }
        
        const submitButton = document.getElementById('submitButton');
        if (submitButton) {
            submitButton.addEventListener('click', submitExam);
        }
    }

    function navigateQuestion(direction) {
        // Save current answer before navigating
        saveCurrentAnswer(currentQuestionIndex);
        currentQuestionIndex += direction;
        displayQuestion(currentQuestionIndex);
    }

    function saveCurrentAnswer(index) {
        const question = displayedQuestions[index];
        if (question.type === 'text') {
            answers[index] = document.getElementById(`answer${index}`).value;
        } else {
            answers[index] = [...document.querySelectorAll(`input[name="answer${index}"]:checked`)].map(el => el.value);
        }
    }

    function submitExam() {
		if (timer) clearInterval(timer); // Stop the timer when exam is submitted
        saveCurrentAnswer(currentQuestionIndex); // Ensure the last answer is saved
        const correctAnswers = calculateCorrectAnswers();
        const score = correctAnswers / displayedQuestions.length * 100;
        const passed = score >= Number(config.passPercentage);
        displayResults(score, passed);
    }

    function startTimer(duration) {
        const timerDisplay = document.getElementById('timerDisplay');
        const endTime = Date.now() + duration;

        function updateTimer() {
            const now = Date.now();
            const distance = endTime - now;
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);

            timerDisplay.textContent = `Time Left: ${pad(minutes)}:${pad(seconds)}`;

            if (distance < 0) {
                clearInterval(timer);
                timerDisplay.textContent = "Time's up!";
                submitExam();
            }
        }

        updateTimer(); // Initial update
        timer = setInterval(updateTimer, 1000); // Assign to the outer scope variable
    }
	
	function pad(number) {
		return number < 10 ? '0' + number : number;
	}
	
	function calculateCorrectAnswers() {
		return answers.reduce((acc, answer, index) => {
			const question = displayedQuestions[index];
			if (question.type === 'text') {
				// Text answer comparison
				return acc + (answer?.toLowerCase() === question.answer.toLowerCase() ? 1 : 0);
			} else if (question.type === 'radio') {
				// For radio, directly compare the selected answer's value to the correct answer
				const correctIndex = question.answers.findIndex(a => a.correct);
				return acc + (answer == correctIndex ? 1 : 0); // Using == for comparison since answer might be string
			} else if (question.type === 'checkbox') {
				// Checkbox answer comparison
				const correct = question.answers.filter(a => a.correct).map((_, i) => String(i));
				return acc + (JSON.stringify(answer?.sort()) === JSON.stringify(correct.sort()) ? 1 : 0);
			}
		}, 0);
	}
	
	function displayResults(score, passed) {
		document.getElementById('examContainer').innerHTML = `
			<div class="summary">
				<p>Your Score: ${score.toFixed(2)}%</p>
				<p>${passed ? "Congratulations, you passed! 🍺" : "Unfortunately, you didn't pass. Try again!"}</p>
				<button onclick="window.location.href='index.html'">Back to Main</button>
			</div>
		`;
	}
	
	function prepopulateAnswers(index) {
		if (answers[index] === null) return;
		const question = displayedQuestions[index];
		if (question.type === 'text') {
			document.getElementById(`answer${index}`).value = answers[index];
		} else {
			answers[index].forEach(answerIndex => {
				document.querySelector(`input[name="answer${index}"][value="${answerIndex}"]`).checked = true;
			});
		}
	}
	
	function getAnswerInputHTML(question, index) {
		let html = '';
		if (question.type === 'radio' || question.type === 'checkbox') {
			question.answers.forEach((answer, i) => {
				html += `<label><input type="${question.type}" name="answer${index}" value="${i}">${answer.text}</label><br>`;
			});
		} else if (question.type === 'text') {
			html += `<input type="text" id="answer${index}" name="answer${index}" class="text-answer"><br>`;
		}
		return html;
	}

    displayQuestion(currentQuestionIndex);
});
