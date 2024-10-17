document.addEventListener('DOMContentLoaded', function() {
	const quiz = JSON.parse(localStorage.getItem('quiz'));
	const config = JSON.parse(localStorage.getItem('learnConfig'));
	let questions = quiz.questions.map((question, index) => ({
		...question,
		id: index,
		attempts: 0,
		correct: 0,
		errors: 0
	})).sort(() => 0.5 - Math.random()); // Shuffle questions

	function shuffleArray(array) {
		for (let i = array.length - 1; i > 0; i--) {
			const j = Math.floor(Math.random() * (i + 1));
			[array[i], array[j]] = [array[j], array[i]]; // Swap
		}
	}

	function isQuestionLearned(question) {
		const repetitionsNeeded = Number(config.numRepetitions) + question.errors * Number(config.additionalRepsOnError);
		return question.correct >= repetitionsNeeded;
	}

	function displayNextQuestion() {
		// Filter out learned questions
		const unlearnedQuestions = questions.filter(q => !isQuestionLearned(q));

		if (unlearnedQuestions.length === 0) {
			return finishQuiz();
		}

		// Shuffle the unlearned questions to pick a random next question
		const nextQuestion = unlearnedQuestions.sort(() => 0.5 - Math.random())[0];

		renderQuestion(nextQuestion);
	}

	function renderQuestion(question) {
		const container = document.getElementById('quizContainer');
		container.innerHTML = '';

		// Shuffle answers without changing the original order in 'question.answers'
		let shuffledAnswers = [...question.answers];
		shuffleArray(shuffledAnswers);

		const questionHtml = `
            <div class="question">
                <p>${question.text}</p>
                ${getAnswerInputHTML(question, shuffledAnswers)}
                <button id="checkButton">Check</button>
            </div>
        `;
		container.innerHTML += questionHtml;

		// The 'Next' button is managed dynamically after checking an answer.
		let nextButtonHTML = `<button id="nextButton" style="display:none;">Next</button>`;
		container.innerHTML += nextButtonHTML;

		let finishButtonHTML = `<button id="finishButton">Finish</button>`;
		container.innerHTML += finishButtonHTML;

		const checkButton = document.getElementById('checkButton');
		checkButton.onclick = () => checkAnswer(question);

		const nextButton = document.getElementById('nextButton');
		if (nextButton) {
			nextButton.onclick = () => displayNextQuestion();
		}

		const finishButton = document.getElementById('finishButton');
		if (finishButton) {
			finishButton.onclick = finishQuiz;
		}
	}

	function checkAnswer(question) {
		let isCorrect = false; // Flag to determine if the answer is correct

		if (question.type === 'text') {
			const userAnswer = document.getElementById(`answer${question.id}`).value.trim();
			isCorrect = userAnswer.toLowerCase() === question.answer.toLowerCase();
			// Apply color directly as there's only one element to color
			document.getElementById(`answer${question.id}`).style.color = isCorrect ? '#4CAF50' : '#FF5722';
		} else if (question.type === 'radio') {
			const selectedOption = document.querySelector(`input[name='answer${question.id}']:checked`);
			if (selectedOption) {
				const answerIndex = parseInt(selectedOption.value);
				isCorrect = question.answers[answerIndex].correct;
				// Color all options, correct one in green and others in default color
				document.querySelectorAll(`input[name='answer${question.id}']`).forEach((input) => {
					const index = parseInt(input.value);
					input.parentNode.style.color = question.answers[index].correct ? '#4CAF50' : '#fff';
				});
			}
		} else if (question.type === 'checkbox') {
			const userAnswers = [...document.querySelectorAll(`input[name='answer${question.id}']:checked`)].map(el => parseInt(el.value));
			// Consider correct if all selected options are correct and all correct options are selected
			const correctAnswers = question.answers.flatMap((a, i) => a.correct ? [i] : []);
			isCorrect = correctAnswers.length === userAnswers.length && userAnswers.every(val => correctAnswers.includes(val));
			// Color all checkbox options
			document.querySelectorAll(`input[name='answer${question.id}']`).forEach((input) => {
				const index = parseInt(input.value);
				input.parentNode.style.color = question.answers[index].correct ? '#4CAF50' : '#fff';
			});
		}

		if (isCorrect) {
			question.correct++;
		} else {
			question.errors++;
		}

		// Adjust UI elements for the next action
		document.getElementById('checkButton').style.display = 'none';
		const nextButton = document.getElementById('nextButton');
		if (nextButton) nextButton.style.display = 'inline-block';
		const finishButton = document.getElementById('finishButton');
		if (finishButton) finishButton.style.display = 'inline-block';
	}

	function finishQuiz() {
		const learnedCount = questions.filter(isQuestionLearned).length;
		const totalQuestions = questions.length;
		const mistakes = questions.reduce((acc, q) => acc + q.errors, 0);
		const answeredQuestions = questions.filter(q => q.correct > 0 || q.errors > 0).length;
		const incorrectQuestions = questions.filter(q => q.errors > 0);

		const container = document.getElementById('quizContainer');
		let summaryHtml = `
            <div class="summary">
                <p>Questions Learned: ${learnedCount} / ${totalQuestions}</p>
                <p>Learned Percentage: ${((learnedCount / totalQuestions) * 100).toFixed(2)}%</p>
                <p>Total Mistakes: ${mistakes}</p>
        `;

		if (mistakes === 0 && answeredQuestions === totalQuestions) {
			summaryHtml += "<p>You're good to go 🍺!</p>";
		} else {
			summaryHtml += '<p>You have some questions to review. Consider saving them for focused revision.</p>';
		}

		summaryHtml += `
                <button onclick="window.location.href='index.html'">Back</button>
                ${mistakes > 0 ? '<button id="saveButton">Save</button>' : ''}
            </div>
        `;

		container.innerHTML = summaryHtml;

		if (mistakes > 0) {
			document.getElementById('saveButton').addEventListener('click', function() {
				saveIncorrectQuestions(incorrectQuestions);
			});
		}
	}

	function saveIncorrectQuestions(incorrectQuestions) {
		// Wrap incorrect questions in the required structure with a title
		const dataToSave = {
			title: "Refinement",
			questions: incorrectQuestions.map(q => ({
				text: q.text,
				type: q.type,
				answers: q.answers.map(a => ({
					text: a.text,
					correct: a.correct
				}))
			}))
		};

		const jsonString = JSON.stringify(dataToSave, null, 2);
		const blob = new Blob([jsonString], { type: 'application/json' });
		const url = URL.createObjectURL(blob);

		// Create a link and trigger download
		const link = document.createElement('a');
		link.href = url;
		link.download = 'learning_refinement.json';
		document.body.appendChild(link); // Required for Firefox
		link.click();
		document.body.removeChild(link);
		URL.revokeObjectURL(url);
	}

	function getAnswerInputHTML(question, shuffledAnswers) {
		let html = '';
		if (question.type === 'radio' || question.type === 'checkbox') {
			shuffledAnswers.forEach((answer, index) => {
				// Use the index from the original question.answers array to preserve answer identity
				const originalIndex = question.answers.findIndex(a => a.text === answer.text);
				html += `<label><input type="${question.type}" name="answer${question.id}" value="${originalIndex}"> ${answer.text}</label><br>`;
			});
		} else if (question.type === 'text') {
			html += `<input type="text" id="answer${question.id}" name="answer${question.id}"><br>`;
		}
		return html;
	}

	displayNextQuestion();
});
