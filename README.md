███╗░░░███╗░█████╗░███╗░░██╗██╗████████╗░█████╗░██████╗░
████╗░████║██╔══██╗████╗░██║██║╚══██╔══╝██╔══██╗██╔══██╗
██╔████╔██║██║░░██║██╔██╗██║██║░░░██║░░░██║░░██║██████╔╝
██║╚██╔╝██║██║░░██║██║╚████║██║░░░██║░░░██║░░██║██╔══██╗
██║░╚═╝░██║╚█████╔╝██║░╚███║██║░░░██║░░░╚█████╔╝██║░░██║
╚═╝░░░░░╚═╝░╚════╝░╚═╝░░╚══╝╚═╝░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝

# MANET Network Intrusion Detection System

## Overview

The **MANET Network Intrusion Detection System** is a command-line simulation designed to enhance security in Mobile Ad-Hoc Networks (MANETs). MANETs are decentralized, wireless networks where nodes communicate without fixed infrastructure, making them vulnerable to intrusions like file modifications or Black Hole attacks. This system implements an **Intrusion Detection System (IDS)** that monitors file changes in node directories, encrypts alerts using a **hybrid encryption technique** (3DES for messages, RSA for key exchange), and routes them securely to an admin node for analysis.

Developed as part of a master’s thesis, the system simulates a MANET with five nodes: four monitoring nodes (`Node_X1` to `Node_X3` and an additional node) and one admin node (`ADMIN`). It uses **Object-Oriented Analysis and Design (OOAD)** with **Unified Modeling Language (UML)** for structured development and **Python 3.11.5** for implementation. The project is ideal for secure communication in dynamic, resource-constrained environments like military operations, disaster response, or IoT networks.

Watch a [video demo](https://drive.google.com/file/d/1R7bFUaqWfdxPiKw1he6C9VygCgyk9S2A/view?usp=drive_link) showcasing the system in action, including node initialization, file monitoring, and alert propagation.

## Features

- **Real-Time Monitoring**: Tracks file changes (creation, modification, deletion) in node directories using the `watchdog` library.
- **Hybrid Encryption**: Combines 3DES for efficient message encryption and RSA for secure key exchange, ensuring confidentiality.
- **Secure Alert Routing**: Encrypts and forwards alerts through intermediate nodes to the admin node via UDP sockets.
- **Color-Coded Logs**: Uses `colorama` for clear console output (green for created, yellow for modified, red for deleted).
- **Dynamic Key Management**: The `KeyManager` class generates and distributes RSA key pairs for secure communication.
- **MANET Simulation**: Simulates a five-node network with dynamic routing tables for alert propagation.
- **Email Notifications**: Sends alerts to a configured email (via `monitor_mail.py`) for critical events.
- **Dashboard Interface**: Includes a `real_dashboard.py` Textual-based GUI to visualize node activities in real time.
- **UML Design**: Incorporates class, sequence, and activity diagrams for clear system architecture (see thesis documentation).



## Project Structure

```plaintext
manet-network-intrusion-detection-system-24/
├── improved_code/                    # Directory for core IDS logic
│   └── files_monitor.py             # Implements hybrid encryption and file monitoring
├── NODE1/                           # Directory for Node_X1 monitored files
├── NODE2/                           # Directory for Node_X2 monitored files
├── NODE3/                           # Directory for Node_X3 monitored files
├── NODE4/                           # Directory for additional node monitored files
├── ADMIN/                           # Directory for admin node data
├── screenshot/                      # Directory for system output screenshots
├── Manet-master/                    # Directory for MANET simulator scripts
│   └── AdHocSim.py                  # Simulates ad-hoc network routing
├── art.txt                          # ASCII art logo for README
├── config.json                      # Configuration for email and monitored files
├── cred.txt                         # Email credentials (pickled, not shared)
├── file_intrude.py                  # Simulates file changes for testing
├── key_manager2.py                  # Manages RSA key pairs and node connections
├── main.py                          # Legacy entry point (use nodes_test.py instead)
├── manet_dashboard.py               # Simulated dashboard for node outputs
├── monitor.py                       # Utility for basic message sending
├── monitor_mail.py                  # Sends email notifications for alerts
├── node_manager.py                  # Handles admin node message processing
├── nodes.py                        # Defines node classes for report handling
├── nodes_config                     # Stores node execution commands
├── nodes_monitor.py                 # Monitors node directories for changes
├── nodes_test.py                    # Main script to run and test nodes
├── real_dashboard.py                # Real-time Textual-based GUI dashboard
├── requirements.txt                 # Lists Python dependencies
├── secure_files.py                  # Basic file monitoring logic (legacy)
├── utilities.py                     # Utility functions for logging and config
└── *.docx                           # Thesis documentation (not required for runtime)



## Prerequisites

- **Python 3.8+**: Install from [python.org](https://www.python.org/downloads/).
- **Git**: Install from [git-scm.com](https://git-scm.com/downloads).
- **Operating System**: Tested on Windows 10+; compatible with Linux/macOS with minor adjustments.
- **Network**: Nodes use `127.0.0.2` (localhost) with ports 5555–5599; ensure ports are open.
- **VS Code**: Recommended for editing monitored directories (optional).
- **Dependencies** (listed in `requirements.txt`):
  - `watchdog`: File system monitoring
  - `pycryptodome`: RSA and 3DES encryption
  - `colorama`: Colored console logs
  - `textual`: Dashboard GUI

Install dependencies:
```bash
pip install -r requirements.txt

Installation

Clone the Repository:
git clone https://github.com/AkinwandeSlim/manet-network-intrusion-detection-system-24.git
cd manet-network-intrusion-detection-system-24


Create Node Directories:
mkdir NODE1 NODE2 NODE3 NODE4 ADMIN


Configure config.json:Update with your email and monitored files:
{
    "name": "Your Name",
    "path": "thesis",
    "email": "your.email@example.com",
    "interval": 5,
    "files_to_track": ["test.txt", "test_files.txt"]
}


Secure cred.txt:Store email credentials (used by monitor_mail.py) in cred.txt using pickle format:
import pickle
with open('cred.txt', 'wb') as f:
    pickle.dump({'Email': 'your.email@example.com', 'Password': 'your-app-password'}, f)

Note: Use an app-specific password for Gmail. Do not share cred.txt.


Usage
The system runs in five command-line terminals, simulating a MANET with four monitoring nodes and one admin node. Arrange terminals in a 2x2 grid for nodes (Node_X1 to Node_X3, one additional node) and a long terminal below for the key manager.

Open Five Terminals:

Use Command Prompt, PowerShell, or VS Code integrated terminals.
Arrange four terminals in a 2x2 grid and one below.


Start the Key Manager (Terminal 5):
python key_manager2.py


Runs on 127.0.0.1:5555, managing node connections and keys.


Start Monitoring Nodes (Terminals 1–3):In separate terminals, run:
python nodes_test.py Node_X1 127.0.0.2 5559 NODE1
python nodes_test.py Node_X2 127.0.0.2 5560 NODE2
python nodes_test.py Node_X3 127.0.0.2 5561 NODE3


Start Admin Node (Terminal 4):
python nodes_test.py ADMIN 127.0.0.2 5599 ADMIN


Test Intrusion Detection:

Use VS Code to modify files in NODE1, NODE2, NODE3, or NODE4:
Create: echo. > NODE1\test.txt
Modify: echo Test >> NODE1\test.txt
Delete: del NODE1\test.txt


Observe console output:
Nodes log changes and forward encrypted alerts (cyan for forwarding).
Admin node decrypts and logs alerts (green for created, yellow for modified, red for deleted).
Email notifications may be sent (if configured).




Run the Dashboard (Optional):In a new terminal, run:
python real_dashboard.py


Displays real-time node outputs in a Textual-based GUI.


Stop the System:

Press Ctrl+C in each terminal to stop nodes and the key manager.



Demo and Screenshots

Video Demo: Watch the system in action here. It shows:

Key manager initialization
Node connections to the MANET
File change detection and alert encryption
Alert routing and admin node decryption


Screenshots (in screenshot/):

Key Manager Initialization: 
Node Connection: 
Alert Triggering: 
Admin Decryption: 
Note: Add screenshots to the screenshot/ directory and update paths if needed.



How It Works

Key Manager (key_manager2.py):

Initializes on 127.0.0.1:5555, generates RSA key pairs, and maintains a routing table.
Distributes public keys to nodes for secure communication.


Node Monitoring (files_monitor.py):

Each node (Node_X1 to Node_X3, additional node) monitors its directory using watchdog.
Detects file changes and triggers alerts (e.g., “File test.txt is modified”).


Hybrid Encryption:

3DES: Encrypts alert messages for speed.
RSA: Encrypts the 3DES key using the admin’s public key.
Alerts are JSON-encoded and sent via UDP.


Alert Routing:

Nodes forward encrypted alerts to the next node based on the routing table.
The admin node (ADMIN) receives and decrypts alerts.


Logging and Notifications:

Color-coded logs enhance readability.
Email alerts are sent via monitor_mail.py for critical events.



Research Methodology
Based on the master’s thesis, the system uses OOAD with UML:

Use Case Diagrams: Define monitoring and alerting interactions.
Class Diagrams: Structure classes like FileMonitor and KeyManager.
Sequence Diagrams: Show node-to-admin alert flow.
Activity Diagrams: Detail encryption and routing processes.

See thesis files (e.g., MANET_CHAP4 (1).docx) in the repository for details. UML diagrams are not included but can be visualized using tools like diagrams.net.
Testing
The system was tested rigorously:

Unit Testing: Validated encryption (pycryptodome), file monitoring (watchdog), and routing.
Integration Testing: Ensured node communication and alert propagation.
System Testing: Simulated intrusions by modifying files in NODE1–NODE4 using VS Code.
Scenario Testing: Created, modified, and deleted files to verify alert generation and delivery.

Use file_intrude.py to automate file change simulations:
python file_intrude.py

Challenges Addressed

Dynamic Topology: Routing tables adapt to node changes, ensuring reliable alert delivery.
Resource Constraints: 3DES minimizes computational overhead; RSA secures key exchange.
Security: Hybrid encryption prevents intermediate nodes from reading alerts.
Usability: Color-coded logs and the real_dashboard.py GUI improve monitoring.

Future Enhancements

Scalability: Support dynamic node addition/removal.
Advanced Routing: Implement protocols like AODV (inspired by Manet-master/AdHocSim.py).
Cloud Logging: Store alerts in a secure database.
ML Integration: Add anomaly detection for proactive intrusion prevention.
Cross-Platform: Enhance Linux/macOS compatibility.

Contributing
Contributions are welcome! To contribute:

Fork the repository.
Create a feature branch:git checkout -b feature/your-feature


Commit changes:git commit -m "Add your feature"


Push to your fork:git push origin feature/your-feature


Open a pull request.

Follow the coding style in files_monitor.py and include tests.
License
Licensed under the MIT License. See LICENSE for details.
Contact

Author: Akinwande Slim
GitHub: AkinwandeSlim
Email: akinwandealex95@gmail.com

Acknowledgments

Research: Inspired by MANET security studies (e.g., Sankarayanan et al., 2017).
Tools: Python, watchdog, pycryptodome, textual, and diagrams.net.
Community: Thanks to open-source contributors and the Manet-master project.


Secure your MANET with this robust IDS. Run the nodes, test intrusions, and explore the code!```
