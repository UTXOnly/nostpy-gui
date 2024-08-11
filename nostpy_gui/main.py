import tkinter as tk
from tkinter import ttk, messagebox, colorchooser, simpledialog
from delete import DeleteEventPage
from landing import LandingPage
from manage import ManageRelayPage
from query import QueryRelayPage

class DarkModeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Nostpy Admin GUI")
        self.geometry("800x600")
        self.set_dark_mode()

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.private_key = tk.StringVar()
        self.public_key = tk.StringVar()
        self.relay_url = tk.StringVar()

        self.frames = {}
        for F in (LandingPage, ManageRelayPage, QueryRelayPage, DeleteEventPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.create_menu()
        self.show_frame("LandingPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def set_dark_mode(self):
        self.configure(bg="#2E2E2E")

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background="#2E2E2E")
        style.configure("TLabel", background="#2E2E2E", foreground="#FFFFFF")
        style.configure("TButton", background="#4D4D4D", foreground="#FFFFFF")
        style.configure(
            "TEntry",
            background="#2E2E2E",
            foreground="#FFFFFF",
            fieldbackground="#2E2E2E",
        )
        style.configure("TText", background="#2E2E2E", foreground="#FFFFFF")

        style.map(
            "TButton",
            background=[("active", "#666666")],
            foreground=[("active", "#FFFFFF")],
        )

    def create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Exit", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.quit)

        # Edit Menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Manage", menu=edit_menu)
        edit_menu.add_command(label="Clear Output", command=self.clear_output)
        edit_menu.add_command(label="Change Text Color", command=self.change_text_color)
        edit_menu.add_command(
            label="Update Keys and Relay", command=self.enter_keys_and_relay
        )

    def clear_output(self):
        for frame in self.frames.values():
            if hasattr(frame, "clear_output"):
                frame.clear_output()

    def change_text_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            for frame in self.frames.values():
                if hasattr(frame, "change_text_color"):
                    frame.change_text_color(color)

    def enter_keys_and_relay(self):
        self.private_key.set(
            simpledialog.askstring("Input", "Enter your private key:", show="*")
        )
        self.public_key.set(simpledialog.askstring("Input", "Enter your public key:"))
        self.relay_url.set(simpledialog.askstring("Input", "Enter your relay URL:"))

        # Save the values in the controller
        print("Private Key:", self.private_key.get())  # Debugging
        print("Public Key:", self.public_key.get())  # Debugging
        print("Relay URL:", self.relay_url.get())  # Debugging



def main():
    app = DarkModeApp()
    app.mainloop()


if __name__ == "__main__":
    main()

