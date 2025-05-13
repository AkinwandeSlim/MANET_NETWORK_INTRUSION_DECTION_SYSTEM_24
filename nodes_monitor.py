# node_monitor.py
import sys
import datetime
import os
import json
import time
import socket
from threading import Thread
from files_monitor import FileMonitor
from colorama import Fore, Style, init

class NodeMonitor:
    def __init__(self, ip, directory, key_manager_address):
        self.ip = ip
        self.directory = directory
        self.key_manager_address = key_manager_address
        self.node_monitor = FileMonitor(folderPath=self.directory,ip=self.ip)
        self.manet_ip = self.get_local_ip()  # Use the local IP address of the machine
        self.manet_port = 5555  # Specify the desired port for MANET communication

    def get_local_ip(self):
        # Get the local IP address of the machine
        local_ip = socket.gethostbyname(socket.gethostname())
        return local_ip

    def start_manet_communication(self):
        # Set up a socket for MANET communication
        manet_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        manet_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        manet_socket.bind((self.ip, self.manet_port))

        print(Fore.GREEN + Style.BRIGHT + f"This node is waiting for messages on {self.manet_ip}:{self.manet_port}...")

        while True:
            data, address = manet_socket.recvfrom(1024)
            message = data.decode("utf-8")
            self.log_message(f"Received message from {address}: {message}")

            # Process the message from nodes
            self.process_node_message(message, address)

    def start_monitoring(self, interval):
        node_thread = Thread(target=self.node_monitor.run, args=(interval,))
        node_thread.start()

    def process_node_message(self, message, address):
        # Add logic to process and handle messages from nodes
        # For example, you can print the message or take other actions
        if "deleted" in message:
            print(Fore.RED + Style.BRIGHT + f"Message from {address}: {message}")
        else:
            print(Fore.YELLOW + Style.BRIGHT + f"Message from {address}: {message}")

        # Send acknowledgment message to the sender node
        acknowledgment_message = f"Acknowledgment: Message '{message}' processed successfully."
        self.send_message(acknowledgment_message, address)

    def log_message(self, message):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}] {message}")

    def send_message(self, message, destination_address):
        # Create a socket for sending messages
        sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            # Send the message to the specified address
            sender_socket.sendto(message.encode("utf-8"), destination_address)
            print(Fore.BLUE + Style.BRIGHT + f"Sent acknowledgment to {destination_address}: {message}")

        except Exception as e:
            print(Fore.RED + Style.BRIGHT + f"Failed to send acknowledgment: {e}")

        finally:
            # Close the socket
            sender_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python node_monitor.py <ip> <directory> <key_manager_ip>")
        sys.exit(1)

    node_ip = sys.argv[1]
    node_directory = sys.argv[2]
    key_manager_ip = sys.argv[3]
    key_manager_address = (key_manager_ip, 5555)

    node = NodeMonitor(ip=node_ip, directory=node_directory, key_manager_address=key_manager_address)

    # Start MANET communication in a separate thread
    node_manet_thread = Thread(target=node.start_manet_communication)
    node_manet_thread.start()

    # Start monitoring the node's directory in the main thread
    node.start_monitoring(interval=5)

    try:
        while True:
            time.sleep(10)

    except KeyboardInterrupt:
        # Stop the node monitor and MANET communication thread
        node.node_monitor.observer.stop()
        node_manet_thread.join()
