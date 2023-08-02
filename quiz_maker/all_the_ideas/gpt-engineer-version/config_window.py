import tkinter as tk
from tkinter import messagebox
from quiz import read_questions_from_csv, select_unique_chapters

class ConfigWindow(tk.Frame):
    def __init__(self, master, start_quiz_callback):
        super().__init__(master)
        self.master = master
        self.start_quiz_callback = start_quiz_callback
        self.selected_chapters = []

        self.questions = read_questions_from_csv("questions.csv")
        self.unique_chapters = select_unique_chapters(self.questions)

        self.create_widgets()

    def create_widgets(self):
        self.chapter_label = tk.Label(self, text="Select Chapters:")
        self.chapter_label.pack()

        self.chapter_listbox = tk.Listbox(self, selectmode=tk.MULTIPLE)
        for chapter in self.unique_chapters:
            self.chapter_listbox.insert(tk.END, chapter)
        self.chapter_listbox.pack()

        self.start_button = tk.Button(self, text="Start Quiz", command=self.start_quiz)
        self.start_button.pack()

    def start_quiz(self):
        selected_indices = self.chapter_listbox.curselection()
        if len(selected_indices) == 0:
            messagebox.showwarning("No Chapters Selected", "Please select at least one chapter.")
        else:
            self.selected_chapters = [self.unique_chapters[i] for i in selected_indices]
            self.start_quiz_callback(self.selected_chapters)
