from tkinter import ttk


class LandingPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Welcome to the Nostpy Admin GUI").pack(pady=20)

        ttk.Label(self, text="Relay Admin Privkey Hex").pack(pady=5)
        self.private_key_entry = ttk.Entry(
            self, textvariable=self.controller.private_key, width=60
        )  # Adjust the width as needed
        self.private_key_entry.pack(pady=5)

        ttk.Label(self, text="Relay Admin Pubkey Hex").pack(pady=5)
        self.public_key_entry = ttk.Entry(
            self, textvariable=self.controller.public_key, width=60
        )  # Adjust the width as needed
        self.public_key_entry.pack(pady=5)

        ttk.Label(self, text="Relay URL").pack(pady=5)
        self.relay_url_entry = ttk.Entry(
            self, textvariable=self.controller.relay_url, width=60
        )  # Adjust the width as needed
        self.relay_url_entry.pack(pady=5)

        ttk.Button(
            self, text="Save Keys and Relay", command=self.save_keys_and_relay
        ).pack(pady=20)

        # Add a separator to divide sections
        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=10)

        ttk.Button(
            self,
            text="Manage Relay Allowlist",
            command=lambda: controller.show_frame("ManageRelayPage"),
        ).pack(pady=10)
        ttk.Button(
            self,
            text="Delete Events From Pubkey",
            command=lambda: controller.show_frame("DeleteEventPage"),
        ).pack(pady=20)
        ttk.Button(
            self,
            text="Query Relay Allowlist",
            command=lambda: controller.show_frame("QueryRelayPage"),
        ).pack(pady=20)

    def save_keys_and_relay(self):
        # Save the values in the main application (controller)
        self.controller.private_key.set(self.private_key_entry.get())
        self.controller.public_key.set(self.public_key_entry.get())
        self.controller.relay_url.set(self.relay_url_entry.get())

        # Debugging print statements
        # print("Private Key:", self.controller.private_key.get())
        # print("Public Key:", self.controller.public_key.get())
        # print("Relay URL:", self.controller.relay_url.get())