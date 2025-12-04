import customtkinter
import tkinter as tk
from PIL import Image
from customtkinter import CTkImage
import os
import requests
import sqlite3
import json
from datetime import datetime


# DEFINE ANG GLOBAL VARIABLES
CURRENT_USER_EMAIL = ""
CURRENT_USER_PASSWORD = ""
CURRENT_DISPLAY_NAME = ""
CURRENT_USER_ID = ""

#DATABASE CONFIG. ALSO, CREATE USERS AND CONVERSIONS TABLE FOR AUTH AND AUDIT TRAIL
def init_database():
    conn = sqlite3.connect('cointravert.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            password TEXT,
            name TEXT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            from_currency TEXT,
            to_currency TEXT,
            amount REAL,
            converted_amount REAL,
            timestamp TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()


init_database()

class SignUp(customtkinter.CTk):
    def __init__(self, position=None):
        super().__init__()
        if position:
            self.geometry(f"1280x800+{position[0]}+{position[1]}")
        else:
            self.geometry("1280x800")
        self.resizable(False, False)
        self.title("SignUp")

        self.frameMainBackground = customtkinter.CTkFrame(master=self, fg_color="black",width=640,height=860)
        self.frameMainBackground.grid(row=0, column=0, sticky="nsew")

        self.imgOpenBullish = Image.open("bullish.jpg")
        self.imgImageBullish = CTkImage(dark_image=self.imgOpenBullish, light_image=self.imgOpenBullish,size=(800, 1100))
        self.lblImageBullish = customtkinter.CTkLabel(master=self, image=self.imgImageBullish, text="")
        self.lblImageBullish.grid(row=0, column=1, sticky="e")

        self.imgOpenLogo = Image.open("logo_coinTraVert.png")
        self.imgOpenLogo = CTkImage(dark_image=self.imgOpenLogo, light_image=self.imgOpenLogo, size=(60, 100))

        self.lblTitle = customtkinter.CTkLabel(master=self.frameMainBackground, image=self.imgOpenLogo, text="CoinTraVert",text_color="white", font=('Yrsa', 15, "bold"), justify="right",compound="left")
        self.lblTitle.place(relx=0.14, rely=0.03, anchor="center")

        self.frameMainLogin =customtkinter.CTkFrame(master=self.frameMainBackground, fg_color="#15134E",width=530,height=610,corner_radius=30)
        self.frameMainLogin.place(relx=0.5,rely=0.35,anchor="center")

        self.lblJoinUs = customtkinter.CTkLabel(master=self.frameMainLogin, text="Join us and\nget full access",font=('Yrsa', 49, "bold"),justify="left",text_color="white")
        self.lblJoinUs.place(relx=0.41,rely=0.19,anchor="center")

        self.lblSignUpto = customtkinter.CTkLabel(master=self.frameMainLogin, text="Sign up to never miss a rate update\nagain!",font=('Yrsa', 18,"bold"),justify="left",text_color="#7E8DCE")
        self.lblSignUpto.place(relx=0.36,rely=0.36,anchor="center")

        self.lblEmail = customtkinter.CTkLabel(master=self.frameMainLogin, text="Email",font=('Yrsa', 18,"bold"),justify="left",text_color="white")
        self.lblEmail.place(relx=0.16,rely=0.47,anchor="center")

        self.imgOpenEmail = Image.open("email.png")
        self.imgImageEmail = CTkImage(dark_image=self.imgOpenEmail, light_image=self.imgOpenEmail, size=(30, 25))

        self.entryFrameEmail = customtkinter.CTkEntry(master=self.frameMainLogin, width=413, height=35,corner_radius=10, fg_color="white", border_color="black",placeholder_text="        Your email",font=('Yrsa',15,"bold"),text_color="black")
        self.entryFrameEmail.place(relx=0.5, rely=0.53, anchor="center")

        self.lblImageEmail = customtkinter.CTkLabel(master=self.entryFrameEmail, image=self.imgImageEmail, text="")
        self.lblImageEmail.place(relx=0.05, rely=0.5, anchor="center")

        self.entryFrameEmail.bind('<FocusIn>',self.click_email_entry)
        self.entryFrameEmail.bind('<FocusOut>',self.unclick_email_entry)

        self.lblPassword = customtkinter.CTkLabel(master=self.frameMainLogin, text="Password",font=('Yrsa', 18,"bold"),justify="left",text_color="white")
        self.lblPassword.place(relx=0.18,rely=0.60,anchor="center")

        self.entryPassword = customtkinter.CTkEntry(master=self.frameMainLogin, width=413, height=35,corner_radius=10, fg_color="white", border_color="black",placeholder_text="        Your password",font=('Yrsa',15,"bold"),text_color="black", show="*")
        self.entryPassword.place(relx=0.5, rely=0.66, anchor="center")

        self.agree_var = customtkinter.BooleanVar(value=False)
        self.chkBoxAgree = customtkinter.CTkCheckBox(
            master=self.frameMainLogin,
            text="By clicking \"Sign Up\", you agree to our Terms of Service\nand Privacy Policy.",
            font=('Yrsa', 12.5,"bold"),
            text_color="#7E8DCE",
            variable=self.agree_var
        )
        self.chkBoxAgree.place(relx=0.42, rely=0.73, anchor="center")

        self.lblMessage = customtkinter.CTkLabel(master=self.frameMainLogin, text="",font=('Yrsa', 14,"bold"),justify="left",text_color="red")
        self.lblMessage.place(relx=0.5, rely=0.80, anchor="center")

        self.btnSignUpEmail = customtkinter.CTkButton(master=self.frameMainLogin, command=self.handle_signup,text="Sign up email",font=('Yrsa', 19,"bold"),text_color="white",width=220,height=50,fg_color="#00008B",corner_radius=40)
        self.btnSignUpEmail.place(relx=0.49, rely=0.87, anchor="center")

        self.lblLoginInu = customtkinter.CTkButton(master=self.frameMainLogin, command=self.portal_login,text="Log in",font=('Yrsa', 12.5, "bold","underline"),text_color="#7E8DCE",fg_color="transparent",hover_color="#15134E")
        self.lblLoginInu.place(relx=0.65, rely=0.93, anchor="center")

        self.lblAlreadyHave = customtkinter.CTkLabel(master=self.frameMainLogin, text="Already have an account?",font=('Yrsa', 12.5, "bold"), justify="left", text_color="#7E8DCE")
        self.lblAlreadyHave.place(relx=0.42, rely=0.93, anchor="center")

    def handle_signup(self):
        conn = sqlite3.connect('cointravert.db')
        cursor = conn.cursor()
        # global variables
        global CURRENT_USER_EMAIL, CURRENT_USER_PASSWORD, CURRENT_USER_ID, CURRENT_DISPLAY_NAME
        email_value = self.entryFrameEmail.get()
        password_value = self.entryPassword.get()

        #from here to has_email. Kung may same email that means di mag p-proceed
        cursor.execute('''
                SELECT * FROM users WHERE email = ? 
                  ''', (email_value,))
        user = cursor.fetchone()
        has_email = False

        if user is not None:
           has_email = True

        if email_value == "" or password_value == "":
            self.lblMessage.configure(text="Please enter both email and password.", text_color="red")

        # verify kung meron "@" symbol kung wala then it means di siya email
        elif "@" not in email_value:
            self.lblMessage.configure(text="Email must contain @ symbol.", text_color="red")

        elif has_email:
            self.lblMessage.configure(text="Email already registered.", text_color="red")

        elif self.agree_var.get() == 0:
            self.lblMessage.configure(text="Please agree to the Terms first.", text_color="red")

        else:
            cursor.execute('''
                INSERT INTO users (email, password) VALUES (?, ?)
            ''', (email_value, password_value))
            conn.commit()

            cursor.execute('''
                    SELECT * FROM users WHERE email = ? AND password = ?
                      ''', (email_value, password_value))
            m_user = cursor.fetchone()

            #initializing global variables to the specific details of the user
            CURRENT_USER_ID = m_user[0]
            CURRENT_USER_EMAIL = m_user[1]
            CURRENT_USER_PASSWORD = m_user[2]
            CURRENT_DISPLAY_NAME = m_user[3]

            self.entryFrameEmail.delete(0, "end")
            self.entryPassword.delete(0, "end")
            self.lblMessage.configure(text="Account created! Go to Login to sign in.", text_color="light green")
        conn.close()
    def portal_login(self):
        pos = (self.winfo_x(), self.winfo_y())
        self.destroy()
        Login(position=pos).mainloop()
    def click_email_entry(self,event): #ok na to
        self.lblImageEmail.place_forget()
    def unclick_email_entry(self,event):
        if not self.entryFrameEmail.get():
            self.lblImageEmail.place(relx=0.05,rely=0.5,anchor="center")

class Login(customtkinter.CTk):
    def __init__(self, position=None):
        super().__init__()

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        if position:
            self.geometry(f"1280x800+{position[0]}+{position[1]}")
        else:
            self.geometry("1280x800")
        self.resizable(False, False)
        self.title("Login")

        base_dir = os.path.dirname(os.path.abspath(__file__))
        login_bg = os.path.join(base_dir, "login_bg.png")
        logo_path = os.path.join(base_dir, "cv-logo.png")

        main = customtkinter.CTkFrame(self, fg_color="black")
        main.pack(fill="both", expand=True)

        main.grid_columnconfigure(0,weight=0)
        main.grid_columnconfigure(1,weight=1)
        main.grid_rowconfigure(0,weight=1)

        top_bar = customtkinter.CTkFrame(main, fg_color="transparent")
        top_bar.place(x=40, y=20)

        logo_icon = customtkinter.CTkImage(
            light_image = Image.open(logo_path),
            size=(32,32)
        )
        logo_lbl = customtkinter.CTkLabel(top_bar, image=logo_icon, text="")
        logo_lbl.pack(side="left")
        # App name
        app_name_lbl = customtkinter.CTkLabel(
            top_bar,
            text="CoinTraVert",
            font=("Segoe UI", 20, "bold")
        )
        app_name_lbl.pack(side="left", padx=(10, 0))

        #Left Card (Log-in)
        login_card = customtkinter.CTkFrame(
            main,
            width=420,
            height= 500,
            corner_radius=20,
            fg_color="#0D0B52"
        )
        login_card.grid(row=0, column=0, padx=(40,12), pady=(100,40), sticky="ns")
        login_card.grid_propagate(False)
        login_card.grid_columnconfigure(0, weight=1)

        #Title + Login Greetings
        customtkinter.CTkLabel(
            login_card,
            text="Pleased to\nsee you back!",
            font=("Segoe UI", 38, "bold"),
            justify="left",
        ).grid(row=0, column=0, sticky="w", padx=40, pady=(40,10))

        customtkinter.CTkLabel(
            login_card,
            text="Sign in to access your dashboard\nand stay updated with new updates!",
            font=("Segoe UI", 15),
            text_color="gray80"
        ).grid(row=1, column=0, sticky="w", padx=40, pady=(0,25))

        customtkinter.CTkLabel( login_card, text="Email", font=("Segoe UI", 15, "bold")).grid(row=2, column=0, sticky="w", padx=40)
        self.email_input = customtkinter.CTkEntry(
            login_card,
            placeholder_text="Your email",
            width=300,
            height=40
        )
        self.email_input.grid(row=3, column=0, padx=40, pady=(5,20), sticky="w")

        customtkinter.CTkLabel( login_card, text="Password", font=("Segoe UI", 15, "bold")).grid(row=4, column=0, sticky="w", padx=40)
        self.pass_input = customtkinter.CTkEntry(
            login_card,
            placeholder_text="Your password",
            width=300,
            height=40,
            show="*"
        )
        self.pass_input.grid(row=5, column=0, padx=40, pady=(5,25), sticky="w")

        customtkinter.CTkLabel(
            login_card,
            text="By clicking Sign in, you are agreeing to our Terms and Policy.",
            font=("Segoe UI", 12),
            text_color="gray70",
            justify="left",
        ).grid(row=6, column=0, sticky="w", padx=40, pady=(0,20))

        self.login_message = customtkinter.CTkLabel(
            login_card,
            text="",
            font=("Segoe UI", 12),
            text_color="red"
        )
        self.login_message.grid(row=7, column=0, sticky="w", padx=40, pady=(0,10))

        customtkinter.CTkButton(
            login_card,
            command=self.handle_login,
            text="Log In",
            width=300,
            font=("Segoe UI", 15, "bold"),
            height=40,
            corner_radius=15
        ).grid(row=8, column=0, padx=40, pady=(0,20), sticky="w")

        #Sign Up link if wala pang account si user
        signup_card= customtkinter.CTkFrame(login_card, fg_color="transparent")
        signup_card.grid(row=9, column=0, padx=40, pady=(10,20), sticky="w")
        customtkinter.CTkLabel(signup_card, text="Don't have an account yet?", font=("Segoe UI",12)).pack(side="left")
        customtkinter.CTkButton(
            signup_card,
            command=self.portal_signup,
            text="Sign Up",
            fg_color="transparent",
            font=("Segoe UI", 12, "bold"),
            width=1,
            height=1,
            corner_radius=0
        ).pack(side="left",padx=(5,0))

        #Right Panel
        right_card = customtkinter.CTkFrame(main, fg_color="transparent")
        right_card.grid(row=0, column=1, sticky="nsew",padx=(40,0))
        right_card.grid_rowconfigure(0, weight=1)
        right_card.grid_columnconfigure(0, weight=1)

        login = Image.open(login_bg)
        self.login_img = customtkinter.CTkImage(light_image= login, size=(1,1))

        right_bg = customtkinter.CTkLabel(right_card, image=self.login_img, text="")
        right_bg.grid(row=0, column=0, sticky="nsew")

        def resize_bg(event):
            self.login_img.configure(size=(event.width,event.height))
        right_card.bind("<Configure>", resize_bg)
    def handle_login(self):

        global CURRENT_USER_EMAIL, CURRENT_USER_PASSWORD, CURRENT_USER_ID, CURRENT_DISPLAY_NAME
        email_value = self.email_input.get()
        password_value = self.pass_input.get()

        conn = sqlite3.connect('cointravert.db')
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT * FROM users WHERE email = ? AND password = ?
            ''', (email_value, password_value)
        )
        user = cursor.fetchone()
        conn.close()


        if email_value == "" or password_value == "":
            self.login_message.configure(text="Please enter email and password.", text_color="red")
            return

        elif user is None:
            self.login_message.configure(text="User not registered.", text_color="red")
        
        else:
            CURRENT_USER_ID = user[0]
            CURRENT_USER_EMAIL = user[1]
            CURRENT_USER_PASSWORD = user[2]
            CURRENT_DISPLAY_NAME = user[3]

            self.login_message.configure(text="Login successful!", text_color="light green")
            pos = (self.winfo_x(), self.winfo_y())
            self.destroy()
            Converter(prevent_redun_page="Converter", position=pos).mainloop()

    def portal_signup(self):
        pos = (self.winfo_x(), self.winfo_y())
        self.destroy()
        SignUp(position=pos).mainloop()
    def go_to_converter(self):
        pos = (self.winfo_x(), self.winfo_y())
        self.destroy()
        Converter(prevent_redun_page="Converter", position=pos).mainloop()

class CoinTra(customtkinter.CTk):
    def __init__(self,prevent_redun_page="", position=None):
        super().__init__()
        self.prevent_redun_page = prevent_redun_page
        self.position = position
        self.header_setup()

    def header_setup(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        setting_icon_path = os.path.join(base_dir, "setting.png")
        user_icon_path = os.path.join(base_dir, "user.png")
        logo_path = os.path.join(base_dir, "cv-logo.png")

        setting_icon = customtkinter.CTkImage(
            light_image=Image.open(setting_icon_path),
            size=(20, 20)
        )
        user_icon = customtkinter.CTkImage(
            light_image=Image.open(user_icon_path),
            size=(20, 20)
        )
        logo = customtkinter.CTkImage(
            light_image=Image.open(logo_path),
            size=(32, 32)
        )

        top_nav = customtkinter.CTkFrame(self, corner_radius=20)
        top_nav.pack(fill="x", pady=5, padx=10)

        left_nav = customtkinter.CTkFrame(top_nav, fg_color="transparent")
        left_nav.pack(side="left", padx=15)

        logo_lbl = customtkinter.CTkLabel(left_nav, image=logo, text="")
        logo_lbl.pack(side="left")

        app_name = customtkinter.CTkLabel(
            left_nav,
            text="CoinTraVert",
            font=("Arial", 16, "bold")
        )
        app_name.pack(side="left", padx=10)

        right_nav = customtkinter.CTkFrame(top_nav, fg_color="transparent")
        right_nav.pack(side="right", pady=5, padx=10)
        converter_btn = customtkinter.CTkButton(
            right_nav,
            text="Converter",
            command=self.portal_converter,
            fg_color="medium slate blue",
            height=32,
            border_width=2,
            border_color="white",
            corner_radius=20,
            font=("Arial", 16, "bold"),
        )
        converter_btn.pack(side="left", padx=5)

        audit_btn = customtkinter.CTkButton(
            right_nav,
            text="Audit",
            command=self.portal_audit,
            fg_color="medium slate blue",
            height=32,
            border_width=2,
            border_color="white",
            corner_radius=20,
            font=("Arial", 16, "bold"),
        )
        audit_btn.pack(side="left", padx=5)

        settings_btn = customtkinter.CTkButton(
            right_nav,
            image=setting_icon,
            text="Settings",
            command=self.portal_settings,
            fg_color="medium slate blue",
            height=32,
            border_width=2,
            border_color="white",
            corner_radius=20,
            font=("Arial", 16, "bold"),
        )
        settings_btn.pack(side="left", padx=5)

        user_btn = customtkinter.CTkButton(
            right_nav,
            image=user_icon,
            fg_color="medium slate blue",
            height=32,
            text="User",
            compound="left",
            border_width=2,
            border_color="white",
            width=32,
            corner_radius=16,
            font=("Arial", 16, "bold"),
        )
        user_btn.pack(side="left", padx=5)
        user_btn.configure(command=self.portal_settings)
    def portal_converter(self):
        if self.prevent_redun_page == "Converter":
            return
        pos = (self.winfo_x(), self.winfo_y())
        self.destroy()
        Converter(prevent_redun_page = "Converter", position=pos).mainloop()

    def portal_audit(self):
        if self.prevent_redun_page == "Audit":
            return
        pos = (self.winfo_x(), self.winfo_y())
        self.destroy()
        Audit(prevent_redun_page = "Audit", position=pos).mainloop()
    def portal_settings(self):
        if self.prevent_redun_page == "Settings":
            return
        pos = (self.winfo_x(), self.winfo_y())
        self.destroy()
        Settings(prevent_redun_page = "Settings", position=pos).mainloop()


class ScrollableDropdown(customtkinter.CTkFrame):
    def __init__(self, master, values, command=None, width=150, height=35):
        super().__init__(master)

        self.command = command
        self.all_values = values[:]    # full list
        self.filtered_values = values[:]  # filtered list for search

        self.button = customtkinter.CTkButton(
            self,
            text="Select",
            width=width,
            height=height,
            corner_radius=8,
            fg_color="#DDDDDD",
            text_color="black",
            command=self.open_menu
        )
        self.button.pack(fill="both")

        self.menu_window = None
        self.clicked_inside_dropdown = False

    def open_menu(self):
        if self.menu_window:
            self.menu_window.destroy()

        self.menu_window = customtkinter.CTkToplevel(self)
        self.menu_window.overrideredirect(True)
        self.menu_window.attributes("-topmost", True)
        self.menu_window.configure(fg_color="white")

        # position under button
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.button.winfo_height()
        self.menu_window.geometry(f"220x260+{x}+{y}")

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda var, index, mode: self.update_filter())

        search_entry = customtkinter.CTkEntry(
            self.menu_window,
            height=35,
            placeholder_text="Search...",
            textvariable=self.search_var,
            fg_color="white",
            text_color="black",
            placeholder_text_color="#666666",
            border_color="#AAAAAA"
        )
        search_entry.pack(fill="x", padx=8, pady=(8, 4))


        self.frame = customtkinter.CTkScrollableFrame(
            self.menu_window,
            width=220,
            height=210,
            fg_color="honeydew2"
        )
        self.frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.populate_items()


        self.winfo_toplevel().bind("<Button-1>", self.global_click_handler, add="+")

    def populate_items(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        for value in self.filtered_values:
            item = customtkinter.CTkButton(
                self.frame,
                text=value,
                anchor="w",
                fg_color="transparent",
                text_color="black",
                hover_color="#DDDDDD",
                command=lambda v=value: self.select(v),
                hover= False
            )
            item.pack(fill="x", pady=2, padx=5)

    def update_filter(self, *args):
        query = self.search_var.get().lower()
        self.filtered_values = [
            v for v in self.all_values if query in v.lower()
        ]
        self.populate_items()

    def global_click_handler(self, event):
        if not self.menu_window:
            return

        x, y = event.x_root, event.y_root

        # dropdown window boundaries
        left = self.menu_window.winfo_rootx()
        top = self.menu_window.winfo_rooty()
        right = left + self.menu_window.winfo_width()
        bottom = top + self.menu_window.winfo_height()

        inside = (left <= x <= right) and (top <= y <= bottom)

        if not inside:
            self.menu_window.destroy()
            self.menu_window = None
            self.winfo_toplevel().unbind("<Button-1>")

    def select(self, value):
        self.button.configure(text=value)
        if self.command:
            self.command(value)

        if self.menu_window:
            self.menu_window.destroy()
            self.menu_window = None
            self.winfo_toplevel().unbind("<Button-1>")

    def set(self, value):
        self.button.configure(text=value)

    def get(self):
        return self.button.cget("text")

class Converter(CoinTra):
    def __init__(self,prevent_redun_page="", position=None):
        super().__init__(prevent_redun_page=prevent_redun_page, position=position)

        #JSON FILE (laman yung mga characteristics ng bawat currency)
        with open("currency_spec.json", "r", encoding="utf-8") as file:
            self.currency_info = json.load(file)

        #APIS
        self.api_url = "https://v6.exchangerate-api.com/v6/46635d180412d92eeadcfa25/latest/USD"

        if position:
            self.geometry(f"1280x800+{position[0]}+{position[1]}")
        else:
            self.geometry("1280x800")
        self.resizable(False, False)
        self.title("Converter")

        main_card = customtkinter.CTkFrame(self,corner_radius=30)
        main_card.pack(fill="x", pady=20, padx=20)

        main_card.grid_columnconfigure(0, weight=1)
        main_card.grid_columnconfigure(1, weight=1)

        left_card = customtkinter.CTkFrame(
            main_card,
            width=600,
            height=280,
            corner_radius=20,
            fg_color="white"
        )
        left_card.grid(row=0, column=0, columnspan=2, pady=10)
        left_card.grid_columnconfigure((0,1,2), weight=1)
        left_card.grid_propagate(False)

        def update_left(choice):
            info = self.currency_info[choice]
            left_flag.configure(fg_color=info["color"])
            left_code.configure(text=choice)
            left_name.configure(text=info["name"])

        def update_right(choice):
            info = self.currency_info[choice]
            right_flag.configure(fg_color=info["color"])
            right_code.configure(text=choice)
            right_name.configure(text=info["name"])

        left_top_box = customtkinter.CTkFrame(left_card, fg_color="#E5E5E5", corner_radius=12, width=10)
        left_top_box.grid(row=0, column=0, padx=20, pady=(20,10), sticky="ew")
        left_top_box.grid_propagate(False)

        left_flag = customtkinter.CTkFrame(left_top_box, width=35, height=22, corner_radius=4, fg_color="#d9534f")
        left_flag.pack(side="left", padx=10, pady=10)

        left_code = customtkinter.CTkLabel(left_top_box, text="USD", font=("Arial", 16, "bold"))
        left_code.pack(side="left")

        left_name = customtkinter.CTkLabel(left_top_box, text="US Dollar", font=("Arial", 14), text_color="#333")
        left_name.pack(side="left", padx=5)

        right_top_box = customtkinter.CTkFrame(left_card, fg_color="#E5E5E5", corner_radius=12, width=20)
        right_top_box.grid(row=0, column=2, padx=20, pady=(20,10), sticky="ew")
        right_top_box.grid_propagate(False)

        right_flag = customtkinter.CTkFrame(right_top_box, width=35, height=22, corner_radius=4, fg_color="#0275d8")
        right_flag.pack(side="left", padx=10, pady=10)

        right_code = customtkinter.CTkLabel(right_top_box, text="PHP", font=("Arial", 16, "bold"))
        right_code.pack(side="left")

        right_name = customtkinter.CTkLabel(right_top_box, text="Philippine Peso", font=("Arial", 14), text_color="#333")
        right_name.pack(side="left", padx=5)

        input_contain = customtkinter.CTkEntry(left_card, placeholder_text="Enter amount", height=60, corner_radius=10)
        input_contain.grid(row=1, column=0, padx=(20,10), pady=10, sticky="ew")

        swap_icon = customtkinter.CTkButton(left_card, text="🔁", text_color="green", font=("Arial", 26), width=10, fg_color="transparent", command=self.swap_currencies)
        swap_icon.grid(row=1, column=1, pady=10)

        output_box = customtkinter.CTkEntry(left_card, placeholder_text="", height=60, corner_radius=10, state="readonly")
        output_box.grid(row=1, column=2, padx=(10,20), pady=10, sticky="ew")

        left_dropdown = ScrollableDropdown(
            left_card,
            values=list(self.currency_info.keys()),
            command=update_left,
            width=180
        )
        left_dropdown.set("USD")
        left_dropdown.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")

        right_dropdown = ScrollableDropdown(
            left_card,
            values=list(self.currency_info.keys()),
            command=update_right,
            width=180
        )
        right_dropdown.set("PHP")
        right_dropdown.grid(row=2, column=2, padx=20, pady=(0, 20), sticky="ew")

        #API USAGE. EXCHANGE RATE API.
        def perform_conversion():
            try:
                from_curr = left_dropdown.get()
                to_curr = right_dropdown.get()
                amount = float(input_contain.get())
                
                m_response = requests.get(self.api_url)
                print(f"RESPONSE = {m_response}")
                m_data = m_response.json()
                print("REQUEST:")
                print(m_data)
                m_rates = m_data.get("conversion_rates", {})
                
                if from_curr == "USD":
                    converted = amount * rates.get(to_curr, 1)
                else:
                    usd_amount = amount / rates.get(from_curr, 1)
                    converted = usd_amount * rates.get(to_curr, 1)
                
                output_box.configure(state="normal")
                output_box.delete(0, "end")
                output_box.insert(0, f"{converted:.4f}")
                output_box.configure(state="readonly")
                
                conn = sqlite3.connect('cointravert.db')
                cursor = conn.cursor()
                timestamp = datetime.now().strftime("%d %b %Y\n%H:%M")
                cursor.execute('''
                    INSERT INTO conversions (user_id, from_currency, to_currency, amount, converted_amount, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (CURRENT_USER_ID, from_curr, to_curr, amount, converted, timestamp))
                conn.commit()
                conn.close()
            except ValueError:
                output_box.configure(state="normal")
                output_box.delete(0, "end")
                output_box.insert(0, "Invalid amount")
                output_box.configure(state="readonly")
            except Exception as e:
                output_box.configure(state="normal")
                output_box.delete(0, "end")
                output_box.insert(0, "Error")
                output_box.configure(state="readonly")

        convert_btn = customtkinter.CTkButton(
            left_card,
            text="CONVERT",
            width=200,
            height=50,
            corner_radius=12,
            font=("Arial", 18, "bold"),
            command=perform_conversion
        )
        convert_btn.grid(row=3, column=0, columnspan=3, pady=(0, 25))

        self.left_dropDown = left_dropdown
        self.right_dropDown = right_dropdown
        self.inputContain = input_contain
        self.outputBox = output_box

        other_currency_container = customtkinter.CTkFrame(self, corner_radius=20)
        other_currency_container.pack(pady=10, padx=20, fill="both", expand=True)

        customtkinter.CTkLabel(
            other_currency_container,
            text="Philippine Peso Conversion Rate Around The World",
            font=("Arial", 22, "bold")
        ).pack(pady=10)

        other_currency_scroll = customtkinter.CTkScrollableFrame(
            other_currency_container,
            corner_radius=15,
            width=1100,
            height=300
        )
        other_currency_scroll.pack(fill="both", padx=10, pady=(0, 10), expand=True)

        def create_currency_row(parent, code, name, color, rate):
            row = customtkinter.CTkFrame(parent)
            row.pack(pady=5, fill="x", padx=10)

            flag_box = customtkinter.CTkFrame(row, width=40, height=25, fg_color=color, corner_radius=5)
            flag_box.pack(side="left", padx=10)

            customtkinter.CTkLabel(row, text=f"{code} - {name}", font=("Arial", 16)).pack(side="left", padx=10)
            customtkinter.CTkLabel(row, text=f"1 PHP = {rate:.4f} {code}", font=("Arial", 14), text_color="gray").pack(side="right", padx=10)

        try:
            response = requests.get(self.api_url)
            data = response.json()
            rates = data.get("conversion_rates", {})
            php_rate = rates.get("PHP", 1)
            
            for code, info in self.currency_info.items():
                if code == "PHP":
                    rate = 1.0
                else:
                    currency_rate = rates.get(code, 1)
                    rate = currency_rate / php_rate
                create_currency_row(other_currency_scroll, code, info["name"], info["color"], rate)
        except Exception as e:
            for code, info in self.currency_info.items():
                create_currency_row(other_currency_scroll, code, info["name"], info["color"], 0.0)

    def swap_currencies(self):
        left_val = self.left_dropDown.get()
        right_val = self.right_dropDown.get()
        self.left_dropDown.set(right_val)
        self.right_dropDown.set(left_val)
        self.inputContain.delete(0, "end")
        self.outputBox.configure(state="normal")
        self.outputBox.delete(0, "end")
        self.outputBox.configure(state="readonly")

class Audit(CoinTra):
    def __init__(self,prevent_redun_page="", position=None):
        super().__init__(prevent_redun_page=prevent_redun_page, position=position)

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        if position:
            self.geometry(f"1280x800+{position[0]}+{position[1]}")
        else:
            self.geometry("1280x800")
        self.resizable(False, False)
        self.title("Audit")

        with open("currency_spec.json", "r", encoding="utf-8") as f:
            flag_colors = json.load(f)

        main = customtkinter.CTkFrame(self, corner_radius=20, fg_color="light slate blue")
        main.pack(padx=20, pady=20, fill="both", expand=True)

        header = customtkinter.CTkFrame(main, fg_color="#1a2f80")
        header.pack(fill="x", pady=(10,0), padx=20)

        for i in range(4):
            header.grid_columnconfigure(i, weight=1)
        labels = ["Country","Currency","Amount","Timestamp"]
        for col, text in enumerate(labels):
            customtkinter.CTkLabel(header, text=text, font=("Segoe UI", 16, "bold")).grid(row=0, column=col, pady=15)

        scroll = customtkinter.CTkScrollableFrame(main, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=10)

        scroll.grid_columnconfigure(0, weight=1)
        scroll.grid_columnconfigure(1, weight=1)
        scroll.grid_columnconfigure(2, weight=1)
        scroll.grid_columnconfigure(3, weight=1)

        def add_data(color, currency, amount, time):
            row = customtkinter.CTkFrame(scroll, fg_color="#10215c", corner_radius=20)
            row.pack(fill="x", pady=6)

            for i in range(4):
                row.grid_columnconfigure(i, weight=1)

            color_flag = customtkinter.CTkLabel(
                row,
                text="",
                fg_color=color,
                width=60,
                height=35,
                corner_radius=10
            )
            color_flag.grid(row=0, column=0, pady=10)

            customtkinter.CTkLabel(row, text=currency, font=("Segoe UI", 15, "bold")).grid(row=0, column=1)
            customtkinter.CTkLabel(row, text=amount, font=("Segoe UI", 15, "bold")).grid(row=0, column=2)
            customtkinter.CTkLabel(row, text=time, font=("Segoe UI", 15, "bold")).grid(row=0, column=3)

        conn = sqlite3.connect('cointravert.db')
        cursor = conn.cursor()
        cursor.execute('SELECT from_currency, to_currency, amount, converted_amount, timestamp FROM conversions WHERE user_id = ?', (CURRENT_USER_ID,))
        rows = cursor.fetchall()
        conn.close()

        for from_curr, to_curr, amount, converted, timestamp in rows:
            color = flag_colors.get(from_curr, {}).get("color", "#FFFFFF")
            currency_text = f"{from_curr} → {to_curr}"
            amount_text = f"{amount:.2f} → {converted:.2f}"
            add_data(color, currency_text, amount_text, timestamp)

class Settings(CoinTra):
    def __init__(self,prevent_redun_page="", position=None):
        super().__init__(prevent_redun_page=prevent_redun_page, position=position)

        if position:
            self.geometry(f"1280x800+{position[0]}+{position[1]}")
        else:
            self.geometry("1280x800")
        self.resizable(False, False)

        main_card = customtkinter.CTkFrame(
            self,
            corner_radius=15,
            fg_color="transparent"
        )
        main_card.pack(pady=10)
        left_card = customtkinter.CTkFrame(main_card, width=480, height=500, corner_radius=15)
        left_card.pack_propagate(False)
        left_card.grid(row=0, column=0, padx=(0, 20))

        right_card = customtkinter.CTkFrame(main_card, width=600, height=500, corner_radius=15)
        right_card.pack_propagate(False)
        right_card.grid(row=0, column=1)

        def clear_right():
            for widget in right_card.winfo_children():
                widget.destroy()

        def show_userprofile():
            global CURRENT_USER_EMAIL, CURRENT_DISPLAY_NAME
            clear_right()
            customtkinter.CTkLabel(
                right_card,
                text="User Profile",
                font=("Segoe UI", 28, "bold")
            ).pack(pady=(10, 20))
            profile_frme = customtkinter.CTkFrame(
                right_card,
                width=450,
                height=350,
                corner_radius=12
            )
            profile_frme.pack(padx=20, pady=10, fill="both")
            profile_frme.grid_columnconfigure(0, weight=1)
            profile_frme.grid_columnconfigure(1, weight=2)
            customtkinter.CTkLabel(
                profile_frme,
                text="Display Name",
                font=("Segoe UI", 18)
            ).grid(row=0, column=0, padx=20, pady=(25, 10), sticky="w")
            display_name_input = customtkinter.CTkEntry(
                profile_frme,
                placeholder_text=CURRENT_DISPLAY_NAME,
                height=40,
                corner_radius=8,
                font=("Segoe UI", 16)
            )
            display_name_input.grid(row=0, column=1, padx=20, pady=(25, 10), sticky="ew")
            customtkinter.CTkLabel(
                profile_frme,
                text="Email Address",
                font=("Segoe UI", 18)
            ).grid(row=1, column=0, padx=20, pady=10, sticky="w")
            email_input = customtkinter.CTkEntry(
                profile_frme,
                placeholder_text=CURRENT_USER_EMAIL,
                height=40,
                corner_radius=8,
                font=("Segoe UI", 16)
            )
            email_input.grid(row=1, column=1, padx=20, pady=10, sticky="ew")


            msg_label = customtkinter.CTkLabel(
                profile_frme,
                text="",
                font=("Segoe UI", 14),
                text_color="light green"
            )
            msg_label.grid(row=2, column=0, columnspan=2, pady=(10, 5))

            def save_profile():
                global CURRENT_DISPLAY_NAME, CURRENT_USER_EMAIL, CURRENT_USER_ID, CURRENT_USER_PASSWORD

                new_name_check = False
                new_email_check = False

                new_name = display_name_input.get()
                new_email = email_input.get()
                conn = sqlite3.connect('cointravert.db')
                cursor = conn.cursor()

                if new_name != "":
                    cursor.execute('''
                            UPDATE users 
                            SET name = ?
                            WHERE id = ?
                    ''', (new_name, CURRENT_USER_ID))
                    conn.commit()
                    new_name_check = True

                if '@' not in new_email:
                    msg_label.configure(text="Email should have @", text_color="red")
                elif new_email != "":
                    cursor.execute('''
                        SELECT * FROM users WHERE email = ?
                    ''', (new_email,))
                    email = cursor.fetchone()

                    email_exists = False
                    if email is not None:
                        email_exists = True


                    if email_exists:
                        msg_label.configure(text="Email already exists", text_color="red")
                    else:
                        cursor.execute('''
                                 UPDATE users 
                                 SET email = ?
                                 WHERE id = ?
                         ''', (new_email, CURRENT_USER_ID))
                        conn.commit()
                        new_email_check = True

                if new_name_check and new_email_check:
                    msg_label.configure(text="Name and Email updated.", text_color="light green")
                elif new_email_check:
                    msg_label.configure(text="Email updated.", text_color="light green")
                elif new_name_check:
                    msg_label.configure(text="Name updated.", text_color="light green")

                cursor.execute('''
                    SELECT * FROM users WHERE id = ?
                ''', (CURRENT_USER_ID,))
                user = cursor.fetchone()
                conn.close()

                CURRENT_USER_ID = user[0]
                CURRENT_USER_EMAIL = user[1]
                CURRENT_USER_PASSWORD = user[2]
                CURRENT_DISPLAY_NAME = user[3]

            save_btn = customtkinter.CTkButton(
                profile_frme,
                text="Save Changes",
                height=45,
                corner_radius=8,
                font=("Segoe UI", 18, "bold"),
                fg_color="medium slate blue",
                border_color="white",
                border_width=2,
                command=save_profile
            )
            save_btn.grid(row=3, column=0, columnspan=2, pady=25)

        def show_password():
            clear_right()
            customtkinter.CTkLabel(
                right_card,
                text="Password and Security",
                font=("Segoe UI", 28, "bold")
            ).pack(pady=(10, 10))

            pass_contain = customtkinter.CTkFrame(
                right_card,
                width=450,
                height=500,
                corner_radius=12
            )
            pass_contain.pack(fill="both", expand=True, padx=20, pady=10)
            pass_contain.grid_columnconfigure(0, weight=1)
            pass_contain.grid_columnconfigure(1, weight=1)

            customtkinter.CTkLabel(
                pass_contain,
                text="Your Current Password",
                font=("Segoe UI", 20, "bold")
            ).grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(20, 5))
            info = (
                "You need to enter your password\n"
                "before changing it for security reasons."
            )
            customtkinter.CTkLabel(
                pass_contain,
                text=info,
                justify="left",
                font=("Segoe UI", 16)
            ).grid(row=1, column=0, sticky="nw", padx=20, pady=5)
            customtkinter.CTkLabel(
                pass_contain,
                text="Current Password",
                font=("Segoe UI", 16)
            ).grid(row=1, column=1, sticky="w", padx=20)
            current_pass_entry = customtkinter.CTkEntry(
                pass_contain,
                height=40,
                show="*",
                placeholder_text="Enter your Current Password",
            )
            current_pass_entry.grid(row=2, column=1, sticky="ew", padx=20)
            divider = customtkinter.CTkFrame(pass_contain, height=2, fg_color="#444")
            divider.grid(row=3, columnspan=2, column=0, sticky="ew", pady=25, padx=20)
            customtkinter.CTkLabel(
                pass_contain,
                text="Change your Password",
                font=("Segoe UI", 16)
            ).grid(row=4, column=0, columnspan=2, sticky="w", padx=20)
            customtkinter.CTkLabel(
                pass_contain,
                text="New Password",
                font=("Segoe UI", 16)
            ).grid(row=5, column=0, sticky="w", padx=20)
            new_pass_entry = customtkinter.CTkEntry(
                pass_contain,
                height=40,
                show="*",
                placeholder_text="Enter your New Password",
            )
            new_pass_entry.grid(row=5, column=1, sticky="ew", padx=20)
            customtkinter.CTkLabel(
                pass_contain,
                text="Confirm New Password",
                font=("Segoe UI", 16)
            ).grid(row=6, column=0, sticky="w", padx=20, pady=15)
            confirm_pass_entry = customtkinter.CTkEntry(
                pass_contain,
                height=40,
                show="*",
                placeholder_text="Re-enter new password."
            )
            confirm_pass_entry.grid(row=6, column=1, sticky="ew", padx=20)

            msg_label = customtkinter.CTkLabel(
                pass_contain,
                text="",
                font=("Segoe UI", 14),
                text_color="light green"
            )
            msg_label.grid(row=7, column=0, columnspan=2, pady=(10, 5))

            def update_password():
                """Very simple password update using == comparisons."""
                global CURRENT_USER_PASSWORD

                current_val = current_pass_entry.get()
                new_val = new_pass_entry.get()
                confirm_val = confirm_pass_entry.get()

                if current_val == "" or new_val == "" or confirm_val == "":
                    msg_label.configure(text="Please fill in all password fields.", text_color="red")
                    return

                elif current_val == CURRENT_USER_PASSWORD and new_val == confirm_val:

                    CURRENT_USER_PASSWORD = new_val
                    conn = sqlite3.connect('cointravert.db')
                    cursor = conn.cursor()
                    cursor.execute('''
                        UPDATE users 
                        SET password = ?
                        WHERE id = ?
                    ''', (CURRENT_USER_PASSWORD, CURRENT_USER_ID))
                    conn.commit()
                    conn.close()

                    msg_label.configure(text="Password updated.", text_color="light green")

                    current_pass_entry.delete(0, "end")
                    new_pass_entry.delete(0, "end")
                    confirm_pass_entry.delete(0, "end")
                else:
                    msg_label.configure(text="Check your current or new passwords.", text_color="red")

            update_btn = customtkinter.CTkButton(
                pass_contain,
                text="Update Password",
                font=("Segoe UI", 16, "bold"),
                fg_color="medium slate blue",
                border_color="white",
                border_width=2,
                corner_radius=10,
                width=260,
                command=update_password
            )
            update_btn.grid(row=8, column=0, columnspan=2, pady=35)
        def show_logout():
            clear_right()
            customtkinter.CTkLabel(
                right_card,
                text="Log Out",
                font=("Arial", 28, "bold")
            ).pack(pady=(10, 10))

            customtkinter.CTkLabel(
                right_card,
                text="Are you sure you want to log out?",
                font=("Arial", 20)
            ).pack(pady=(0, 20))

            btn_frame = customtkinter.CTkFrame(right_card, fg_color="transparent")
            btn_frame.pack(pady=10)

            logout_btn = customtkinter.CTkButton(
                btn_frame,
                text="Log Out",
                fg_color="crimson",
                hover_color="#b30000",
                border_width=2,
                border_color="white",
                width=180,
                height=48,
                corner_radius=10,
                font=("Arial", 18, "bold"),
                command=self._do_logout
            )
            logout_btn.grid(row=0, column=0, padx=15)

            cancel_btn = customtkinter.CTkButton(
                btn_frame,
                text="Cancel",
                fg_color="gray20",
                hover_color="#3a3a3a",
                border_width=2,
                border_color="white",
                width=180,
                height=48,
                corner_radius=10,
                font=("Arial", 18, "bold"),
                command=show_userprofile
            )
            cancel_btn.grid(row=0, column=1, padx=15)

        settings = customtkinter.CTkLabel(
            left_card,
            text="Settings",
            font=("Segoe UI", 28, "bold")
        )
        settings.pack(pady=(20, 10))
        setting_optns = [
            ("User Profile", show_userprofile),
            ("Password & Security", show_password),
            ("Log Out", show_logout),
        ]
        for text, cmd, in setting_optns:
            customtkinter.CTkButton(
                left_card,
                text=text,
                command=cmd,
                width=400,
                height=55,
                font=("Segoe UI", 20, "bold"),
                anchor="w",
                fg_color="transparent",
                text_color="white"
            ).pack(pady=10, padx=20)
            show_userprofile()
    def _do_logout(self):

        global CURRENT_USER_EMAIL, CURRENT_USER_PASSWORD, CURRENT_DISPLAY_NAME, CURRENT_USER_ID
        CURRENT_USER_EMAIL = ""
        CURRENT_USER_PASSWORD = ""
        CURRENT_DISPLAY_NAME = ""
        CURRENT_USER_ID = ""

        pos = (self.winfo_x(), self.winfo_y())
        self.destroy()
        Login(position=pos).mainloop()
coinTraVert = SignUp()
coinTraVert.mainloop()