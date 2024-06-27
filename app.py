import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from models import Candidate, session  # Make sure to import your Candidate model and session correctly

class EnrollmentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Candidate Enrollment Application")

        self.create_login_frame()

    def create_login_frame(self):
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(padx=10, pady=10, fill='x', expand=True)

        tk.Label(self.login_frame, text="Username").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5, sticky='e')

        tk.Label(self.login_frame, text="Password").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5, sticky='e')

        tk.Button(self.login_frame, text="Login", command=self.login).grid(row=2, columnspan=2, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == 'admin' and password == 'password':
            self.user_role = 'admin'
            self.login_frame.pack_forget()
            self.create_dashboard()
        elif username == 'user' and password == 'password':
            self.user_role = 'user'
            self.login_frame.pack_forget()
            self.create_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def create_dashboard(self):
        self.dashboard_frame = tk.Frame(self.root)
        self.dashboard_frame.pack(padx=10, pady=10, fill='x', expand=True)

        if self.user_role == 'admin':
            tk.Button(self.dashboard_frame, text="Add Candidate", command=self.add_candidate).grid(row=0, column=0, padx=5, pady=5)
            tk.Button(self.dashboard_frame, text="View Candidates", command=self.view_candidates).grid(row=0, column=1, padx=5, pady=5)
        elif self.user_role == 'user':
            tk.Button(self.dashboard_frame, text="View Candidates", command=self.view_candidates).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(self.dashboard_frame, text="Back", command=self.back_to_login).grid(row=1, column=0, columnspan=2, pady=10)
    def add_candidate(self):
        self.dashboard_frame.pack_forget()
        self.add_frame = tk.Frame(self.root)
        self.add_frame.pack(padx=10, pady=10, fill='x', expand=True)

        tk.Label(self.add_frame, text="Name").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.name_entry = tk.Entry(self.add_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky='e')

        tk.Label(self.add_frame, text="Email").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.email_entry = tk.Entry(self.add_frame)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5, sticky='e')

        tk.Label(self.add_frame, text="Phone").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.phone_entry = tk.Entry(self.add_frame)
        self.phone_entry.grid(row=2, column=1, padx=5, pady=5, sticky='e')

        tk.Button(self.add_frame, text="Submit", command=self.submit_candidate).grid(row=3, columnspan=2, pady=10)

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
        self.dashboard_frame.pack_forget()
        self.view_frame = tk.Frame(self.root)
        self.view_frame.pack(padx=10, pady=10, fill='x', expand=True)

        candidates = session.query(Candidate).all()
        for idx, candidate in enumerate(candidates):
            tk.Label(self.view_frame, text=f"{candidate.id} - {candidate.name}").grid(row=idx, column=0, padx=5, pady=5, sticky='w')

        tk.Button(self.view_frame, text="Back", command=self.back_to_dashboard).grid(row=len(candidates), column=0, pady=10)

    def back_to_dashboard(self):
        self.view_frame.pack_forget()
        self.create_dashboard()
    def back_to_login(self):
        self.dashboard_frame.pack_forget()
        self.create_login_frame()

if __name__ == "__main__":
    root = tk.Tk()
    app = EnrollmentApp(root)
    root.mainloop()
