import tkinter as tk
import pandas as pd
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from tkinter import ttk, messagebox
import os

root = tk.Tk()
root.title("GradeBook")
root.state('zoomed')
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

details = []
main_frame = tk.Frame(root)
main_frame.grid(row=0, column=0, sticky='news')

tree_frame2 = tk.Frame(root)
tree_frame2.grid(row=0, column=0, sticky='news')


# raises the frame on screen
def raise_frame(frame):
    frame.tkraise()


# toggle state of signup/login button from disable to normal or vice-versa.
def toggle_state(*_):
    if name_entry1.var.get() and passwd_entry1.var.get() and class_entry1.var.get():
        login_button1['state'] = 'normal'
    else:
        login_button1['state'] = 'disabled'

    if name_entry2.var.get() and passwd_entry2.var.get() and class_entry2.var.get():
        signup_button1['state'] = 'normal'
    else:
        signup_button1['state'] = 'disabled'


# to find location of a given value
def getLocation(df, value):
    listOfPos = []
    # will create a dataframe with boolean values and True for those locations only where this value exists.
    result = df.isin([value])
    # will create a series with only those columns which have True.
    ser = result.any()
    columnNames = list(ser[ser == True].index)

    for col in columnNames:
        rows = list(result[col][result[col] == True].index)

        for row in rows:
            listOfPos.append((row, col))

    return listOfPos


def change_password():
    currentPassword = change_passwd_entry1.get()
    newPassword1 = change_passwd_entry2.get()
    newPassword2 = change_passwd_entry3.get()

    if currentPassword == details[2] and newPassword1 == newPassword2:
        user_df.at[getLocation(user_df, details[2])[0][0], 'password'] = newPassword1
        user_df.to_csv('E:/IP Project Assets/user.csv', index=False)
        messagebox.showinfo('GradeBook', 'Your password has been changed successfully!')
        change_passwd_entry1.delete(0, 'end')
        change_passwd_entry2.delete(0, 'end')
        change_passwd_entry3.delete(0, 'end')

    elif currentPassword != details[2] and newPassword1 == newPassword2:
        messagebox.showerror('GradeBook', 'Current Password is incorrect.')

    elif currentPassword == details[2] and newPassword1 != newPassword2:
        messagebox.showerror('GradeBook', 'The new passwords you have entered do not match.')

    else:
        messagebox.showerror('GradeBook', 'Current Password is incorrect. Also, the new passwords you have entered do '
                                          'not match.')


def signup():
    # checking if the class entered exists or not
    # os.listdir('E:/IP Project Assets') will create a list of all the files and folders existing at the given path.
    if class_entry2.get() not in os.listdir('E:/IP Project Assets'):
        os.mkdir('E:/IP Project Assets/' + class_entry2.get())  # making a new directory/folder.
        messagebox.showinfo('GradeBook', 'Signup Successful!')
        user_df.loc[len(user_df), :] = [name_entry2.get(), class_entry2.get(), passwd_entry2.get()]
        user_df.to_csv('E:/IP Project Assets/user.csv', index=False)
        name_entry2.delete(0, 'end')
        class_entry2.delete(0, 'end')
        passwd_entry2.delete(0, 'end')

    else:
        messagebox.showerror('GradeBook', 'Account for {} already exists.'.format(class_entry2.get()))
        for entry in [name_entry2, class_entry2, passwd_entry2]:
            entry.delete(0, 'end')


def create_file():
    global files_df
    global path
    file_name = create_file_entry.get()
    path = "E:/IP Project Assets/" + details[1]

    if file_name not in os.listdir(path):
        df = pd.DataFrame(columns=['Name', 'RollNo', 'Maths', 'Physics', 'Chemistry', 'IP', 'English'])
        df.to_csv("E:/IP Project Assets/" + details[1] + '/' + file_name + '.csv', index=False)
        files = os.listdir(path)
        messagebox.showinfo('GradeBook', 'A new file has been created!')
        create_file_entry.delete(0, 'end')

    else:
        messagebox.showerror('GradeBook', 'File already exists.')

    for record in my_tree1.get_children():
        my_tree1.delete(record)

    files_df = pd.DataFrame(files, columns=['File Name'])
    df_col = list(files_df.columns)
    my_tree1["columns"] = df_col
    my_tree1["show"] = "headings"

    for x in range(len(df_col)):
        my_tree1.column(x, width=400, minwidth=400)
        my_tree1.heading(x, text=df_col[x])

    my_tree1.tag_configure("oddrow", background="white")
    my_tree1.tag_configure("evenrow", background="light blue")

    count = 0
    for file in files:
        if count % 2 == 0:
            my_tree1.insert(parent="", index="end", iid=count, values=(file,), tags=("evenrow",))
        else:
            my_tree1.insert(parent="", index="end", iid=count, values=(file,), tags=("oddrow",))
        count += 1


def deleteFile():
    if my_tree1.focus():
        global files_df
        global path
        os.remove(path + '/' + files_df.at[int(my_tree1.focus()), 'File Name'])
        files = os.listdir(path)

        for record in my_tree1.get_children():
            my_tree1.delete(record)
        files_df = pd.DataFrame(files, columns=['File Name'])
        df_col = list(files_df.columns)
        my_tree1["columns"] = df_col
        my_tree1["show"] = "headings"

        for x in range(len(df_col)):
            my_tree1.column(x, width=400, minwidth=400)
            my_tree1.heading(x, text=df_col[x])

        my_tree1.tag_configure("oddrow", background="white")
        my_tree1.tag_configure("evenrow", background="light blue")

        count = 0
        for file in files:
            if count % 2 == 0:
                my_tree1.insert(parent="", index="end", iid=count, values=(file,), tags=("evenrow",))
            else:
                my_tree1.insert(parent="", index="end", iid=count, values=(file,), tags=("oddrow",))
            count += 1

    else:
        messagebox.showerror('GradeBook', 'No file selected.')


# toggles password from '*' format to normal or vice-versa.
def toggle_password(passwd_entry, toggle_passwd_button):
    if passwd_entry['show'] == '':
        passwd_entry['show'] = '*'
        toggle_passwd_button.config(image=show_password_img)

    else:
        toggle_passwd_button.config(image=hide_password_img)
        passwd_entry['show'] = ''


path = ''
files_df = pd.DataFrame()

tree_frame3 = tk.Frame(tree_frame2)
tree_frame3.pack()

my_tree = ttk.Treeview(tree_frame3, selectmode="extended")


def login():
    global details
    global path
    global files_df
    details = [name_entry1.get(), class_entry1.get(), passwd_entry1.get()]

    if details in user_df.to_numpy().tolist():
        messagebox.showinfo('GradeBook', 'Login Successful!')
        raise_frame(table_frame)
        name_entry1.delete(0, 'end')
        passwd_entry1.delete(0, 'end')
        class_entry1.delete(0, 'end')
        path = "E:/IP Project Assets/" + details[1]
        files = os.listdir(path)
        files_df = pd.DataFrame(files, columns=['File Name'])
        teacher_name2.config(text=details[0])
        teacher_class2.config(text=details[1])

        for record in my_tree1.get_children():
            my_tree1.delete(record)
        df_col = list(files_df.columns)
        my_tree1["columns"] = df_col
        my_tree1["show"] = "headings"

        for x in range(len(df_col)):
            my_tree1.column(x, width=400, minwidth=400)
            my_tree1.heading(x, text=df_col[x])

        my_tree1.tag_configure("oddrow", background="white")
        my_tree1.tag_configure("evenrow", background="light blue")

        count = 0
        for file_name in files:
            if count % 2 == 0:
                my_tree1.insert(parent="", index="end", iid=count, values=(file_name,), tags=("evenrow",))
            else:
                my_tree1.insert(parent="", index="end", iid=count, values=(file_name,), tags=("oddrow",))
            count += 1

    else:
        for entry in [name_entry1, passwd_entry1, class_entry1]:
            entry.delete(0, 'end')
        raise_frame(login_frame)
        messagebox.showerror('GradeBook', 'Login unsuccessful!\nInvalid Details entered.')


def openFile():
    if my_tree1.focus():
        global my_tree
        global data
        raise_frame(tree_frame2)
        data = pd.read_csv(path + '/' + files_df.at[int(my_tree1.focus()), 'File Name'], index_col=None)
        data['Total'] = data.loc[:, 'Maths':'English'].sum(axis=1)
        data['%'] = [round(x / 250 * 100, 2) for x in data.loc[:, 'Maths':'English'].sum(axis=1)]
        grade = []

        for marks in data['Total']:
            if marks >= 0.9 * 250:
                grade.append('A1')
            elif 0.9 * 250 > marks >= 0.75 * 250:
                grade.append('A2')
            elif 0.75 * 250 > marks >= 0.60 * 250:
                grade.append('B1')
            elif 0.60 * 250 > marks >= 0.45 * 250:
                grade.append('B2')
            elif 0.45 * 250 > marks >= 0.30 * 250:
                grade.append('C')
            elif 0.30 * 250 > marks:
                grade.append('D')

        data['Grade'] = grade

    else:
        messagebox.showerror('GradeBook', 'No file selected.')

    # selecting a record
    def select_record(event):
        entries = [name_entry, roll_no_entry, maths_entry, physics_entry, chemistry_entry, ip_entry, english_entry]
        for entry in entries:
            entry.delete(0, 'end')

        try:
            selected = my_tree.focus()
            val = my_tree.item(selected, 'values')[0:7]
            for i in range(len(entries)):
                entries[i].insert(0, val[i])

        except IndexError:
            pass

    # shows dataframe in treeview
    def show_treeview(df):
        global tree_scroll_y
        global tree_scroll_x
        global my_tree

        tree_scroll_y = tk.Scrollbar(tree_frame3)
        tree_scroll_y.pack(side="right", fill="y", pady=50)
        tree_scroll_x = tk.Scrollbar(tree_frame3, orient='horizontal')
        tree_scroll_x.pack(side='bottom', fill='x')

        my_tree = ttk.Treeview(tree_frame3, yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set,
                               selectmode="extended")
        my_tree.pack(pady=50)
        tree_scroll_y.config(command=my_tree.yview)
        tree_scroll_x.config(command=my_tree.xview)

        for record in my_tree.get_children():
            my_tree.delete(record)
        df_col = list(df.columns)

        my_tree["columns"] = df_col
        my_tree["show"] = "headings"

        for x in range(len(df_col)):
            my_tree.column(x, width=130, minwidth=130, anchor='center')
            my_tree.heading(x, text=df_col[x])

        my_tree.tag_configure("oddrow", background="white")
        my_tree.tag_configure("evenrow", background="light blue")

        count = 0
        df_rows = df.to_numpy().tolist()

        for row in df_rows:
            if count % 2 == 0:
                my_tree.insert(parent="", index="end", iid=count, values=row, tags=("evenrow",))
            else:
                my_tree.insert(parent="", index="end", iid=count, values=row, tags=("oddrow",))
            count += 1
        # will bind the event of releasing left click of mouse to selecting record.
        my_tree.bind("<ButtonRelease-1>", select_record)

    show_treeview(data)

    # clears all entry boxes
    def clear():
        for entry in [name_entry, roll_no_entry, maths_entry, physics_entry, chemistry_entry, ip_entry, english_entry]:
            entry.delete(0, 'end')

    # Removes selected records from dataframe
    def remove_selected():
        global data
        select = my_tree.selection()

        if len(select) != 0:
            data = data.drop([int(x) for x in select])
            data.index = range(len(data))
            my_tree.pack_forget()
            tree_scroll_x.pack_forget()
            tree_scroll_y.pack_forget()
            show_treeview(data)
            data.to_csv(path + '/' + files_df.at[int(my_tree1.focus()), 'File Name'], index=False)

        else:
            messagebox.showerror('GradeBook', 'No records selected.')

    # Remove all records from dataframe
    def remove_all():
        global data
        data = data[0:0]
        data.to_csv(path + '/' + files_df.at[int(my_tree1.focus()), 'File Name'], index=False)

        my_tree.pack_forget()
        tree_scroll_x.pack_forget()
        tree_scroll_y.pack_forget()
        show_treeview(data)

    # Update an existing record.
    def update():
        try:
            selected = my_tree.focus()

            if selected != '':
                rollno = data.at[int(selected), 'RollNo']
                new = [name_entry, roll_no_entry, maths_entry, physics_entry, chemistry_entry, ip_entry, english_entry]
                new_rollno = int(new[1].get())
                marks = [int(entry.get()) for entry in new[2:]]
                total = sum(marks)

                if True not in [x > 50 for x in marks]:
                    gr = ''

                    if total >= 0.90 * 250:
                        gr = 'A1'
                    elif 0.9 * 250 > total >= 0.75 * 250:
                        gr = 'A2'
                    elif 0.75 * 250 > total >= 0.60 * 250:
                        gr = 'B1'
                    elif 0.60 * 250 > total >= 0.45 * 250:
                        gr = 'B2'
                    elif 0.45 * 250 > total >= 0.30 * 250:
                        gr = 'C'
                    elif 0.30 * 250 > total:
                        gr = 'D'

                    if new_rollno == rollno or (new_rollno != rollno and new_rollno not in data['RollNo'].to_list()):
                        val = [entry.get() for entry in new[:1]] + [int(entry.get()) for entry in new[1:]] + \
                              [total, round(total / 250 * 100, 2), gr]
                        my_tree.item(selected, text='', values=tuple(val))
                        data.loc[int(selected), :'English'] = [entry.get() for entry in new[:1]] + \
                                                              [int(entry.get()) for entry in new[1:]]
                        data.to_csv(path + '/' + files_df.at[int(my_tree1.focus()), 'File Name'], index=False)

                    elif new_rollno != rollno and new_rollno in data['RollNo'].to_list():
                        messagebox.showerror('GradeBook', 'Roll no already exists. Please enter a different roll no.')

                else:
                    messagebox.showerror('GradeBook', 'Some of the marks entered are >50. Please enter marks <=50.')

            else:
                messagebox.showerror('GradeBook', 'Please select a record first.')

        except ValueError:
            messagebox.showerror('GradeBook', 'Please enter valid details.')

    # Adding a new record to the dataframe
    def add_record():
        global data

        try:
            new = [name_entry, roll_no_entry, maths_entry, physics_entry, chemistry_entry, ip_entry, english_entry]
            marks = [int(entry.get()) for entry in new[2:]]

            if True not in [x > 50 for x in marks] and int(new[1].get()) not in data['RollNo'].to_list():
                total = sum(marks)
                gr = ''

                if total >= 0.90 * 250:
                    gr = 'A1'
                elif 0.9 * 250 > total >= 0.75 * 250:
                    gr = 'A2'
                elif 0.75 * 250 > total >= 0.60 * 250:
                    gr = 'B1'
                elif 0.60 * 250 > total >= 0.45 * 250:
                    gr = 'B2'
                elif 0.45 * 250 > total >= 0.30 * 250:
                    gr = 'C'
                elif 0.30 * 250 > total:
                    gr = 'D'

                val = [entry.get() for entry in new[:1]] + [int(entry.get()) for entry in new[1:]] + \
                      [total, round(total / 250 * 100, 2), gr]
                ser = pd.Series(val, index=list(data.columns))
                data = data.append(ser, ignore_index=True)
                data.to_csv(path + '/' + files_df.at[int(my_tree1.focus()), 'File Name'], index=False)
                my_tree.pack_forget()
                tree_scroll_x.pack_forget()
                tree_scroll_y.pack_forget()
                show_treeview(data)

            elif True not in [x > 50 for x in marks] and int(new[1].get()) in data['RollNo'].to_list():
                messagebox.showerror('GradeBook', 'Roll no already exists. Please enter a different roll no.')

            else:
                messagebox.showerror('GradeBook', 'Some of the marks entered are >50. Please enter marks <=50.')

        except ValueError:
            messagebox.showerror('GradeBook', 'Please enter valid details.')

    # for sorting dataframe by a particular column.
    def sort():
        global data
        column = clicked1.get()
        asc = True if clicked3.get() == 'Ascending' else False
        data = data.sort_values(by=column, ascending=asc)
        data.index = range(0, len(data))
        my_tree.pack_forget()
        tree_scroll_x.pack_forget()
        tree_scroll_y.pack_forget()
        show_treeview(data)

    # decrement index value of a particular record by 1.
    def move_up():
        try:
            selected = int(my_tree.focus())

            if selected != 0:
                s = data.loc[selected - 1, :]
                data.loc[selected - 1, :] = data.loc[selected, :]
                data.loc[selected, :] = s
                data.to_csv(path + '/' + files_df.at[int(my_tree1.focus()), 'File Name'], index=False)
                my_tree.pack_forget()
                tree_scroll_x.pack_forget()
                tree_scroll_y.pack_forget()
                show_treeview(data)

            else:
                pass

        except ValueError:
            messagebox.showerror('GradeBook', 'Please select a record first.')

    # increment index value of a particular record by 1.
    def move_down():
        try:
            selected = int(my_tree.focus())

            if selected != len(data) - 1:
                s = data.loc[selected + 1, :]
                data.loc[selected + 1, :] = data.loc[selected, :]
                data.loc[selected, :] = s
                data.to_csv(path + '/' + files_df.at[int(my_tree1.focus()), 'File Name'], index=False)
                my_tree.pack_forget()
                tree_scroll_x.pack_forget()
                tree_scroll_y.pack_forget()
                show_treeview(data)

            else:
                pass

        except ValueError:
            messagebox.showerror('GradeBook', 'Please select a record first.')

    # Plots student report/class report or subject-wise report.
    def plot_graph():
        global data
        selected = clicked2.get()

        if selected == 'Subject-wise':

            if clicked4.get() != 'Choose subject':
                subject = clicked4.get()
                data1 = data.sort_values(by='RollNo', ascending=True)
                data1.plot(x='RollNo', y=subject, legend=False)
                plt.xticks(data1['RollNo'].to_list())
                plt.ylabel(subject + ' marks')
                plt.show()

            else:
                messagebox.showerror('GradeBook', 'Please choose a subject first.')

        elif selected == 'Student report':
            student = my_tree.focus()

            if student != '':
                student_marks = data.loc[int(student), 'Maths':'English'].to_list()
                plt.bar(data.columns[2:7].to_list(), student_marks)
                plt.ylabel('Marks')
                plt.xlabel('Subjects')
                plt.title(data.at[int(student), 'Name'])
                plt.show()

            else:
                messagebox.showerror('GradeBook', 'Please select a record first.')

        elif selected == 'Class report':

            if clicked4.get() != 'Choose subject':
                subject = clicked4.get()

                if subject != 'Total':
                    plt.figure()
                    plt.hist(data.loc[:, subject], bins=10, range=(0, 50))
                    plt.xticks(range(0, 55, 5))
                    plt.xlabel('Marks in '+subject)
                    plt.ylabel('Number of Students')
                    plt.show()

                else:
                    plt.figure(figsize=(13, 6))
                    plt.hist(data.loc[:, subject], bins=25, range=(0, 250))
                    plt.xticks(range(0, 260, 10))
                    plt.xlabel('Overall Marks')
                    plt.ylabel('Number of Students')
                    plt.show()

            else:
                messagebox.showerror('GradeBook', 'Please select a subject first.')

    # search for a particular record
    def search(e):
        key = e.char
        sub = (search_by_name_entry.get() + key).strip()

        if (sub != '') and (key != '') and ((65 <= ord(key) < 90) or (97 <= ord(key) <= 122)):
            data1 = data[data['Name'].str.find(sub) != -1]
            my_tree.pack_forget()
            tree_scroll_x.pack_forget()
            tree_scroll_y.pack_forget()
            show_treeview(data1)

        else:
            pass

    # when backspace pressed, it will search for records using the string left in the entry box.
    def backspace(e):
        sub = search_by_name_entry.get()[:-1]

        if sub == '':
            my_tree.pack_forget()
            tree_scroll_x.pack_forget()
            tree_scroll_y.pack_forget()
            show_treeview(data)

        else:
            data1 = data[data['Name'].str.find(sub) != -1]
            my_tree.pack_forget()
            tree_scroll_x.pack_forget()
            tree_scroll_y.pack_forget()
            show_treeview(data1)

    def go_back_to_files_page():
        my_tree.pack_forget()
        tree_scroll_x.pack_forget()
        tree_scroll_y.pack_forget()
        raise_frame(table_frame)

    go_back_to_files_page_button = tk.Button(tree_frame2, borderwidth=0, command=go_back_to_files_page, image=go_back_img)
    go_back_to_files_page_button.place(relx=0.01, rely=0.01)

    record_labelframe = tk.LabelFrame(tree_frame2, text='Record', font=('Calibri', 13))
    record_labelframe.place(relx=0.12, rely=0.50)

    name_label = tk.Label(record_labelframe, text='Name', font=('Calibri', 13))
    name_label.grid(row=0, column=0, padx=10, pady=10)
    name_entry = tk.Entry(record_labelframe, font=('Calibri', 13))
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    roll_no_label = tk.Label(record_labelframe, text='Roll No.', font=('Calibri', 13))
    roll_no_label.grid(row=0, column=2, padx=10, pady=10)
    roll_no_entry = tk.Entry(record_labelframe, font=('Calibri', 13))
    roll_no_entry.grid(row=0, column=3, padx=10, pady=10)

    maths_label = tk.Label(record_labelframe, text='Maths', font=('Calibri', 13))
    maths_label.grid(row=0, column=4, padx=10, pady=10)
    maths_entry = tk.Entry(record_labelframe, font=('Calibri', 13))
    maths_entry.grid(row=0, column=5, padx=10, pady=10)

    physics_label = tk.Label(record_labelframe, text='Physics', font=('Calibri', 13))
    physics_label.grid(row=0, column=6, padx=10, pady=10)
    physics_entry = tk.Entry(record_labelframe, font=('Calibri', 13))
    physics_entry.grid(row=0, column=7, padx=10, pady=10)

    chemistry_label = tk.Label(record_labelframe, text='Chemistry', font=('Calibri', 13))
    chemistry_label.grid(row=1, column=0, padx=10, pady=10)
    chemistry_entry = tk.Entry(record_labelframe, font=('Calibri', 13))
    chemistry_entry.grid(row=1, column=1, padx=10, pady=10)

    ip_label = tk.Label(record_labelframe, text='IP', font=('Calibri', 13))
    ip_label.grid(row=1, column=2, padx=10, pady=10)
    ip_entry = tk.Entry(record_labelframe, font=('Calibri', 13))
    ip_entry.grid(row=1, column=3, padx=10, pady=10)

    english_label = tk.Label(record_labelframe, text='English', font=('Calibri', 13))
    english_label.grid(row=1, column=4, padx=10, pady=10)
    english_entry = tk.Entry(record_labelframe, font=('Calibri', 13))
    english_entry.grid(row=1, column=5, padx=10, pady=10)

    clear_button = tk.Button(record_labelframe, text="Clear", font=('Calibri', 13), width=20, command=clear)
    clear_button.grid(row=1, column=7)

    commands_labelframe = tk.LabelFrame(tree_frame2, text='Commands', font=('Calibri', 13))
    commands_labelframe.place(relx=0.04, rely=0.7)

    update_record_button = tk.Button(commands_labelframe, text='Update Record', font=('Calibri', 13), command=update)
    update_record_button.grid(row=0, column=1, padx=10, pady=10)

    add_record_button = tk.Button(commands_labelframe, text='Add Record', font=('Calibri', 13), command=add_record)
    add_record_button.grid(row=0, column=2, padx=50, pady=10)

    remove_all_records_button = tk.Button(commands_labelframe, text='Remove All Records', font=('Calibri', 13),
                                          command=remove_all)
    remove_all_records_button.grid(row=0, column=3, padx=10, pady=10)

    remove_selected_records_button = tk.Button(commands_labelframe, text='Remove Selected Records',
                                               font=('Calibri', 13), command=remove_selected)
    remove_selected_records_button.grid(row=0, column=4, padx=50, pady=10)

    sort_by_button = tk.Button(commands_labelframe, text="Sort by", font=('Calibri', 13), command=sort)
    sort_by_button.grid(row=0, column=5)

    plot_graph_button = tk.Button(commands_labelframe, text='Plot Graph', font=('Calibri', 13), command=plot_graph)
    plot_graph_button.grid(row=1, column=1)

    move_down_button = tk.Button(commands_labelframe, text='Move Down', font=('Calibri', 13), command=move_down)
    move_down_button.grid(row=0, column=9, padx=10)

    move_up_button = tk.Button(commands_labelframe, text='Move Up', font=('Calibri', 13), command=move_up)
    move_up_button.grid(row=0, column=8, padx=50)

    search_by_name_label = tk.Label(commands_labelframe, text='Search by Name', font=('Calibri', 13))
    search_by_name_label.grid(row=2, column=1)

    search_by_name_entry = tk.Entry(commands_labelframe, font=('Calibri', 13))
    search_by_name_entry.grid(row=2, column=2, pady=20)
    search_by_name_entry.bind("<Key>", search)
    search_by_name_entry.bind("<BackSpace>", backspace)

    clicked1 = tk.StringVar()
    clicked1.set('Column Name')
    options = data.columns

    drop1 = tk.OptionMenu(commands_labelframe, clicked1, *options)
    drop1.grid(row=0, column=6)
    drop1.config(font=('Calibri', 13))
    menu1 = root.nametowidget(drop1.menuname)
    menu1.config(font=('Calibri', 13))

    clicked2 = tk.StringVar()
    clicked2.set('Choose')
    drop2 = tk.OptionMenu(commands_labelframe, clicked2, "Subject-wise", "Student report", "Class report")
    drop2.grid(row=1, column=2, padx=10)
    drop2.config(font=('Calibri', 13))
    menu2 = root.nametowidget(drop2.menuname)
    menu2.config(font=('Calibri', 13))

    clicked3 = tk.StringVar()
    clicked3.set('Ascending')
    drop3 = tk.OptionMenu(commands_labelframe, clicked3, "Ascending", "Descending")
    drop3.grid(row=0, column=7, padx=0)
    drop3.config(font=('Calibri', 13))
    menu3 = root.nametowidget(drop3.menuname)
    menu3.config(font=('Calibri', 13))

    clicked4 = tk.StringVar()
    clicked4.set('Choose subject')
    drop4 = tk.OptionMenu(commands_labelframe, clicked4, *options[2:len(options) - 2])
    drop4.grid(row=1, column=3)
    drop4.config(font=('Calibri', 13))
    menu4 = root.nametowidget(drop4.menuname)
    menu4.config(font=('Calibri', 13))


user_df = pd.read_csv('E:/IP Project Assets/user.csv', index_col=None)

data = None

bg_img = Image.open('E:/IP Project Assets/Images/bg.png')
bg_img = bg_img.resize((960, 1080))
bg = ImageTk.PhotoImage(bg_img)
bg_label = tk.Label(main_frame, image=bg)

show_password_img = Image.open('E:/IP Project Assets/Images/show.png')
show_password_img = show_password_img.resize((30, 30))
show_password_img = ImageTk.PhotoImage(show_password_img)

hide_password_img = Image.open('E:/IP Project Assets/Images/hide.png')
hide_password_img = hide_password_img.resize((30, 30))
hide_password_img = ImageTk.PhotoImage(hide_password_img)

bg_label.place(relx=0.4, rely=0)


login_button_img = Image.open('E:/IP Project Assets/Images/log.png')
login_button_img = login_button_img.resize((250, 65))
login_button_img = ImageTk.PhotoImage(login_button_img)

signup_button_img = Image.open('E:/IP Project Assets/Images/sig.png')
signup_button_img = signup_button_img.resize((250, 65))
signup_button_img = ImageTk.PhotoImage(signup_button_img)

go_back_img = Image.open('E:/IP Project Assets/Images/goback.png')
go_back_img = go_back_img.resize((45, 45))
go_back_img = ImageTk.PhotoImage(go_back_img)

logout_img = Image.open('E:/IP Project Assets/Images/logout.png')
logout_img = logout_img.resize((250, 65))
logout_img = ImageTk.PhotoImage(logout_img)

school_name_label = tk.Label(main_frame, text='SCHOOL', font=('Copperplate Gothic Light', 43))
school_name_label.place(relx=0.1, rely=0.4)
gradeBook_label = tk.Label(main_frame, text='GRADEBOOK', font=('Copperplate Gothic Light', 43))
gradeBook_label.place(relx=0.062, rely=0.5)

main_labelframe = tk.LabelFrame(main_frame, text='', bg='#f0f0f0', width=400, height=400, relief='groove')
signup_button = tk.Button(main_labelframe, text='SIGN UP', font=('Calibri', 22), borderwidth=0, image=signup_button_img,
                          command=lambda: raise_frame(signup_frame))
login_button = tk.Button(main_labelframe, text='LOGIN', font=('Calibri', 22), borderwidth=0, image=login_button_img,
                         command=lambda: raise_frame(login_frame))
main_labelframe.place(relx=0.57, rely=0.25)
login_button.place(relx=0.2, rely=0.35)
signup_button.place(relx=0.2, rely=0.65)

welcome_label = tk.Label(main_labelframe, text='WELCOME', font=('Bookman Old Style', 30))
welcome_label.place(relx=0.23, rely=0.1)

login_frame = tk.Frame(root, height=600, width=600, bg='#f0f0f0')
login_frame.place(relx=0.51, rely=0.13)
signup_frame = tk.Frame(root, height=600, width=600, bg='#f0f0f0')
signup_frame.place(relx=0.51, rely=0.13)

login_label = tk.Label(login_frame, text="LOGIN", font=('Copperplate Gothic Light', 32), bg='#f0f0f0')
login_label.place(relx=0.38, rely=0.03)

name_label1 = tk.Label(login_frame, text='Name', font=('Constantia', 22), bg='#f0f0f0')
class_label1 = tk.Label(login_frame, text="Class", font=('Constantia', 22), bg='#f0f0f0')
passwd_label1 = tk.Label(login_frame, text='Password', font=('Constantia', 22), bg='#f0f0f0')

name_label1.place(relx=0.1, rely=0.25)
class_label1.place(relx=0.1, rely=0.45)
passwd_label1.place(relx=0.1, rely=0.65)

name_entry1 = tk.Entry(login_frame, font=('Times New Roman', 22))
class_entry1 = tk.Entry(login_frame, font=('Times New Roman', 22))
passwd_entry1 = tk.Entry(login_frame, font=('Times New Roman', 22), show='*')
name_entry1.place(relx=0.4, rely=0.25)
class_entry1.place(relx=0.4, rely=0.45)
passwd_entry1.place(relx=0.4, rely=0.65)

go_back_from_login_frame_button = tk.Button(login_frame, image=go_back_img, borderwidth=0,
                                            command=lambda: raise_frame(main_frame))
go_back_from_login_frame_button.place(relx=0.05, rely=0.03)

login_button1 = tk.Button(login_frame, text='LOGIN', command=login, borderwidth=0, font=('Constantia', 6),
                          image=login_button_img, state='disabled')
login_button1.place(relx=0.3, rely=0.8)

toggle_passwd_button1 = tk.Button(login_frame, image=show_password_img, borderwidth=0,
                                  command=lambda: toggle_password(passwd_entry1, toggle_passwd_button1))
toggle_passwd_button1.place(relx=0.92, rely=0.65)

name_entry1.var = tk.StringVar()
name_entry1['textvariable'] = name_entry1.var
name_entry1.var.trace_add('write', toggle_state)
class_entry1.var = tk.StringVar()
class_entry1['textvariable'] = class_entry1.var
class_entry1.var.trace_add('write', toggle_state)
passwd_entry1.var = tk.StringVar()
passwd_entry1['textvariable'] = passwd_entry1.var
passwd_entry1.var.trace_add('write', toggle_state)

signup_label = tk.Label(signup_frame, text="SIGN UP", font=('Copperplate Gothic Light', 32), bg='#f0f0f0')
signup_label.place(relx=0.36, rely=0.03)

name_label2 = tk.Label(signup_frame, text='Name', font=('Constantia', 22), bg='#f0f0f0')
class_label2 = tk.Label(signup_frame, text="Class", font=('Constantia', 22), bg='#f0f0f0')
passwd_label2 = tk.Label(signup_frame, text='Password', font=('Constantia', 22), bg='#f0f0f0')
name_label2.place(relx=0.1, rely=0.25)
class_label2.place(relx=0.1, rely=0.45)
passwd_label2.place(relx=0.1, rely=0.65)

name_entry2 = tk.Entry(signup_frame, font=('Times New Roman', 22))
class_entry2 = tk.Entry(signup_frame, font=('Times New Roman', 22))
passwd_entry2 = tk.Entry(signup_frame, font=('Times New Roman', 22), show='*')
name_entry2.place(relx=0.4, rely=0.25)
class_entry2.place(relx=0.4, rely=0.45)
passwd_entry2.place(relx=0.4, rely=0.65)

go_back_from_signup_frame_button = tk.Button(signup_frame, image=go_back_img, borderwidth=0,
                                             command=lambda: raise_frame(main_frame))
go_back_from_signup_frame_button.place(relx=0.05, rely=0.03)

signup_button1 = tk.Button(signup_frame, state='disabled', borderwidth=0, command=signup, image=signup_button_img)
signup_button1.place(relx=0.3, rely=0.8)

toggle_passwd_button2 = tk.Button(signup_frame, image=show_password_img, borderwidth=0,
                                  command=lambda: toggle_password(passwd_entry2, toggle_passwd_button2))
toggle_passwd_button2.place(relx=0.92, rely=0.65)

name_entry2.var = tk.StringVar()
name_entry2['textvariable'] = name_entry2.var
name_entry2.var.trace_add('write', toggle_state)
class_entry2.var = tk.StringVar()
class_entry2['textvariable'] = class_entry2.var
class_entry2.var.trace_add('write', toggle_state)
passwd_entry2.var = tk.StringVar()
passwd_entry2['textvariable'] = passwd_entry2.var
passwd_entry2.var.trace_add('write', toggle_state)

table_frame = tk.Frame(root)
table_frame.grid(row=0, column=0, sticky='news')

style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=25, fieldbackground="#D3D3D3",
                font=('Calibri', 13))
style.map("Treeview", background=[("selected", "#347083")])
style.configure('Treeview.Heading', font=('Calibri', 13))

tree_frame = tk.Frame(table_frame, height=275, width=420)
tree_frame.place(relx=0.6, rely=0.2)
tree_frame.pack_propagate(False)
tree_scroll = tk.Scrollbar(tree_frame)
tree_scroll.pack(side="right", fill="y")

teacher_name1 = tk.Label(table_frame, text='Name:', font=('Bookman Old Style', 21))
teacher_name1.place(relx=0.1, rely=0.2)
teacher_class1 = tk.Label(table_frame, text='Class:', font=('Bookman Old Style', 21))
teacher_class1.place(relx=0.1, rely=0.3)
teacher_name2 = tk.Label(table_frame, font=('Bookman Old Style', 21))
teacher_name2.place(relx=0.16, rely=0.2)
teacher_class2 = tk.Label(table_frame, font=('Bookman Old Style', 21))
teacher_class2.place(relx=0.16, rely=0.3)

my_tree1 = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="browse")
my_tree1.pack(fill='x')
tree_scroll.config(command=my_tree1.yview)

open_file_button = tk.Button(table_frame, text='Open File', font=('Calibri', 15), command=openFile)
open_file_button.place(relx=0.66, rely=0.57)

delete_file_button = tk.Button(table_frame, text='Delete File', font=('Calibri', 15), command=deleteFile)
delete_file_button.place(relx=0.74, rely=0.57)

open_file_label = tk.Label(table_frame, text='CHOOSE A FILE TO OPEN', font=('Bookman Old Style', 21))
open_file_label.place(relx=0.615, rely=0.1)

logout_button = tk.Button(table_frame, image=logout_img, borderwidth=0, command=lambda: raise_frame(main_frame))
logout_button.place(relx=0.83, rely=0.01)

create_file_label = tk.Label(table_frame, text='CREATE A NEW FILE', font=('Bookman Old Style', 21))
create_file_label.place(relx=0.65, rely=0.7)
new_file_label = tk.Label(table_frame, text='File name', font=('Bookman Old Style', 16))
new_file_label.place(relx=0.6, rely=0.8)
create_file_entry = tk.Entry(table_frame, font=('Times', 21))
create_file_entry.place(relx=0.7, rely=0.8)
create_file_button = tk.Button(table_frame, text='Create File', font=('Calibri', 15), command=create_file)
create_file_button.place(relx=0.7, rely=0.9)

teacher_details_label = tk.Label(table_frame, text='YOUR DETAILS:', font=('Bookman Old Style', 21))
teacher_details_label.place(relx=0.1, rely=0.1)

change_passwd_label = tk.Label(table_frame, text="CHANGE PASSWORD", font=('Bookman Old Style', 21))
change_passwd_label.place(relx=0.15, rely=0.45)
change_passwd_entry1 = tk.Entry(table_frame, font=('Times', 21))
change_passwd_entry1.place(relx=0.225, rely=0.55)
change_passwd_entry2 = tk.Entry(table_frame, font=('Times', 21))
change_passwd_entry2.place(relx=0.225, rely=0.65)
change_passwd_entry3 = tk.Entry(table_frame, font=('Times', 21))
change_passwd_entry3.place(relx=0.225, rely=0.75)
current_passwd_label = tk.Label(table_frame, text="Current Password", font=('Bookman Old Style', 16))
current_passwd_label.place(relx=0.08, rely=0.55)
new_passwd_label1 = tk.Label(table_frame, text="New Password", font=('Bookman Old Style', 16))
new_passwd_label1.place(relx=0.08, rely=0.65)
new_passwd_label2 = tk.Label(table_frame, text="Confirm New Password", font=('Bookman Old Style', 16))
new_passwd_label2.place(relx=0.04, rely=0.75)
change_passwd_button = tk.Button(table_frame, text='Change Password', font=('Calibri', 15), command=change_password)
change_passwd_button.place(relx=0.15, rely=0.85)

raise_frame(main_frame)

root.mainloop()
