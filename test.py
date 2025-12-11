import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# ------------------ SQLAlchemy Setup ------------------
engine = create_engine("sqlite:///example.db", echo=False)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


# ------------------ Functions ------------------
def insert_user():
    name = name_entry.get()
    email = email_entry.get()
    if not name or not email:
        return
    new_user = User(name=name, email=email)
    session.add(new_user)
    session.commit()
    load_data()
    name_entry.delete(0, "end")
    email_entry.delete(0, "end")


def load_data():
    for row in tree.get_children():
        tree.delete(row)
    users = session.query(User).all()
    for u in users:
        tree.insert("", "end", values=(u.id, u.name, u.email))


# ------------------ CTk Window ------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("650x450")
app.title("CTk + ttk.Treeview + SQLAlchemy")

# ------------------ Input Form ------------------
form_frame = ctk.CTkFrame(app)
form_frame.pack(fill="x", pady=10, padx=10)

ctk.CTkLabel(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
name_entry = ctk.CTkEntry(form_frame)
name_entry.grid(row=0, column=1, padx=5, pady=5)

ctk.CTkLabel(form_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5)
email_entry = ctk.CTkEntry(form_frame)
email_entry.grid(row=1, column=1, padx=5, pady=5)

ctk.CTkButton(form_frame, text="Add User", command=insert_user).grid(
    row=2, column=0, columnspan=2, pady=10
)

# ------------------ Treeview Section ------------------
table_frame = ctk.CTkFrame(app)
table_frame.pack(fill="both", expand=True, padx=10, pady=10)

# ------------------ Dark-themed Scrollbar ------------------
style = ttk.Style()
style.theme_use("clam")  # Must use a theme that allows coloring

style.configure(
    "Vertical.TScrollbar",
    background="#2B2B2B",       # Scrollbar thumb color
    troughcolor="#1E1E1E",      # Track color
    arrowcolor="white",          # Arrow color
    bordercolor="#2B2B2B",
    borderwidth=0,
    relief="flat"
)

scrollbar = ttk.Scrollbar(table_frame, orient="vertical", style="Vertical.TScrollbar")
scrollbar.pack(side="right", fill="y")

# ------------------ Treeview ------------------
columns = ("ID", "Name", "Email")
tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    yscrollcommand=scrollbar.set
)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.pack(fill="both", expand=True)
scrollbar.config(command=tree.yview)

# ------------------ Dark Treeview Styling ------------------
style.configure(
    "Treeview",
    background="#2B2B2B",
    foreground="white",
    rowheight=28,
    fieldbackground="#2B2B2B",
    bordercolor="#2B2B2B",
    borderwidth=0
)
style.map(
    "Treeview",
    background=[("selected", "#1E90FF")]
)

load_data()
app.mainloop()
