import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from models import *
class EnrollmentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Candidate Enrollment Application")
        self.root.geometry("600x400")

        self.create_login_frame()

    def create_login_frame(self):
        self.login_frame = ttk.Frame(self.root, padding="50 50 50 50")
        self.login_frame.pack(padx=10, pady=10, fill='x', expand=True)

        ttk.Label(self.login_frame, text="Username").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.username_entry = ttk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5, sticky='e')

        ttk.Label(self.login_frame, text="Password").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.password_entry = ttk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5, sticky='e')

        ttk.Button(self.login_frame, text="Login", command=self.login).grid(row=2, columnspan=2, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == 'admin' and password == 'password':
            self.user_role = 'admin'
            self.login_frame.pack_forget()
            self.create_dashboard()
        else :
            user = session.query(Candidate).filter_by(email=username).first()
            if user and password == 'password':  # Simplified password check
                self.user_role = 'user'
                # self.logged_in_user = user
                self.login_frame.pack_forget()
                self.create_user_dashboard()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")

    def create_dashboard(self):
        self.dashboard_frame = ttk.Frame(self.root, padding="10 10 10 10")
        self.dashboard_frame.pack(padx=10, pady=10, fill='x', expand=True)

        if self.user_role == 'admin':
            ttk.Button(self.dashboard_frame, text="Add Candidate", command=self.add_candidate).grid(row=0, column=0, padx=5, pady=5)
            ttk.Button(self.dashboard_frame, text="View Candidates", command=self.view_candidates).grid(row=0, column=1, padx=5, pady=5)
        # elif self.user_role == 'user':
        #     ttk.Button(self.dashboard_frame, text="View Candidates", command=self.view_candidates).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(self.dashboard_frame, text="Back", command=self.back_to_login).grid(row=1, column=0, columnspan=2, pady=10)

    def create_user_dashboard(self):
        self.dashboard_frame = ttk.Frame(self.root, padding="10 10 10 10")
        self.dashboard_frame.pack(padx=10, pady=10, fill='x', expand=True)

       
        ttk.Label(self.dashboard_frame, text=f"Welcome, {self.logged_in_user.name}").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        ttk.Label(self.dashboard_frame, text=f"Email: {self.logged_in_user.email}").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        ttk.Label(self.dashboard_frame, text=f"Phone: {self.logged_in_user.phone}").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        ttk.Label(self.dashboard_frame, text=f"Status: {self.logged_in_user.status}").grid(row=3, column=0, padx=5, pady=5, sticky='w')

        ttk.Button(self.dashboard_frame, text="Back", command=self.back_to_login).grid(row=4, column=0, pady=10)
    
    def add_candidate(self):
        self.dashboard_frame.pack_forget()
        self.add_frame = ttk.Frame(self.root, padding="10 10 10 10")
        self.add_frame.pack(padx=10, pady=10, fill='x', expand=True)

        ttk.Label(self.add_frame, text="Name").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.name_entry = ttk.Entry(self.add_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky='e')

        ttk.Label(self.add_frame, text="Email").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.email_entry = ttk.Entry(self.add_frame)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5, sticky='e')

        ttk.Label(self.add_frame, text="Phone").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.phone_entry = ttk.Entry(self.add_frame)
        self.phone_entry.grid(row=2, column=1, padx=5, pady=5, sticky='e')

        ttk.Button(self.add_frame, text="Submit", command=self.submit_candidate).grid(row=3, columnspan=2, pady=10)
        ttk.Button(self.add_frame, text = "Back", command = self.dashboard).grid(row = 4, columnspan=2)
        
    def submit_candidate(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()

        new_candidate = Candidate(name=name, email=email, phone=phone)
        session.add(new_candidate)
        session.commit()
        messagebox.showinfo("Success", "Candidate added successfully")
        self.add_frame.pack_forget()
        self.create_dashboard()

    def view_candidates(self):

        for widget in self.root.winfo_children():
            widget.destroy()

        self.view_frame = ttk.Frame(self.root, padding="10 10 10 10")
        self.view_frame.pack( fill='both', expand=True)

        columns = ("ID", "Name", "Email", "Phone")
        self.tree = ttk.Treeview(self.view_frame, columns=columns, show='headings', height=10)

       
        for col in columns:
            self.tree.heading(col, text=col)
           
            self.tree.column(col, anchor='center', width=150)

       
        candidates = session.query(Candidate).all()
        count = 0 
        for candidate in candidates:
            if count % 2 == 0 :
                self.tree.insert("", "end", values=(candidate.id, candidate.name, candidate.email, candidate.phone), tags = "evenrow")
            else: 
                self.tree.insert("", "end", values=(candidate.id, candidate.name, candidate.email, candidate.phone), tags = "oddrow")    
            count += 1 
        
        vsb = ttk.Scrollbar(self.view_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side='right', fill='y')

        
        hsb = ttk.Scrollbar(self.view_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=hsb.set)
        hsb.pack(side='bottom', fill='x')

        self.tree.pack(fill='both', expand=True)

       
        back_button = ttk.Button(self.view_frame, text="Back", command=self.back_to_dashboard)
        back_button.pack(pady=10)
        ttk.Button(self.view_frame, text= "Edit", command= self.edit_candidate_by_id).pack()


        
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Times New Roman', 12, 'bold'))
        style.configure("Treeview", font=('Times New Roman', 10))

        
        self.tree.tag_configure('oddrow', background='lightgray')
        self.tree.tag_configure('evenrow', background='white')
        style.map('Treeview', background=[('selected', 'lightblue')], foreground=[('selected', 'black')])
         
    def edit_candidate_by_id(self):
        # self.dashboard_frame.pack_forget()
        self.edit_search_frame = ttk.Frame(self.root, padding="10 10 10 10")
        self.edit_search_frame.pack(padx=10, pady=10, fill='x', expand=True)

        ttk.Label(self.edit_search_frame, text="Enter Candidate ID to Edit:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.edit_id_entry = ttk.Entry(self.edit_search_frame)
        self.edit_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky='e')

        ttk.Button(self.edit_search_frame, text="Search", command=self.load_candidate_for_edit).grid(row=1, columnspan=2, pady=10)
    def load_candidate_for_edit(self):
        candidate_id = self.edit_id_entry.get()
        candidate = session.query(Candidate).filter_by(id=candidate_id).first()

        if candidate:
            self.edit_search_frame.pack_forget()
            self.edit_frame = ttk.Frame(self.root, padding="10 10 10 10")
            self.edit_frame.pack(padx=10, pady=10, fill='x', expand=True)

            ttk.Label(self.edit_frame, text="Name").grid(row=0, column=0, padx=5, pady=5, sticky='w')
            self.edit_name_entry = ttk.Entry(self.edit_frame)
            self.edit_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky='e')
            self.edit_name_entry.insert(0, candidate.name)

            ttk.Label(self.edit_frame, text="Email").grid(row=1, column=0, padx=5, pady=5, sticky='w')
            self.edit_email_entry = ttk.Entry(self.edit_frame)
            self.edit_email_entry.grid(row=1, column=1, padx=5, pady=5, sticky='e')
            self.edit_email_entry.insert(0, candidate.email)

            ttk.Label(self.edit_frame, text="Phone").grid(row=2, column=0, padx=5, pady=5, sticky='w')
            self.edit_phone_entry = ttk.Entry(self.edit_frame)
            self.edit_phone_entry.grid(row=2, column=1, padx=5, pady=5, sticky='e')
            self.edit_phone_entry.insert(0, candidate.phone)

            ttk.Button(self.edit_frame, text="Update", command=lambda: self.update_candidate(candidate.id)).grid(row=3, columnspan=2, pady=10)
        else:
            messagebox.showerror("Error", "Candidate ID not found")

    def update_candidate(self, candidate_id):
        name = self.edit_name_entry.get()
        email = self.edit_email_entry.get()
        phone = self.edit_phone_entry.get()

        candidate = session.query(Candidate).filter_by(id=candidate_id).first()
        if candidate:
            candidate.name = name
            candidate.email = email
            candidate.phone = phone
            session.commit()
            messagebox.showinfo("Success", "Candidate updated successfully")
            self.edit_frame.pack_forget()
            self.create_dashboard()
        else:
            messagebox.showerror("Error", "Failed to update candidate")

    def back_to_dashboard(self):
        self.view_frame.pack_forget()
        self.create_dashboard()

    def back_to_login(self):
        self.dashboard_frame.pack_forget()
        self.create_login_frame()
    def dashboard(self):
        self.add_frame.pack_forget()
        self.create_dashboard()
        
    

if __name__ == "__main__":
    root = tk.Tk()
    app = EnrollmentApp(root)
    root.mainloop()
