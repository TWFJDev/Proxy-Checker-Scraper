from customtkinter import *
import json
from util import scrape
from threading import Thread

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

    def tabs_setup(self):
        tabview = CTkTabview(self, width=880, height=880)
        tabview.pack(padx=10, pady=10)

        self.scrape_tab = tabview.add('Scrape Proxies')
        self.check_tab = tabview.add('Check Proxies')
        self.proxy_database = tabview.add('Proxy Database')

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
        
    def log(self, message):
        try:
            self.log_box.insert("end", message + "\n")
            self.log_box.see("end")
        except:
            self.after(1, lambda: self.log(message))


app = App()
app.mainloop()