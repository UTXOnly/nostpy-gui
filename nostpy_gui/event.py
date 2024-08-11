import tkinter as tk
import asyncio
import json
import secp256k1
import hashlib
import time
import websockets
import ast

class Event:
    def __init__(self, relays, controller, output_widget=None, treeview=None) -> None:
        self.relays = relays
        self.controller = controller  # Store the controller reference to access keys
        self.output_widget = output_widget
        self.treeview = treeview
        if self.output_widget:
            self.output_widget.tag_configure("color32", foreground="#20C20E")
            self.output_widget.tag_configure("color33", foreground="#FF5733")
            self.output_widget.tag_configure("color31", foreground="#FF3333")

    def print_color(self, text, color):
        if self.output_widget:
            self.output_widget.insert(tk.END, f"{text}\n", (color,))
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

    def create_event(self, content: str, kind: int, tags: list):
        public_key = self.controller.public_key.get()
        private_key_hex = self.controller.private_key.get()
        created_at = int(time.time())
        event_id = self.calc_event_id(public_key, created_at, kind, tags, content)
        signature_hex = self.sign_event_id(event_id, private_key_hex)
        try:
            self.verify_signature(event_id, public_key, signature_hex)
        except Exception as exc:
            self.print_color(f"Error verifying sig: {exc}", "color31")
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
                self.print_color(
                    f"Verification successful for event: {event_id}", "color32"
                )
                return True
            else:
                self.print_color(
                    f"Verification failed for event: {event_id}", "color31"
                )
                return False
        except (ValueError, TypeError) as e:
            self.print_color(
                f"Error verifying signature for event {event_id}: {e}", "color31"
            )
            return False

    async def send_event(self, content, kind, tags):
        try:
            event_data = self.create_event(content, kind, tags)
            for ws_relay in self.relays:
                async with websockets.connect(ws_relay) as ws:
                    event_json = ("EVENT", event_data)
                    self.print_color(f"Sending event:\n{event_json}", "color32")
                    self.print_color(f"to {ws_relay}", "color32")
                    await ws.send(json.dumps(event_json))
                    response = await asyncio.wait_for(ws.recv(), timeout=10)
                    self.print_color(
                        f"Response from {ws_relay} is :\n{response}", "color33"
                    )
        except Exception as exc:
            self.print_color(f"Error in sending event: {exc}", "color31")

    async def query_relays(self, query_dict, timeout=5):
        for relay in self.relays:
            try:
                async with websockets.connect(relay) as ws:
                    query_ws = json.dumps(("REQ", "nostpy_client", query_dict))
                    await ws.send(query_ws)
                    self.print_color(
                        f"Query sent to relay {relay}:\n{query_ws}", "color32"
                    )

                    responses_received = 0
                    start_time = time.time()
                    response_limit = query_dict.get("limit", 100)
                    response_list = []

                    while (
                        responses_received < response_limit
                        and (time.time() - start_time) < timeout
                    ):
                        try:
                            response = await asyncio.wait_for(ws.recv(), timeout=1)
                            self.print_color(
                                f"Response from {relay}:\n{response}", "color32"
                            )
                            if response[0] != "EOSE":
                                response_list.append(response)
                                responses_received += 1
                            # self.update_treeview(response_list)

                        except asyncio.TimeoutError:
                            self.print_color(
                                "No response within 1 second, continuing...", "color31"
                            )
                            break
                    self.update_treeview(response_list)
            except Exception as exc:
                self.print_color(
                    f"Exception is {str(exc)}, error querying {relay}", "color31"
                )

    def update_treeview(self, response_string):
        try:
            for item in response_string:
                if item[0] == "EOSE":
                    return
                response = ast.literal_eval(item)
                data = response[2]

                self.treeview.insert(
                    "",
                    "end",
                    values=(
                        data.get("client_pub", ""),
                        data.get("kind", ""),
                        data.get("allowed", ""),
                        data.get("note_id", "")
                        # item.get('content', '')
                    ),
                )

        except json.JSONDecodeError:
            self.print_color(f"Error decoding JSON response: {response[2]}", "color31")