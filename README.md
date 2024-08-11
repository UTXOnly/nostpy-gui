# Nostpy GUI

Nostpy GUI is a relay management client built with Tkinter. It provides an interface to manage relays, enter private and public keys, and query relay allowlists.

### Features

- Enter and save relay private/public keys and relay URLs.
- Manage relay allowlists.
- Query relay allowlists.
- Dark mode interface.

## Requirements

- Python 3.7 or higher

## Installation

#### Option 1: Install from PyPI

To install Nostpy GUI using pip:
```bash
pip install nostpy-gui
```
Once installed, you can start the application by simply running:
```bash
nostpy-gui
```

#### Option 2: Build and Install Locally

If you prefer to build the project locally:

1. Clone the repository:
```bash
git clone https://github.com/UTXOnly/nostpy-gui.git
cd nostpy-gui
```

2. Install dependencies:

Ensure that you have `setuptools` and `wheel` installed:
```bash
pip install setuptools wheel
```
3. Build the package:

Build the package using the following command:
```bash
python3 -m build
```
4. Install the package:

Once built, install the package locally:
```bash
pip install dist/nostpy_gui-*.whl
```
5. Run the application:

After installation, start the application:
```bash
nostpy-gui
```
## Usage

Once the application is running:

*1. Enter Keys and Relay Information:*

* Enter your relay's admin private key and public key in the designated fields
* Provide the relay URL.

*2. Save the Information:*

* Click "Save Keys and Relay" to store the entered data for the duration of the session
  * Not stored on disk for security so you will need to enter this every time you open the client

*3. Manage Relay Allowlist:*

* Use the "Manage Relay Allowlist" button to modify the allowlist for the relay
  * Can use to ban pubkeys or events (need to use pubkey hex, workign on adding `npub/nsec` support)

*4. Query Relay Allowlist:*

* Use the "Query Relay Allowlist" button to view the current allowlist for the relay

### Contributing

If you'd like to contribute to the project, feel free to open a pull request or file an issue on the GitHub repository: https://github.com/UTXOnly/nostpy-gui

### License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
