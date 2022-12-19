import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import re
import random
import os

# Create the main window
window = tk.Tk()
window.title("Login Form")
window.geometry('265x140')
window.resizable(False, False)


def form2():
    # Delete the members.txt file if it exists
    if os.path.exists('members.txt'):
        os.remove('members.txt')

    # Create a new, empty members.txt file
    open('members.txt', 'w').close()

    # Create the root window
    root = tk.Tk()
    root.geometry('500x610')
    root.title('Bank Registration Form')
    root.configure(bg='alice blue')
    root.resizable(False, False)

    # Create an empty list to store the member data
    member_data=[]
    #This function generates a random 10-digit number and displays it in the Card textbox
    def generate_number():
        member_card.delete(0, "end")
        list = ["0","1","2","3","4","5","6","7","8","9"]
        number = "0321"
        for i in range(10):
            number = number + random.choice(list)
        member_card.insert(0, number)
    
    # Define a function to load the member data into the record_table Treeview widget
    def load_member_data():
        # Delete any existing data in the record_table widget
        for item in record_table.get_children():
            record_table.delete(item)

        # Insert the member data from the member_data list into the record_table widget
        for r in range(len(member_data)):
            record_table.insert(parent='',index='end',text='',
                               iid=r,values=member_data[r])

    # Define a function to add a new member's data to the member_data list if it is valid and unique
    def add_member_data(memb_id, memb_name, memb_email, memb_no):
        # Check if the id is valid
        memb_id_pattern = re.compile(r'^\d{1,4}$')
        if not memb_id_pattern.match(memb_id):
            messagebox.showerror('Error', 'Invalid ID,The id should contain 1 to 4 numbers')
            return
        # Check if the email address is valid
        email_pattern = re.compile(r'[\w.-]+@[\w.-]+.\w+')
        if not email_pattern.match(memb_email):
            messagebox.showerror('Error', 'Invalid email address')
            return
        # Check if the card number is valid
        memb_no_pattern = re.compile(r'^\d{14}$')
        if not memb_no_pattern.match(str(memb_no)):
            messagebox.showerror('Error', 'Please click the generate button to get a card number')
            return
        # Check if the member's data already exists in the list
        if [memb_id, memb_name, memb_email, memb_no] in member_data:
            # If it exists, show an error message to the user
            messagebox.showerror('Error', 'Duplicate data is not allowed')
        else:
            # If it does not exist, add the data to the list
            member_data.append([memb_id, memb_name, memb_email, memb_no])
            with open('members.txt', 'a') as file:
                file.write(f"{memb_id},{memb_name},{memb_email},{memb_no}\n")
            member_id.delete(0, tk.END)
            member_name.delete(0, tk.END)
            member_email.delete(0, tk.END)
            member_card.delete(0, tk.END)
            load_member_data()

    # Define a function to update an existing member's data in the member_data list
    def update_member_data(memb_id,memb_name,memb_email,memb_no,index):
        # Update the member's data in the list
        member_data[index] = [memb_id,memb_name,memb_email,memb_no]
        # Read the entire file into memory
        with open('members.txt', 'r') as file:
            lines = file.readlines()

        # Replace the line with the updated member data
        lines[index] = f"{memb_id},{memb_name},{memb_email},{memb_no}\n"

        # Write the modified data back to the file
        with open('members.txt', 'w') as file:
            file.writelines(lines)
        # Reload the member data into the record_table Treeview widget
        load_member_data()

    # Define a function to delete an existing member's data from the member_data list
    def delete_member_data(index):
        # Delete the member's data from the list
        del member_data[index]
        # Read the entire file into memory
        with open('members.txt', 'r') as file:
            lines = file.readlines()

        # Delete the selected data
        lines[index] = f""

        # Write the modified data back to the file
        with open('members.txt', 'w') as file:
            file.writelines(lines)

        # Reload the member data into the record_table Treeview widget
        load_member_data()

        # Clear the data in the member entry widgets
        clear_member_data()

    # Define a function to put the selected member's data into the entry widgets
    def put_member_in_entry(selected_member_index):
        # Clear the data in the member entry widgets
        member_id.delete(0, tk.END)
        member_name.delete(0, tk.END)
        member_email.delete(0, tk.END)
        member_card.delete(0, tk.END)

        # Get the selected member's data from the member_data list
        memb_id = member_data[selected_member_index][0]
        memb_name = member_data[selected_member_index][1]
        memb_email = member_data[selected_member_index][2]
        memb_no = member_data[selected_member_index][3]

        # Put the selected member's data into the member entry widgets
        member_id.insert(0, memb_id)
        member_name.insert(0, memb_name)
        member_email.insert(0, memb_email)
        member_card.insert(0,memb_no)

    # Define a function to clear the data in the member entry widgets
    def clear_member_data():
        # Clear the data in the member entry widgets
        member_id.delete(0, tk.END)
        member_name.delete(0, tk.END)
        member_email.delete(0, tk.END)
        member_card.delete(0, tk.END)

        # Clear the data in the search entry widget
        search_entry.delete(0, tk.END)

        # Reload the member data in the member data table
        load_member_data()

    # Define a function to find members by ID
    def find_member_by_id(memb_id):
        # Check if the ID is not empty
        if memb_id != '':
            # Create a list to store the indexes of the members with the specified ID
            member_data_index = []

            # Loop through the member data
            for data in member_data:
                # If the specified ID is in the current data, append the index of the data to the member data index list
                if str(memb_id) in str(data[0]):
                    member_data_index.append(member_data.index(data))

            # Delete all the rows in the member data table
            for item in record_table.get_children():
                record_table.delete(item)

            # Loop through the member data index list
            for r in member_data_index:
                # Insert the member data with the specified ID into the member data table
                record_table.insert(parent='',index='end',text='',
                               iid=r,values=member_data[r])
        else:
            # If the ID is empty, load all the member data into the member data table
            load_member_data()
    def save_member_data():
        with open('memberdata.txt', 'w') as f:
            for item in member_data:
                f.write(f"{item[0]},{item[1]},{item[2]},{item[3]}\n")

    # The following code creates a head_frame frame, adds a heading_lb label to display the 
    # text "Bank Registration Form", and adds four labels and corresponding entry widgets to 
    # display the member ID, name, email, and card number.
    head_frame=tk.Frame(root)

    heading_lb = tk.Label(head_frame,text='Bank Registeration Form',
    font=('Bold',13),
    bg='cyan4',
    fg='white')

    heading_lb.pack(fill=tk.X,pady=5)

    member_id_lb = tk.Label(head_frame,text='Member ID : ',font=('bold',10))
    member_id_lb.place(x=0,y=50)

    member_id=tk.Entry(head_frame,font=('bold',10))
    member_id.place(x=110,y=50,width=180)

    member_name_lb = tk.Label(head_frame,text='Member Name : ',font=('bold',10))
    member_name_lb.place(x=0,y=100)

    member_name=tk.Entry(head_frame,font=('bold',10))
    member_name.place(x=110,y=100,width=180)

    member_email_lb = tk.Label(head_frame,text='Member Email : ',font=('bold',10))
    member_email_lb.place(x=0,y=150)

    member_email=tk.Entry(head_frame,font=('bold',10))
    member_email.place(x=110,y=150,width=180)

    member_card_lb = tk.Label(head_frame,text='Card Number : ',font=('bold',10))
    member_card_lb.place(x=0,y=200)

    member_card=tk.Entry(head_frame,font=('bold',10))
    member_card.place(x=110,y=200,width=180)
    
    
    # when clicked, it calls the add_member_data function with the current data in the entry
    # widgets as arguments
    register_btn = tk.Button(head_frame, text='Register', font=('Bold',12),command=lambda: add_member_data(member_id.get(),
                                                                                                          member_name.get(),
                                                                                                          member_email.get(),
                                                                                                          member_card.get()))
    register_btn.place(x=10, y=250)

    # when clicked, it calls the update_member_data function with the current data in the entry 
    # widgets and the index of the selected member in the record_table Treeview widget as arguments
    update_btn = tk.Button(head_frame, text='Update', font=('Bold',12),command=lambda: update_member_data(member_id.get(),
                                                                                                          member_name.get(),
                                                                                                          member_email.get(),
                                                                                                          member_card.get(),
                                                                                                          index=int(record_table.selection()[0])))
    update_btn.place(x=95, y=250)
    # when clicked, it calls the delete_member_data function with the index of the selected member in
    # the record_table Treeview widget as an argument
    delete_btn = tk.Button(head_frame, text='Delete', font=('Bold',12),command=lambda:delete_member_data(index=int(record_table.selection()[0])))
    delete_btn.place(x=173, y=250)

    # when clicked, it calls the clear_member_data function to clear the data in the entry widgets and
    # the record_table Treeview widget
    clear_btn = tk.Button(head_frame, text='Clear', font=('Bold',12),command=lambda:clear_member_data())
    clear_btn.place(x=245, y=250)
    
    random_btn = tk.Button(head_frame, text='Random', font=('Bold',12),command=lambda:generate_number())
    random_btn.place(x=317, y=250)
    
    head_frame.pack(pady=10)
    head_frame.pack_propagate(False)
    head_frame.configure(width=400,height=300)

    search_bar_frame = tk.Frame(root)

    # the label displays the text "Search By Member Id:"
    search_lb = tk.Label(search_bar_frame, text= 'Search By Member Id:',
                          font=('Bold', 10) )
    search_lb.pack(anchor=tk.W)

    # the entry widget allows the user to search for a member by their ID
    search_entry = tk.Entry(search_bar_frame,
    font=('Bold', 10))
    search_entry.pack(anchor=tk.W)
    search_entry.bind('<KeyRelease>',lambda e: find_member_by_id(search_entry.get()))

    # frame is then packed into the root window and its size is set to width=408, height=58.
    search_bar_frame.pack(pady=0)
    search_bar_frame.pack_propagate(False)
    search_bar_frame.configure(width=408, height=58)

    # Create a frame widget
    record_frame = tk.Frame(root)

    # Create a label widget
    record_lb = tk.Label(record_frame,text='Select Record for Delete or Update',
                        bg='cyan4',fg='White',font=('bold',13))
    record_lb.pack(fill=tk.X)

    # Create a Treeview widget
    record_table = ttk.Treeview(record_frame)
    record_table.pack(fill=tk.X,pady=5)
    # Bind an event handler to the Treeview widget
    record_table.bind('<<TreeviewSelect>>',lambda e: put_member_in_entry(int(record_table.selection()[0])))

    # Set the columns of the Treeview widget
    record_table['column'] = ['ID','Name','Email','CardNo']

    # Configure the '#0' column of the Treeview widget
    record_table.column('#0',anchor=tk.W, width=0,stretch=tk.NO)

    # Configuring the columns of the Treeview widget
    record_table.column('ID',anchor=tk.W,width=50)
    record_table.column('Name',anchor=tk.W,width=100)
    record_table.column('Email',anchor=tk.W,width=100)
    record_table.column('CardNo',anchor=tk.W,width=200)

    # Setting the headings of the columns of the Treeview widget
    record_table.heading('ID', text='ID', anchor=tk.W)
    record_table.heading('Name', text='Name', anchor=tk.W)
    record_table.heading('Email', text='Email', anchor=tk.W)
    record_table.heading('CardNo', text='CardNo', anchor=tk.W)

    # Pack the frame widget
    record_frame.pack(pady=10)
    # Prevent the frame widget from resizing its children
    record_frame.pack_propagate(False)
    record_frame.configure(width=400, height=200)
    label = tk.Label( text="Copyright @ 2022  |  MUJAHID | 0x11CA",bg='alice blue',fg='black',font=('Bold',12))
    label.place(x=110,y=585)

    root.mainloop()
# Create the login function
def login():
    # Get the username and password
    username = username_entry.get()
    password = password_entry.get()

    # Check if the username and password are correct
    if username == "admin" and password == "python":
        messagebox.showinfo("Succesfully", "Login Succesfully")
        # Close the login window
        window.destroy()

        # Open form 2
        form2()
    else:
        # Clear the input fields and show an error message
        username_entry.delete(0, "end")
        password_entry.delete(0, "end")
        messagebox.showerror('Error', 'Wrong password')

def hint():
    messagebox.showinfo("Hint", "Password : type of snake and programming language")

heading_lb = tk.Label(text='Bank Login Form',
font=('Bold',13),
bg='cyan4',
fg='white')

heading_lb.pack(fill=tk.X,pady=5)

username_label = tk.Label(text='Username : ',font=('bold',10))
username_label.place(x=0,y=30)

username_entry=tk.Entry(font=('bold',10))
username_entry.place(x=80,y=32,width=180)
username_entry.insert(0, "admin")
username_entry.config(state='disabled')


password_label = tk.Label(text='Password : ',font=('bold',10))
password_label.place(x=0,y=70)

password_entry=tk.Entry(font=('bold',10), show="*")
password_entry.place(x=80,y=70,width=180)

# Create the login button
login_button = tk.Button( text='Login', font=('Bold',12),command=login)
login_button.place(x=80, y=100,width=180)

hint_button = tk.Button( text='Hint', font=('Bold',12),command=hint)
hint_button.place(x=5, y=100,width=70)

# Run the main loop
window.mainloop()
