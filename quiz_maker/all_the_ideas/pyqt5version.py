from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QCheckBox, QLineEdit,
                             QDialog, QDialogButtonBox, QFormLayout, QMessageBox)
import sys
import pandas as pd
import pickle
import os
import random


class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Quiz Maker Configuration")

        self.layout = QFormLayout(self)

        # Load the data and create chapter checkbuttons
        try:
            self.df = pd.read_csv('questions.csv')
        except FileNotFoundError:
            QMessageBox.critical(self, 'File not found', 'The CSV file with questions was not found.')
            return

        self.chapters = self.df['Chapter'].unique()
        self.chapter_vars = {chap: QCheckBox(chap) for chap in self.chapters}
        for checkbox in self.chapter_vars.values():
            self.layout.addRow(checkbox)

        self.correct_threshold_entry = QLineEdit("3")
        self.layout.addRow("Correct threshold", self.correct_threshold_entry)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addRow(self.button_box)


class QuizWindow(QMainWindow):
    def __init__(self, config_dialog, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Quiz Maker")

        self.df = config_dialog.df
        self.correct_threshold = int(config_dialog.correct_threshold_entry.text())
        self.chapter_vars = config_dialog.chapter_vars
        self.progress = self.load_progress()
        self.current_question = None
        self.correct_answers = []
        self.user_answers = []

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.layout = QVBoxLayout(self.main_widget)

        self.question_label = QLabel("Question goes here")
        self.layout.addWidget(self.question_label)

        self.option_checkboxes = [QCheckBox("Option " + str(i + 1)) for i in range(6)]
        for checkbox in self.option_checkboxes:
            self.layout.addWidget(checkbox)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit)
        self.layout.addWidget(self.submit_button)

        self.quit_button = QPushButton("Quit")
        self.quit_button.clicked.connect(self.quit)
        self.layout.addWidget(self.quit_button)

        self.update_question()

    def load_progress(self):
        try:
            with open('progress.pickle', 'rb') as file:
                progress = pickle.load(file)
        except FileNotFoundError:
            progress = {i: {'correct': 0} for i in range(len(self.df))}
        return progress

    def save_progress(self):
        with open('progress.pickle', 'wb') as file:
            pickle.dump(self.progress, file)

    def get_next_question(self):
        selected_chapters = [chap for chap, var in self.chapter_vars.items() if var.isChecked()]
        possible_questions = [i for i in range(len(self.df)) if self.df.loc[i, 'Chapter'] in selected_chapters and
                              self.progress[i]['correct'] < self.correct_threshold]
        if not possible_questions:
            return None
        else:
            return random.choice(possible_questions)

    def update_question(self):
        self.current_question = self.get_next_question()
        if self.current_question is None:
            QMessageBox.information(self, "Quiz Maker", "You have learned all the questions.")
            self.close()
        else:
            self.question_label.setText(self.df.loc[self.current_question, 'Question'])
            correct_answers = [int(ans) for ans in self.df.loc[self.current_question, 'Correct'].split(',')]
            self.correct_answers = correct_answers
            self.user_answers = [0 for _ in correct_answers]
            options = self.df.loc[self.current_question, 'Options'].split(',')
            for i, (checkbox, option) in enumerate(zip(self.option_checkboxes, options)):
                checkbox.setText(option)
                checkbox.setChecked(False)
                if i < len(options):
                    checkbox.show()
                else:
                    checkbox.hide()

    def submit(self):
        answers = [int(checkbox.isChecked()) for checkbox in self.option_checkboxes[:len(self.correct_answers)]]
        correct = all(user_ans == correct_ans for user_ans, correct_ans in zip(answers, self.correct_answers))
        if correct:
            self.progress[self.current_question]['correct'] += 1
        else:
            self.progress[self.current_question]['correct'] = 0
        self.update_question()

    def quit(self):
        reply = QMessageBox.question(self, "Quiz Maker", "Do you want to save the progress?",
                                     QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            self.save_progress()
            self.close()
        elif reply == QMessageBox.No:
            self.close()


app = QApplication(sys.argv)

config_dialog = ConfigDialog()

if config_dialog.exec_() == QDialog.Accepted:
    window = QuizWindow(config_dialog)
    window.show()
    sys.exit(app.exec_())
