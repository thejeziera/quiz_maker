function convertQuestions() {
    const inputText = document.getElementById('inputText').value;

    // Replace line breaks with a space unless the next line starts with a question number or an answer option
    const normalizedInput = inputText.replace(/\n(?!(\d+\.\s|\[\s*\]|\[\s*x\s*\]))/g, ' ');

    // Split questions assuming each starts with a number and a dot
    const questionBlocks = normalizedInput.split(/\n(?=\d+\.\s)/);
    const questions = questionBlocks.map(block => {
        const lines = block.split('\n');
        const questionText = lines[0].replace(/^\d+\.\s*/, '').trim();
        const answers = lines.slice(1).map(line => {
            const isCorrect = line.startsWith('[x]');
            const text = line.replace(/^\[\s*x?\s*\]\s*/, '');
            return { text, correct: isCorrect };
        });

        const type = answers.filter(a => a.correct).length > 1 ? 'checkbox' : 'radio';
        return { text: questionText, type, answers };
    });

    document.getElementById('outputJson').value = JSON.stringify({ questions }, null, 2);
}
