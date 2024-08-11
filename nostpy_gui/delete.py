
import tkinter as tk
from tkinter import ttk
import asyncio
from nostpy_gui.event import Event


class DeleteEventPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.relay_url = controller.relay_url
        self.public_key = controller.public_key
        self.private_key = controller.private_key
        self.content = tk.StringVar()
        self.kind = tk.StringVar()
        self.tags = tk.StringVar(value="[]")
        self.public_key_to_mod = tk.StringVar()
        self.kind_to_mod = tk.StringVar()

        title_frame = ttk.Frame(self)
        title_frame.pack(fill="x", pady=10)
        ttk.Label(title_frame, text="Delete Events From Pubkey Page").pack()
        ttk.Button(
            title_frame,
            text="Back to Home",
            command=lambda: controller.show_frame("LandingPage"),
        ).pack()

        sidebar = ttk.Frame(self, width=300)
        sidebar.pack(side="left", fill="y", padx=10, pady=10)
        sidebar.pack_propagate(False)


        ttk.Label(sidebar, text="Pubkey to Delete").pack(pady=5)
        #ttk.Entry(sidebar, textvariable=self.public_key_to_mod).pack(pady=5)
        ttk.Entry(sidebar, textvariable=self.public_key_to_mod, width=60).pack(pady=5)

        button = ttk.Button(
            sidebar,
            text="Delete all events from pubkey",
            command=lambda: self.send_note(
                "delete_pub", self.public_key_to_mod.get()
            ),
        )
        button.pack(pady=5)

        main_content = ttk.Frame(self)
        main_content.pack(fill="both", expand=True, padx=10, pady=10)

        self.output_text = tk.Text(main_content, height=20, bg="#2E2E2E", fg="#FFFFFF")
        self.output_text.pack(pady=10, padx=30, fill="both", expand=True)

    def send_note(self, verb, obj_to_mod):
        relay_urls = [self.relay_url.get()]
        content = self.content.get()
        kind = int(42069)
        tags = [[verb, obj_to_mod]]

        event = Event(
            relays=relay_urls,
            controller=self.controller,
            output_widget=self.output_text,
        )
        asyncio.run(event.send_event(content, kind, tags))

    def clear_output(self):
        self.output_text.delete("1.0", tk.END)

    def change_text_color(self, color):
        self.output_text.config(fg=color)