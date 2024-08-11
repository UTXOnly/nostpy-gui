
import tkinter as tk
from tkinter import ttk, messagebox, colorchooser, simpledialog
import asyncio
from event import Event

class QueryRelayPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.relay_url = controller.relay_url
        self.public_key = controller.public_key

        ttk.Label(self, text="Query Relay Page").pack(pady=20)
        ttk.Button(
            self,
            text="Back to Home",
            command=lambda: controller.show_frame("LandingPage"),
        ).pack()

        content_frame = ttk.Frame(self)
        content_frame.pack(fill="both", expand=True)

        button1 = ttk.Button(
            content_frame, text="Show Allow List", command=self.query_allow_list
        )
        button1.pack(pady=10)

        self.output_text = tk.Text(content_frame, height=10, bg="#2E2E2E", fg="#FFFFFF")
        self.output_text.pack(pady=10, fill="x", expand=True)

        style = ttk.Style()
        style.configure(
            "Treeview",
            background="#2E2E2E",
            foreground="#FFFFFF",
            fieldbackground="#2E2E2E",
            font=("Arial", 10),
        )
        style.configure(
            "Treeview.Heading",
            background="#4D4D4D",
            foreground="#FFFFFF",
            font=("Arial", 10, "bold"),
        )
        style.map("Treeview.Heading", background=[("active", "#666666")])

        self.treeview = ttk.Treeview(
            self,
            columns=("client_pub", "kind", "allowed", "mgmt_note_id"),
            show="headings",
        )
        self.treeview.heading("client_pub", text="client_pub")
        self.treeview.heading("kind", text="kind")
        self.treeview.heading("allowed", text="allowed")
        self.treeview.heading("mgmt_note_id", text="mgmt_note_id")
        self.treeview.pack(pady=10, fill="both", expand=True)

    def query_allow_list(self):
        relay_urls = [self.relay_url.get()]
        query_dict = {"kinds": [42069]}

        event = Event(
            relays=relay_urls,
            output_widget=self.output_text,
            treeview=self.treeview,
            controller=self.controller,
        )
        asyncio.run(event.query_relays(query_dict))

    def clear_output(self):
        self.output_text.delete("1.0", tk.END)
        for item in self.treeview.get_children():
            self.treeview.delete(item)

    def change_text_color(self, color):
        self.output_text.config(fg=color)
