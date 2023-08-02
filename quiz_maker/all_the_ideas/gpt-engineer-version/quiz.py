import csv
import random


class Question:
    def __init__(self, chapter, question, answers, correct_answers):
        self.chapter = chapter
        self.question = question
        self.answers = answers
        self.correct_answers = correct_answers
        self.selected_answers = []


def read_questions_from_csv(filename):
    questions = []
    with open(filename, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            chapter = row[0]
            question = row[1]
            answers = row[2]
            correct_answers = [answer for answer, is_correct in zip(answers, row[-1]) if is_correct == "1"]
            questions.append(Question(chapter, question, answers, correct_answers))
    return questions


def select_unique_chapters(questions):
    return list(set(question.chapter for question in questions))


def pick_random_question(questions, selected_chapters):
    filtered_questions = [question for question in questions if question.chapter in selected_chapters]
    return random.choice(filtered_questions)


def randomize_answers(answers):
    randomized_answers = answers.copy()
    random.shuffle(randomized_answers)
    return randomized_answers


def check_answers(selected_answers, correct_answers):
    return set(selected_answers) == set(correct_answers)
