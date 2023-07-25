import tkinter as tk
from tkinter import messagebox
import pandas as pd
import random
import pickle

df = None
progress = None
current_question = None
correct_answers = []  # store correct answers for each question, define globally
user_answers = None  # store user answers
correct_threshold = 3  # default value

root = tk.Tk()
root.withdraw()  # hide root window initially
root.title("Quiz Maker")  # set the window's title

config_win = tk.Toplevel(root)
config_win.title("Quiz Maker Configuration")  # set the window's title

chap_label = tk.Label(config_win, text='Select chapters')
chap_label.pack()

correct_threshold_label = tk.Label(config_win, text='Correct threshold')
correct_threshold_entry = tk.Entry(config_win)

# set default values
correct_threshold_entry.insert(0, str(correct_threshold))

correct_threshold_label.pack()
correct_threshold_entry.pack()

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

try:
    with open('progress.pickle', 'rb') as file:
        progress = pickle.load(file)
except FileNotFoundError:
    if df is not None:
        progress = {i: {'correct': 0} for i in range(len(df))}

config_win.update()  # needed for winfo_width and winfo_height to work
config_win.geometry(f'{config_win.winfo_width() + 70}x{config_win.winfo_height() + 70}+'
                    f'{root.winfo_x()}+{root.winfo_y()}')  # add extra space and position on top of root window

def update_question():
    global current_question, correct_answers, user_answers
    question_var.set(df.loc[current_question, 'Question'])
    correct_answers = [int(ans) for ans in df.loc[current_question, 'Correct'].split(',')]
    user_answers = [tk.IntVar() for _ in correct_answers]
    options = df.loc[current_question, 'Options'].split(',')
    answers_options = list(zip(correct_answers, options, user_answers))
    random.shuffle(answers_options)  # shuffle options
    correct_answers, options, user_answers = zip(*answers_options)
    for i, option in enumerate(options):
        options_vars[i].set(option)
        options_buttons[i].config(bg='SystemButtonFace', variable=user_answers[i])  # reset button color and variable
        options_buttons[i].grid(row=i + 2, column=0, sticky='w')  # re-grid the button, align to the west

question_var = tk.StringVar()
question_label = tk.Label(root, textvariable=question_var)  # create a label for the question
question_label.grid(row=0, column=0, sticky='w')  # add the label to the grid, align to the west

options_vars = [tk.StringVar() for _ in range(4)]
options_buttons = [tk.Checkbutton(root, textvariable=var) for var in options_vars]  # use Checkbutton for options

submit_var = tk.StringVar(value='Submit')
submit_button = tk.Button(root, textvariable=submit_var)  # use textvariable for submit button

def get_next_question():
    selected_chapters = [chap for chap, var in chap_vars.items() if var.get() == 1]
    possible_questions = [i for i in range(len(df)) if df.loc[i, 'Chapter'] in selected_chapters and
                          progress[i]['correct'] < correct_threshold]
    if not possible_questions:
        return None
    else:
        return random.choice(possible_questions)

def quit_quiz():
    with open('progress.pickle', 'wb') as progress_file:
        pickle.dump(progress, progress_file)
    root.destroy()

def start_quiz():
    global current_question, correct_threshold
    correct_threshold = int(correct_threshold_entry.get())
    config_win.destroy()
    root.deiconify()  # show the main/root window
    current_question = get_next_question()
    if current_question is None:
        submit()
    else:
        update_question()

start_button = tk.Button(config_win, text='Start the quiz', command=start_quiz)
start_button.pack()

def reset_progress():
    global progress
    progress = {i: {'correct': 0} for i in range(len(df))}
    with open('progress.pickle', 'wb') as progress_file:
        pickle.dump(progress, progress_file)
    messagebox.showinfo('Progress reset', 'Progress has been reset successfully.')

reset_button = tk.Button(config_win, text='Reset progress', command=reset_progress)
reset_button.pack()

quit_button = tk.Button(root, text='Quit', command=quit_quiz)
submit_button.grid(row=6, column=0)  # position submit button
quit_button.grid(row=6, column=1)  # position quit button

root.update()
root.geometry(f'{root.winfo_width() + 70}x{root.winfo_height() + 70}')  # add extra space

def submit():
    global current_question, progress
    if submit_var.get() == 'Next':
        current_question = get_next_question()
        if current_question is None:
            total_questions = len([i for i in range(len(df)) if progress[i]['correct'] >= correct_threshold])
            correct_ans_stats = sum(progress[i]['correct'] for i in range(len(df)))
            wrong_answers = total_questions * correct_threshold - correct_ans_stats
            stats_win = tk.Toplevel(root)
            stats_win.title("Quiz Maker - Statistics")  # set the window's title
            stats_win.geometry(f'{stats_win.winfo_width() + 240}x{stats_win.winfo_height() + 130}+'
                               f'{root.winfo_x()}+{root.winfo_y()}')  # add extra space and position on top of root window
            stats_label = tk.Label(stats_win, text='Quiz statistics:\n'
                                                    f'Total questions: {total_questions}\n'
                                                    f'Questions learned correctly: {correct_ans_stats}\n'
                                                    f'Total mistakes made: {wrong_answers}\n'
                                                    f'You have learned all the questions.')
            stats_label.pack()
            quit_button_stats = tk.Button(stats_win, text='Quit', command=quit_quiz)
            quit_button_stats.pack()
            stats_win.protocol('WM_DELETE_WINDOW', quit_quiz)  # override the close button of the stats window
            return
        submit_var.set('Submit')  # change button text back to Submit
        update_question()
        return
    answers = [var.get() for var in user_answers]
    correct = all((user_ans == correct_ans for user_ans, correct_ans in zip(answers, correct_answers)))
    if correct:
        progress[current_question]['correct'] += 1
    else:
        progress[current_question]['correct'] = 0
    for i, option in enumerate(options_buttons):
        if answers[i] and correct_answers[i] == 1:  # correct answer
            option.config(bg='green')
        elif answers[i] and correct_answers[i] == 0:  # incorrect answer
            option.config(bg='red')
        elif not answers[i] and correct_answers[i] == 1:  # correct answer not chosen
            option.config(bg='yellow')
    submit_var.set('Next')  # change button text to Next

submit_button.config(command=submit)  # set the command for the submit button

root.mainloop()
