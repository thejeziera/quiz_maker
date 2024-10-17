# Quiz Manager - README

## Overview

**Quiz Manager** is a lightweight, interactive tool to help you create, learn, and assess knowledge through quizzes. This project is built using HTML, CSS, and JavaScript, and offers three key functionalities: creating quizzes, learning in a structured way, and taking exams based on the quizzes you create. Whether you want to test yourself or help others learn, this tool is easy to use, even without prior development experience.

## Features

1. **Quiz Creation** - A GUI to create quiz questions without writing JSON manually.
2. **Learn Mode** - Practice quizzes in a low-pressure environment with repetition and learning enhancements.
3. **Exam Mode** - Assess your knowledge through a timed exam format with custom question counts and pass percentages.

## Getting Started

### For Users
If you just want to use **Quiz Manager** without modifying the code, please visit the [latest release](https://github.com/thejeziera/quiz-manager/releases) and download the zip file. Extract it and open `index.html` in your browser to start using Quiz Manager.

### For Developers
To get started with **Quiz Manager**, follow these steps:

1. **Clone the Repository**
   ```sh
   git clone https://github.com/your-username/quiz-manager.git
   ```
2. **Open the Project in Your Preferred Editor** - You can use tools like WebStorm, VSCode, or even a basic text editor to explore and modify the project.
3. **Run the Project Locally** - Open `index.html` in your browser to start using Quiz Manager.

## How to Use

### 1. Main Menu

- **Create Quiz**: Create new quizzes using a simple form.
- **Learn**: Practice an existing quiz by uploading a `.json` file.
- **Exam**: Test your knowledge by taking an exam with a time limit and set pass percentage.

### 2. Creating a Quiz

- Click on **Create** to create a new quiz.
- Enter a **Quiz Title**.
- Add questions using the **Add Question** button.
- For each question, choose a **question type** (Single Choice, Multiple Choice, or Open Question).
- The interface always shows the current question only, making it easier to focus.
- Click **Finish** to generate and download the quiz as a `.json` file.

### 3. Learn Mode

- Click **Learn** from the main menu.
- Upload your quiz file in `.json` format.
- Set the **number of repetitions** and **additional repetitions on errors**.
- Learn interactively until you master all questions.

### 4. Exam Mode

- Click **Exam** from the main menu.
- Upload your quiz file.
- Set parameters like **Number of Questions**, **Time Limit**, and **Pass Percentage**.
- Click **Begin Exam** to start and navigate through the questions.

## Quiz JSON Format

To create quizzes manually or understand the generated quiz format, here is the JSON structure:

```json
{
  "title": "Sample Quiz Title",
  "questions": [
    {
      "text": "What is the capital of France?",
      "type": "radio",
      "answers": [
        { "text": "Paris", "correct": true },
        { "text": "London", "correct": false },
        { "text": "Berlin", "correct": false },
        { "text": "Madrid", "correct": false }
      ]
    },
    {
      "text": "Select all prime numbers below:",
      "type": "checkbox",
      "answers": [
        { "text": "2", "correct": true },
        { "text": "3", "correct": true },
        { "text": "4", "correct": false },
        { "text": "5", "correct": true }
      ]
    },
    {
      "text": "Describe the water cycle.",
      "type": "text",
      "answer": "Evaporation, condensation, and precipitation."
    }
  ]
}
```

- **title**: The title of the quiz.
- **questions**: An array of question objects.
    - **text**: The question text.
    - **type**: The type of question (`radio` for single choice, `checkbox` for multiple choice, `text` for open-ended questions).
    - **answers**: An array of answer objects (only for `radio` and `checkbox` types).
        - **text**: The answer text.
        - **correct**: A boolean indicating if the answer is correct.
    - **answer**: For `text` questions, the expected answer.

## Development

The project is built with simple HTML, CSS, and JavaScript, making it easy for anyone to contribute or modify.

### Contributions

Feel free to fork this repository and create pull requests for new features or bug fixes. The project is open to improvements, especially for enhancing the user interface or adding more question types.

## License

This project is licensed under the GNU GPL License. You can use, modify, and distribute it as you like.

## Acknowledgments

- **WebStorm** and **VSCode** for providing great environments for developing this project.
- All the contributors who help make Quiz Manager better.

---

Happy Learning! 🎉

