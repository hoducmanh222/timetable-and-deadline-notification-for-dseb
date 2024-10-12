import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from functions import add_subject, remove_subject, add_deadline_to_subject, start_deadline_checker, load_subjects, load_deadlines
from database import initialize_db

# Initialize the database
initialize_db()

# Setup main window
window = tk.Tk()
window.geometry('800x500')
window.title('School Timetable and Deadlines')

# Days of the week
days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
active_columns = []

# Timetable Section
tt_label = ttk.Label(window, text='Timetable')
tt_label.pack()

tt_tree = ttk.Treeview(window, columns=(), show='headings')
tt_tree.pack(fill=tk.BOTH, expand=True)

# Load subjects and deadlines from the database
load_subjects(tt_tree, active_columns, days_of_week)
load_deadlines(tt_tree)

# Add subject to timetable
tt_day_label = ttk.Label(window, text='Day:')
tt_day_label.pack()
tt_day_combobox = ttk.Combobox(window, values=days_of_week)
tt_day_combobox.pack()

tt_subject_label = ttk.Label(window, text='Subject:')
tt_subject_label.pack()
tt_subject_entry = ttk.Entry(window)
tt_subject_entry.pack()

tt_time_label = ttk.Label(window, text='Time:')
tt_time_label.pack()
tt_time_entry = ttk.Entry(window)
tt_time_entry.pack()

add_tt_button = ttk.Button(window, text='Add Subject', command=lambda: add_subject(tt_tree, tt_day_combobox, tt_subject_entry, tt_time_entry, active_columns, days_of_week))
add_tt_button.pack()

remove_tt_button = ttk.Button(window, text='Remove Subject', command=lambda: remove_subject(tt_tree))
remove_tt_button.pack()

# Deadlines Section
dl_label = ttk.Label(window, text='Add Deadline to Selected Subject')
dl_label.pack()

dl_date_label = ttk.Label(window, text='Date:')
dl_date_label.pack()
dl_date_entry = DateEntry(window)
dl_date_entry.pack()

dl_entry_label = ttk.Label(window, text='Deadline:')
dl_entry_label.pack()
dl_entry = ttk.Entry(window)
dl_entry.pack()

add_dl_button = ttk.Button(window, text='Add Deadline', command=lambda: add_deadline_to_subject(tt_tree, dl_date_entry, dl_entry))
add_dl_button.pack()

# Start the deadline checker
start_deadline_checker(tt_tree)

# Start the Tkinter main loop
window.mainloop()