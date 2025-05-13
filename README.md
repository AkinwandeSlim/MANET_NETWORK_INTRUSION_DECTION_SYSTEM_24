<<<<<<< HEAD
<<<<<<< HEAD
MANET Network Intrusion Detection System 24
Overview
The MANET Network Intrusion Detection System 24 is a command-line simulation designed to enhance the security of Mobile Ad-hoc Networks (MANETs) by detecting and responding to intrusion attacks, such as file modifications and deletions. Developed for a master’s thesis, it implements a hybrid encryption technique combining RSA (for key exchange) and Triple Data Encryption Standard (3DES) (for message encryption) to ensure secure communication and computational efficiency. The system monitors directories, triggers encrypted alerts for intrusions, and routes messages to an admin node for decryption and analysis, addressing threats like Black hole attacks.
Technologies Used

Programming Language: Python 3.11.5
Libraries:
PyCrypto: For RSA and 3DES encryption algorithms.
Socket: For network initialization and communication.
Colorama: For visually highlighting file intrusions (creation, deletion, modification) in test results.


Hardware Requirements:
64-bit PC
Hard drive with at least 500MB free space


Software Requirements:
Operating system: Windows 10 or later, macOS 10.12 or later, or Linux
Python 3.6 or later



Key Features

Hybrid Encryption: Integrates RSA and 3DES for secure key exchange and message encryption.
Real-Time Directory Monitoring: Detects file changes (e.g., updates, deletions) using the DirectoryMonitor class.
Intrusion Alert System: Generates encrypted alerts via the AlertMessage class when intrusions are detected.
Secure Message Routing: Transmits encrypted alerts through intermediary nodes to the admin node.
Admin Node Analysis: Decrypts and logs alert messages for traceability and future analysis.

Setup Instructions

Clone the Repository:git clone https://github.com/AkinwandeSlim/manet-network-intrusion-detection-system-24.git


Navigate to the Project Directory:cd manet-network-intrusion-detection-system-24


Install Dependencies:pip install -r requirements.txt

Ensure Python 3.6 or later is installed.
Run the Simulation:python main.py

The simulation runs in the command line, initializing the Key Manager, connecting nodes, and monitoring directories.

Demo
A video demo showcasing the simulation is available here (replace with your YouTube/Google Drive link). The video demonstrates:

Key Manager Node initialization.
Node connection to the MANET network.
Detection and encryption of alert messages.
Secure message routing and admin node decryption.

Screenshots
Below are screenshots of the simulation in action:

Initialization of Key Manager Node:
Node Connection to MANET Network:
Alert Message Triggering and Encryption:
Secure Message Routing and Admin Node Decryption:

Project Structure

main.py: Entry point for the simulation.
admin_node.py: Implements the AdminNode class for decrypting and recording messages.
manet_node.py: Implements the MANETNode class for monitoring, alerting, and encrypting.
encryption_handler.py: Handles RSA and 3DES encryption/decryption.
directory_monitor.py: Monitors directories for file changes.
alert_message.py: Generates encrypted alert messages.
file_intrude.py: Simulates file intrusions for testing.
files_monitor.py: Core file monitoring logic.
key_manager2.py: Manages RSA key pairs and distribution.
monitor.py: Additional monitoring utilities.
monitor_mail.py: Handles alert notifications.
node_manager.py: Manages node connections.
nodes.py: Defines node classes and behaviors.
nodes_monitor.py: Monitors node activities.
nodes_test.py: Contains test cases for nodes.
secure_files.py: Secures file operations.
utilities.py: Utility functions for the system.
config.json: Configuration settings for the simulation.
cred.txt: Stores credentials (ensure not to share sensitive data).
node_keys/: Directory for node-specific key files (e.g., keys_127.0.0.2_5559.json).
screenshot/: Directory for simulation screenshots.
requirements.txt: Lists Python dependencies.
dist/main.exe: Compiled executable (optional).
dist/Icon.ico: Icon for the executable.
art.txt: ASCII art for the command-line interface.
nodes_config: Node configuration settings.
Manet-master/: Directory with additional simulation scripts (e.g., AdHocSim.py).
*.docx: Thesis documentation files (e.g., MANET_CHAP4 (1).docx).

Note: Thesis documentation files (e.g., CHAPTER 1 -NEW...docx) are included but not required for running the simulation. Consider moving them to a separate folder or repository if they’re not part of the codebase.
Testing
The system underwent rigorous testing to ensure functionality, reliability, and security:

Unit Testing: Validated encryption, decryption, folder monitoring, and message routing.
Integration Testing: Confirmed seamless communication between nodes and data flow.
System Testing: Simulated intrusion scenarios to verify end-to-end performance.

See thesis documentation (e.g., MANET_CHAP4 (1).docx) for detailed test cases and results.
Contributing
Contributions are welcome! Please submit issues or pull requests to enhance the system.
License
This project is licensed under the MIT License.
=======
# manet-network-intrusion-detection-system-24
>>>>>>> d39006614780b82ecfafa69c1d88954312e9c77c
=======
# manet-network-intrusion-detection-system-24
>>>>>>> d39006614780b82ecfafa69c1d88954312e9c77c
