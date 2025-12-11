from customtkinter import *
import json
from util import scrape
from threading import Thread
import tkinter as tk
from tkinter import ttk

class App(CTk):

    def __init__(self):
        super().__init__()

        self.title("Vyrus Proxy Checker/Scraper")
        self.geometry("900x600")
        set_appearance_mode("dark")
        set_default_color_theme("dark-blue")
        self.resizable(False, False)

        self.tabs_setup()
        self.scrape_tab_stuff()
        self.proxy_database()

    def tabs_setup(self):
        tabview = CTkTabview(self, width=880, height=880)
        tabview.pack(padx=10, pady=10)

        self.scrape_tab = tabview.add('Scrape Proxies')
        self.check_tab = tabview.add('Check Proxies')
        self.proxy_database_tab = tabview.add('Proxy Database')

    def scrape_tab_stuff(self):
        with open('sources.json', 'r') as f:
            info = json.load(f)

        url_picker_frame = CTkFrame(self.scrape_tab)
        url_picker_frame.pack(pady=10)

        url_picker_label = CTkLabel(url_picker_frame, text='Choose A Source: ')
        url_picker_label.pack(padx=5, side='left', anchor='center')

        url_values = ['all']
        for source in info['sources']:
            url_values.append(source['name'])

        url_picker = CTkOptionMenu(url_picker_frame, values=url_values)
        url_picker.pack(padx=5, side='right', anchor='center')

        proxy_type_frame = CTkFrame(self.scrape_tab)
        proxy_type_frame.pack(pady=10)

        proxy_type_label = CTkLabel(proxy_type_frame, text='Proxy Type: ')
        proxy_type_label.pack(padx=5, side='left', anchor='center')

        proxy_type_values = ['all', 'http', 'https', 'socks4', 'socks5']
        proxy_type_picker = CTkOptionMenu(proxy_type_frame, values=proxy_type_values)
        proxy_type_picker.pack(padx=5, side='right', anchor='center')

        scrape_button = CTkButton(
            self.scrape_tab, 
            text='Start Scrape',
            command=lambda: Thread(
                target=scrape, 
                args=(url_picker.get(), proxy_type_picker.get(), self.log)
            ).start()
        )
        scrape_button.pack(pady=10)
        
        self.log_box = CTkTextbox(self.scrape_tab)
        self.log_box.pack(fill="both", expand=True, pady=10, padx=10)

    def proxy_database(self):
        table_frame = CTkFrame(self.proxy_database_tab)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Vertical.TScrollbar",
            background="#2B2B2B",
            troughcolor="#1E1E1E",
            arrowcolor="white",
            bordercolor="#2B2B2B",
            borderwidth=0,
            relief="flat"
        )

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", style="Vertical.TScrollbar")
        scrollbar.pack(side="right", fill="y")

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
        
    def log(self, message):
        try:
            self.log_box.insert("end", message + "\n")
            self.log_box.see("end")
        except:
            self.after(1, lambda: self.log(message))


app = App()
app.mainloop()