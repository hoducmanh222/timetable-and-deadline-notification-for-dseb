from tkinter import END, messagebox
from datetime import datetime, timedelta
import threading
import time
import sqlite3  # Import sqlite3 module
from database import add_subject_to_db, get_subjects_from_db, add_deadline_to_db, get_deadlines_from_db, get_subject_id, get_subject_text

# Function to add a subject to the timetable
def add_subject(tt_tree, tt_day_combobox, tt_subject_entry, tt_time_entry, active_columns, days_of_week):
    day = tt_day_combobox.get()
    subject = tt_subject_entry.get()
    time = tt_time_entry.get()
    if day and subject and time:
        add_subject_to_db(day, subject, time)
        if day not in active_columns:
            active_columns.append(day)
            tt_tree['columns'] = active_columns
            for col in active_columns:
                tt_tree.heading(col, text=col)
        values = [''] * len(active_columns)
        values[active_columns.index(day)] = f"{subject} at {time} (0 deadlines)"
        tt_tree.insert('', 'end', values=values, iid=f"{day}_{subject}_{time}")
        tt_day_combobox.set('')
        tt_subject_entry.delete(0, END)
        tt_time_entry.delete(0, END)

# Function to remove a subject and its deadlines from the timetable
def remove_subject(tt_tree):
    selected_item = tt_tree.selection()
    if selected_item:
        for sub_item in tt_tree.get_children(selected_item):
            tt_tree.delete(sub_item)
        tt_tree.delete(selected_item)

# Function to add a deadline to a selected subject
def add_deadline_to_subject(tt_tree, dl_date_entry, dl_entry):
    selected_item = tt_tree.selection()
    if selected_item:
        subject_info = tt_tree.item(selected_item, 'values')[0]
        subject_name = subject_info.split(' at ')[0]  # Extract subject name
        date = dl_date_entry.get_date().strftime('%Y-%m-%d')  # Ensure date is in correct format
        deadline = dl_entry.get()
        if date and deadline:
            subject_id = get_subject_id(subject_name)
            if subject_id is not None:
                add_deadline_to_db(subject_id, date, deadline)
                deadline_text = f"Deadline: {deadline} on {date}"
                tt_tree.insert(selected_item, 'end', values=(deadline_text,), iid=f"{subject_id}_{deadline}_{date}")
                update_subject_deadline_count(tt_tree, selected_item)
                dl_date_entry.set_date('')
                dl_entry.delete(0, END)
            else:
                messagebox.showerror("Error", "Subject ID not found.")

# Function to update the deadline count for a subject
def update_subject_deadline_count(tt_tree, subject_item):
    deadlines = tt_tree.get_children(subject_item)
    deadline_count = len(deadlines)
    subject_info = tt_tree.item(subject_item, 'values')[0]
    subject_name, time_info = subject_info.split(' at ')
    new_subject_info = f"{subject_name} at {time_info} ({deadline_count} deadlines)"
    tt_tree.item(subject_item, values=(new_subject_info,))
    check_deadline_dates(tt_tree, subject_item, deadlines)

# Function to check if any deadline is within 3 days and update the color
def check_deadline_dates(tt_tree, subject_item, deadlines):
    current_date = datetime.now().date()
    for deadline_item in deadlines:
        deadline_info = tt_tree.item(deadline_item, 'values')[0]
        deadline_date_str = deadline_info.split(' on ')[1]
        try:
            deadline_date = datetime.strptime(deadline_date_str, '%Y-%m-%d').date()
        except ValueError:
            deadline_date = datetime.strptime(deadline_date_str, '%m/%d/%y').date()
        if (deadline_date - current_date).days <= 3:
            tt_tree.tag_configure('red', foreground='red')
            tt_tree.item(subject_item, tags=('red',))
            return
    tt_tree.item(subject_item, tags=())

# Function to check deadlines and trigger notifications
def check_deadlines(tt_tree):
    while True:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        for item in tt_tree.get_children():
            for sub_item in tt_tree.get_children(item):
                deadline_text = tt_tree.item(sub_item, 'values')[0]
                if current_time in deadline_text:
                    messagebox.showinfo("Deadline Notification", f"Deadline reached: {deadline_text}")
                    # Schedule removal of the deadline after 1 hour
                    threading.Timer(3600, lambda: tt_tree.delete(sub_item)).start()
        time.sleep(60)  # Check every minute

# Start the deadline checker in a separate thread
def start_deadline_checker(tt_tree):
    threading.Thread(target=check_deadlines, args=(tt_tree,), daemon=True).start()

# Function to load subjects from the database into the timetable
def load_subjects(tt_tree, active_columns, days_of_week):
    subjects = get_subjects_from_db()
    for subject in subjects:
        day, subject_text, time = subject[1], subject[2], subject[3]
        if day not in active_columns:
            active_columns.append(day)
            tt_tree['columns'] = active_columns
            for col in active_columns:
                tt_tree.heading(col, text=col)
        values = [''] * len(active_columns)
        values[active_columns.index(day)] = f"{subject_text} at {time} (0 deadlines)"
        tt_tree.insert('', 'end', values=values, iid=f"{day}_{subject_text}_{time}")

# Function to load deadlines from the database into the timetable
def load_deadlines(tt_tree):
    deadlines = get_deadlines_from_db()
    for deadline in deadlines:
        subject_id, date, deadline_text = deadline[1], deadline[2], deadline[3]
        subject_text = get_subject_text(subject_id)
        for item in tt_tree.get_children():
            if subject_text in tt_tree.item(item, 'values')[0]:
                tt_tree.insert(item, 'end', values=(f"Deadline: {deadline_text} on {date}",), iid=f"{subject_id}_{deadline_text}_{date}")
                update_subject_deadline_count(tt_tree, item)