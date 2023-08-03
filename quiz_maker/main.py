import tkinter as tk
from tkinter import messagebox
import pandas as pd
import random
import pickle
import os

# Declare the global variables
df = None
progress = None
current_question = None
correct_answers = []
user_answers = None
correct_threshold = 3

root = tk.Tk()
root.withdraw()
root.title("Quiz Maker")

# Create a configuration window
config_win = tk.Toplevel(root)
config_win.title("Quiz Maker Configuration")

# Add labels and input fields for chapters and the correct threshold
chap_label = tk.Label(config_win, text='Select chapters')
chap_label.pack()

correct_threshold_label = tk.Label(config_win, text='Correct threshold')
correct_threshold_entry = tk.Entry(config_win)
correct_threshold_entry.insert(0, str(correct_threshold))
correct_threshold_label.pack()
correct_threshold_entry.pack()

# Load the data and create chapter checkbuttons
try:
    df = pd.read_csv('questions.csv')
except FileNotFoundError:
    messagebox.showerror('File not found', 'The CSV file with questions was not found.')

chap_vars = {}
if df is not None:
    chapters = df['Chapter'].unique()
    chap_vars = {chap: tk.IntVar() for chap in chapters}
    for chap, var in chap_vars.items():
        c = tk.Checkbutton(config_win, text=chap, variable=var)
        c.pack()
else:
    messagebox.showerror('Error', 'Failed to initialize the application due to missing CSV file.')

# Load the progress data or create a new one
try:
    with open('progress.pickle', 'rb') as file:
        progress = pickle.load(file)
except FileNotFoundError:
    if df is not None:
        progress = {i: {'correct': 0, 'wrong': 0} for i in range(len(df))}

# Adjust the window size
config_win.update()
config_win.geometry(f'{config_win.winfo_width() + 70}x{config_win.winfo_height() + 70}+'
                    f'{root.winfo_x()}+{root.winfo_y()}')


# Function to update the question
def update_question():
    global current_question, correct_answers, user_answers, options_buttons

    # Clear old answer options if they exist
    for button in options_buttons:
        button.destroy()

    question_var.set(df.loc[current_question, 'Question'])
    correct_answers = [int(ans) for ans in df.loc[current_question, 'Correct'].split(',')]
    user_answers = [tk.IntVar() for _ in correct_answers]
    options = df.loc[current_question, 'Options'].split(',')
    answers_options = list(zip(correct_answers, options, user_answers))
    random.shuffle(answers_options)
    correct_answers, options, user_answers = zip(*answers_options)

    options_buttons = []
    for i, option in enumerate(options):
        var = tk.StringVar(value=option)
        btn = tk.Checkbutton(root, textvariable=var, variable=user_answers[i])
        btn.grid(row=i + 2, column=0, sticky='w')
        options_buttons.append(btn)

    # Update the position of Submit and Quit buttons according to the number of answer options
    submit_button.grid(row=len(options) + 2, column=0)
    quit_button.grid(row=len(options) + 2, column=1)


# Initialize the widgets for the main window
question_var = tk.StringVar()
question_label = tk.Label(root, textvariable=question_var)
question_label.grid(row=0, column=0, sticky='w')

options_buttons = []

submit_var = tk.StringVar(value='Submit')
submit_button = tk.Button(root, textvariable=submit_var)

# Function to select the next question
def get_next_question():
    selected_chapters = [chap for chap, var in chap_vars.items() if var.get() == 1]
    possible_questions = [i for i in range(len(df)) if df.loc[i, 'Chapter'] in selected_chapters and
                          progress[i]['correct'] < correct_threshold]
    if not possible_questions:
        return None
    else:
        return random.choice(possible_questions)


# Function to save progress and quit the application
def quit_quiz():
    if messagebox.askyesno("Quit", "Do you want to save the progress?"):
        with open('progress.pickle', 'wb') as progress_file:
            pickle.dump(progress, progress_file)
    root.destroy()


# Function to start the quiz
def start_quiz():
    global current_question, correct_threshold
    correct_threshold = int(correct_threshold_entry.get())

    config_win.destroy()
    root.deiconify()
    current_question = get_next_question()
    if current_question is None:
        submit()
    else:
        update_question()


start_button = tk.Button(config_win, text='Start the quiz', command=start_quiz)
start_button.pack()

# Function to reset the progress
def reset_progress():
    global progress
    progress = {i: {'correct': 0, 'wrong': 0} for i in range(len(df))}
    if os.path.exists('progress.pickle'):
        os.remove('progress.pickle')
    messagebox.showinfo('Progress reset', 'Progress has been reset successfully.')


reset_button = tk.Button(config_win, text='Reset progress', command=reset_progress)
reset_button.pack()

# Add the submit and quit buttons to the main window
quit_button = tk.Button(root, text='Quit', command=quit_quiz)

root.update()
root.geometry(f'{root.winfo_width() + 70}x{root.winfo_height() + 70}')


# Function to submit an answer
def submit():
    global current_question, progress
    if submit_var.get() == 'Next':
        current_question = get_next_question()
        if current_question is None:
            total_questions = len([i for i in range(len(df)) if progress[i]['correct'] >= correct_threshold])
            correct_ans_stats = sum(progress[i]['correct'] for i in range(len(df)))
            wrong_answers = sum(progress[i]['wrong'] for i in range(len(df)))
            stats_win = tk.Toplevel(root)
            stats_win.title("Quiz Maker - Statistics")
            stats_win.geometry(f'{stats_win.winfo_width() + 240}x{stats_win.winfo_height() + 130}+'
                               f'{root.winfo_x()}+{root.winfo_y()}')
            stats_label = tk.Label(stats_win, text='Quiz statistics:\n'
                                                   f'Total questions learned: {total_questions}\n'
                                                   f'Answers submitted correctly: {correct_ans_stats}\n'
                                                   f'Total mistakes made: {wrong_answers}\n'
                                                   f'You have learned all the questions.')
            stats_label.pack()
            quit_button_stats = tk.Button(stats_win, text='Quit', command=quit_quiz)
            quit_button_stats.pack()
            stats_win.protocol('WM_DELETE_WINDOW', quit_quiz)
            return
        submit_var.set('Submit')
        update_question()
        return
    answers = [var.get() for var in user_answers]
    correct = all((user_ans == correct_ans for user_ans, correct_ans in zip(answers, correct_answers)))
    if correct:
        progress[current_question]['correct'] += 1
    else:
        progress[current_question]['correct'] = 0
        progress[current_question]['wrong'] += 1
    for i, option in enumerate(options_buttons):
        if answers[i] and correct_answers[i] == 1:
            option.config(bg='green')
        elif answers[i] and correct_answers[i] == 0:
            option.config(bg='red')
        elif not answers[i] and correct_answers[i] == 1:
            option.config(bg='yellow')
    submit_var.set('Next')


submit_button.config(command=submit)

root.mainloop()