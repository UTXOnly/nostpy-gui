import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
import asyncio
import json
import secp256k1
import hashlib
import time
import websockets


class Event:
    def __init__(self, relays, output_widget) -> None:
        self.relays = relays
        self.output_widget = output_widget

    def print_color(self, text, color):
        self.output_widget.insert(tk.END, f"{text}\n")
        self.output_widget.see(tk.END)  # Auto-scroll to the end

    def sign_event_id(self, event_id: str, private_key_hex: str) -> str:
        private_key = secp256k1.PrivateKey(bytes.fromhex(private_key_hex))
        sig = private_key.schnorr_sign(
            bytes.fromhex(event_id), bip340tag=None, raw=True
        )
        return sig.hex()

    def calc_event_id(
        self,
        public_key: str,
        created_at: int,
        kind_number: int,
        tags: list,
        content: str,
    ) -> str:
        data = [0, public_key, created_at, kind_number, tags, content]
        data_str = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
        return hashlib.sha256(data_str.encode("UTF-8")).hexdigest()

    def create_event(
        self, public_key: str, private_key_hex: str, content: str, kind: int, tags: list
    ):
        created_at = int(time.time())
        kind
        event_id = self.calc_event_id(public_key, created_at, kind, tags, content)
        signature_hex = self.sign_event_id(event_id, private_key_hex)
        try:
            self.verify_signature(event_id, public_key, signature_hex)
        except Exception as exc:
            self.print_color(f"Error verifying sig: {exc}", "31")
            return
        event_data = {
            "id": event_id,
            "pubkey": public_key,
            "kind": kind,
            "created_at": created_at,
            "tags": tags,
            "content": content,
            "sig": signature_hex,
        }
        return event_data

    def verify_signature(self, event_id: str, pubkey: str, sig: str) -> bool:
        try:
            pub_key = secp256k1.PublicKey(bytes.fromhex("02" + pubkey), True)
            result = pub_key.schnorr_verify(
                bytes.fromhex(event_id), bytes.fromhex(sig), None, raw=True
            )
            if result:
                self.print_color(f"Verification successful for event: {event_id}", "32")
                return True
            else:
                self.print_color(f"Verification failed for event: {event_id}", "31")
                return False
        except (ValueError, TypeError) as e:
            self.print_color(f"Error verifying signature for event {event_id}: {e}", "31")
            return False

    async def send_event(self, public_key, private_key_hex, content, kind, tags):
        try:
            event_data = self.create_event(
                public_key, private_key_hex, content, kind, tags
            )
            for ws_relay in self.relays:
                async with websockets.connect(ws_relay) as ws:
                    event_json = ("EVENT", event_data)
                    self.print_color(f"Sending event:\n{event_json}", "32")
                    self.print_color(f"to {ws_relay}", "32")
                    await ws.send(json.dumps(event_json))
                    response = await asyncio.wait_for(ws.recv(), timeout=10)
                    self.print_color(f"Response from {ws_relay} is :\n{response}", "33")
        except Exception as exc:
            self.print_color(f"Error in sending event: {exc}", "31")

    async def query_relays(self, query_dict, timeout=5):
        for relay in self.relays:
            try:
                async with websockets.connect(relay) as ws:
                    query_ws = json.dumps(("REQ", "5326483051590112", query_dict))
                    await ws.send(query_ws)
                    self.print_color(f"Query sent to relay {relay}:\n{query_ws}", "32")

                    responses_received = 0
                    start_time = time.time()
                    response_limit = query_dict.get("limit", 3)

                    while (
                        responses_received < response_limit
                        and (time.time() - start_time) < timeout
                    ):
                        try:
                            response = await asyncio.wait_for(ws.recv(), timeout=1)
                            self.print_color(f"Response from {relay}:\n{response}", "32")
                            responses_received += 1
                        except asyncio.TimeoutError:
                            self.print_color("No response within 1 second, continuing...", "31")
                            break
            except Exception as exc:
                self.print_color(f"Exception is {exc}, error querying {relay}", "31")


class DarkModeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Nostpy GUI")
        self.root.geometry("800x600")
        self.set_dark_mode()

        self.relay_url = tk.StringVar(value="wss://relay.nostpy.lol")
        self.public_key = tk.StringVar(value="5ce5b352f1ef76b1dffc5694dd5b34126137184cc9a7d78cba841c0635e17952")
        self.private_key = tk.StringVar(value="2b1e4e1f26517dda57458596760bb3bd3bd3717083763166e12983a6421abc18")
        self.content = tk.StringVar()
        self.kind = tk.StringVar(value="1")
        self.tags = tk.StringVar(value="[]")

        self.create_widgets()
        self.create_menu()

    def set_dark_mode(self):
        self.root.configure(bg='#2E2E2E')

        style = ttk.Style()
        style.theme_use('clam')

        style.configure('TFrame', background='#2E2E2E')
        style.configure('TLabel', background='#2E2E2E', foreground='#FFFFFF')
        style.configure('TButton', background='#4D4D4D', foreground='#FFFFFF')
        style.configure('TEntry', background='#2E2E2E', foreground='#FFFFFF', fieldbackground='#2E2E2E')
        style.configure('TText', background='#2E2E2E', foreground='#FFFFFF')

        style.map('TButton',
                  background=[('active', '#666666')],
                  foreground=[('active', '#FFFFFF')])

    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True)

        # Sidebar
        sidebar = ttk.Frame(main_frame, width=200)
        sidebar.pack(side='left', fill='y')
        sidebar.pack_propagate(False)

        ttk.Label(sidebar, text="Relay URL").pack(pady=5)
        ttk.Entry(sidebar, textvariable=self.relay_url).pack(pady=5)

        ttk.Label(sidebar, text="Public Key").pack(pady=5)
        ttk.Entry(sidebar, textvariable=self.public_key).pack(pady=5)

        ttk.Label(sidebar, text="Private Key").pack(pady=5)
        ttk.Entry(sidebar, textvariable=self.private_key).pack(pady=5)

        ttk.Label(sidebar, text="Content").pack(pady=5)
        ttk.Entry(sidebar, textvariable=self.content).pack(pady=5)

        ttk.Label(sidebar, text="Kind").pack(pady=5)
        ttk.Entry(sidebar, textvariable=self.kind).pack(pady=5)

        ttk.Label(sidebar, text="Tags (as JSON array)").pack(pady=5)
        ttk.Entry(sidebar, textvariable=self.tags).pack(pady=5)

        button1 = ttk.Button(sidebar, text="Send Note", command=self.send_note)
        button1.pack(pady=10)

        button2 = ttk.Button(sidebar, text="Query Relays", command=self.query_relays)
        button2.pack(pady=10)

        # Main Content
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(side='right', fill='both', expand=True)

        self.output_text = tk.Text(content_frame, height=15, bg='#2E2E2E', fg='#FFFFFF')
        self.output_text.pack(pady=10, fill='both', expand=True)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Clear Output", command=self.clear_output)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Edit Menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Change Text Color", command=self.change_text_color)

    def clear_output(self):
        self.output_text.delete('1.0', tk.END)

    def change_text_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.output_text.config(fg=color)

    def send_note(self):
        relay_urls = [self.relay_url.get()]
        public_key = self.public_key.get()
        private_key = self.private_key.get()
        content = self.content.get()
        kind = int(self.kind.get())
        tags = json.loads(self.tags.get())

        event = Event(relays=relay_urls, output_widget=self.output_text)
        asyncio.run(event.send_event(public_key, private_key, content, kind, tags))
        messagebox.showinfo("Send Note", f"Sent note: '{content}' to relay: {relay_urls}")

    def query_relays(self):
        relay_urls = [self.relay_url.get()]
        kind = int(self.kind.get())
        authors = [self.public_key.get()]
        limit = 10

        query_dict = {
            "kinds": [kind],
            "authors": authors,
            "limit": limit
        }

        event = Event(relays=relay_urls, output_widget=self.output_text)
        asyncio.run(event.query_relays(query_dict))
        messagebox.showinfo("Query Relays", "Query sent to relays")

if __name__ == "__main__":
    root = tk.Tk()
    app = DarkModeApp(root)
    root.mainloop()
