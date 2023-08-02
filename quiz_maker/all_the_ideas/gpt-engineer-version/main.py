import tkinter as tk
from config_window import ConfigWindow
from quiz_window import QuizWindow

class QuizApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Quiz Maker")
        self.current_window = None

    def start(self):
        self.show_config_window()

    def show_config_window(self):
        self.current_window = ConfigWindow(self.root, self.show_quiz_window)
        self.current_window.pack()

    def show_quiz_window(self, selected_chapters):
        self.current_window.destroy()
        self.current_window = QuizWindow(self.root, selected_chapters)
        self.current_window.pack()

if __name__ == "__main__":
    app = QuizApp()
    app.start()
    app.root.mainloop()
