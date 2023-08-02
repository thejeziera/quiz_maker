import tkinter as tk
from tkinter import messagebox
from quiz import pick_random_question, randomize_answers, check_answers, read_questions_from_csv


class QuizWindow(tk.Frame):
    def __init__(self, master, selected_chapters):
        super().__init__(master)
        self.master = master
        self.selected_chapters = selected_chapters
        self.questions = []
        self.current_question = None
        self.answered_correctly = False

        self.create_widgets()
        self.load_questions()

    def create_widgets(self):
        self.question_label = tk.Label(self, text="", wraplength=400)
        self.question_label.pack()

        self.answer_vars = []
        self.answer_checkboxes = []
        for _ in range(6):
            var = tk.IntVar()
            checkbox = tk.Checkbutton(self, text="", variable=var)
            checkbox.pack()
            self.answer_vars.append(var)
            self.answer_checkboxes.append(checkbox)

        self.submit_button = tk.Button(self, text="Submit", command=self.submit_answer)
        self.submit_button.pack()

    def load_questions(self):
        self.questions = read_questions_from_csv("questions.csv")
        self.next_question()

    def next_question(self):
        if len(self.questions) == 0:
            messagebox.showinfo("Quiz Completed", "You have completed all the questions.")
            self.master.destroy()
            return

        self.current_question = pick_random_question(self.questions, self.selected_chapters)
        self.questions.remove(self.current_question)
        self.answered_correctly = False

        self.question_label.config(text=self.current_question.question)

        randomized_answers = randomize_answers(self.current_question.answers)
        for i in range(len(self.answer_checkboxes)):
            if i < len(randomized_answers):
                self.answer_checkboxes[i].config(text=randomized_answers[i])
                self.answer_checkboxes[i].deselect()
                self.answer_checkboxes[i].config(state=tk.NORMAL)
            else:
                self.answer_checkboxes[i].config(text="")
                self.answer_checkboxes[i].config(state=tk.DISABLED)

        self.submit_button.config(text="Submit")

    def submit_answer(self):
        selected_answers = [self.current_question.answers[i] for i, var in enumerate(self.answer_vars) if var.get() == 1]
        if len(selected_answers) == 0:
            messagebox.showwarning("No Answers Selected", "Please select at least one answer.")
        else:
            self.answered_correctly = check_answers(selected_answers, self.current_question.correct_answers)
            self.update_answer_colors()
            self.update_button_text()

    def update_answer_colors(self):
        for i, checkbox in enumerate(self.answer_checkboxes):
            if self.answered_correctly:
                if self.current_question.answers[i] in self.current_question.correct_answers:
                    checkbox.config(fg="green")
                else:
                    checkbox.config(fg="red")
            else:
                if self.current_question.answers[i] in self.current_question.correct_answers:
                    checkbox.config(fg="green")
                elif self.current_question.answers[i] in self.current_question.selected_answers:
                    checkbox.config(fg="red")
                else:
                    checkbox.config(fg="black")

    def update_button_text(self):
        if self.answered_correctly:
            self.submit_button.config(text="Next")
        else:
            self.submit_button.config(text="Submit")
            self.current_question.selected_answers = []

        if len(self.current_question.selected_answers) == 0:
            self.submit_button.config(state=tk.DISABLED)
        else:
            self.submit_button.config(state=tk.NORMAL)
