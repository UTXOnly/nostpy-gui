# Nostpy GUI

Nostpy GUI is a relay management client built with Tkinter. It provides an interface to manage relays, enter private and public keys, and query relay allowlists. Currently this only works with [nostpy-relay](https://github.com/UTXOnly/nostpy-relay) using `kind 42021` which is an expiramental kind that only nostpy is using. However this could be compatible wit other relay implementations in the future after more testing and acceptance of the relay management event kind.

### Features

- Manage relay allowlists
- Query relay allowlists
- Delete events from a given pubkey
- Dark mode interface

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

### Troubleshooting

This package installes cleanly on Linux systems but `tkinter` is a bit finnicky on Macs and would help to run the package from a virtual environment to ensure all dependencies are met. Otherwise you might get errors like this one:

```bash
~/nostpy-gui UTXOnly/pypackagebuild*
venv ❯ nostpy-gui
Traceback (most recent call last):
  File "/opt/homebrew/bin/nostpy-gui", line 5, in <module>
    from nostpy_gui.main import main
  File "/opt/homebrew/lib/python3.10/site-packages/nostpy_gui/main.py", line 1, in <module>
    import tkinter as tk
  File "/opt/homebrew/Cellar/python@3.10/3.10.14_1/Frameworks/Python.framework/Versions/3.10/lib/python3.10/tkinter/__init__.py", line 37, in <module>
    import _tkinter # If this fails your Python may not be configured for Tk
ModuleNotFoundError: No module named '_tkinter'
```

##### Create a virtual environment:

```bash
python3 -m venv nostpy-env
source nostpy-env/bin/activate  # On Windows use `nostpy-env\Scripts\activate`
```

#### Install the required dependencies:

Install the package in your virtual environment:

```bash
pip install nostpy-gui
```

* Note you may need to deactivate and reactivate your virtual environment after installing package
  * You can run `deactivate` while in the `nostpy-env` virtual environment and then `source nostpy-env/bin/activate` to reactivate


### Contributing

If you'd like to contribute to the project, feel free to open a pull request or file an issue on the GitHub repository: https://github.com/UTXOnly/nostpy-gui

### License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
