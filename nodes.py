import time
import os
from threading import Thread
from files_monitor import FileMonitor
from queue import Queue
from socket import socket, AF_INET, SOCK_DGRAM

class FileModificationReport:
    def __init__(self, timestamp, file_path, node_ip, modification_type):
        self.timestamp = timestamp
        self.file_path = file_path
        self.node_ip = node_ip
        self.modification_type = modification_type

class KeyManagerNode:
    def __init__(self, ip, directory, log_file_path):
        self.ip = ip
        self.directory = directory
        self.reports_queue = Queue()
        self.log_file_path = log_file_path

    def receive_report(self, report):
        # Process the report and acknowledge the modification
        log_message = (
            f"Received report at {report.timestamp} from Node {report.node_ip}:\n"
            f"File Path: {report.file_path}\n"
            f"Modification Type: {report.modification_type}\n"
        )
        print(log_message)
        self.log_to_file(log_message)

    def log_to_file(self, log_message):
        with open(self.log_file_path, "a") as log_file:
            log_file.write(log_message + "\n" + "-" * 30 + "\n")

    def listen_for_reports(self):
        while True:
            if not self.reports_queue.empty():
                report = self.reports_queue.get()
                self.receive_report(report)

    def run(self):
        # Start listening for reports in a separate thread
        listener_thread = Thread(target=self.listen_for_reports)
        listener_thread.start()

        try:
            # Continuously check for reports and log them
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            listener_thread.join()

def send_report(node_ip, file_path, modification_type, key_manager_ip, key_manager_port):
    report = FileModificationReport(
        timestamp=time.time(),
        file_path=file_path,
        node_ip=node_ip,
        modification_type=modification_type,
    )

    # Send the report to the key manager node using UDP
    with socket(AF_INET, SOCK_DGRAM) as client_socket:
        client_socket.sendto(str(report.__dict__).encode(), (key_manager_ip, key_manager_port))

# Test Case
if __name__ == "__main__":
    # Define MANET nodes with their directories
    nodes = [
        {"ip": "192.168.0.101", "directory": "thesis - Copy (1)"},
        {"ip": "192.168.0.102", "directory": "thesis - Copy (2)"},
        {"ip": "192.168.0.103", "directory": "thesis - Copy (3)"},
        {"ip": "192.168.0.104", "directory": "thesis - Copy (4)"},
        {"ip": "192.168.0.105", "directory": "thesis - Copy (5)"},
    ]

    # Central key manager node
    key_manager = KeyManagerNode(
        ip="192.168.0.106",
        directory="thesis - Copy (6)",
        log_file_path="key_manager_log.txt",
    )

    # Start the key manager node
    key_manager_thread = Thread(target=key_manager.run)
    key_manager_thread.start()

    try:
        # Simulate changes in the nodes' directories for 60 seconds
        simulation_duration = 60  # seconds
        start_time = time.time()

        while time.time() - start_time < simulation_duration:
            time.sleep(10)
            for node in nodes:
                # Simulate a file modification in each node's directory
                file_path = os.path.join(node["directory"], "test_file.txt")
                with open(file_path, "a") as file:
                    file.write("Simulated change")

                # Send a report to the key manager node
                send_report(node_ip=node["ip"], file_path=file_path, modification_type="Modification", key_manager_ip=key_manager.ip, key_manager_port=5555)

    except KeyboardInterrupt:
        key_manager_thread.join()
