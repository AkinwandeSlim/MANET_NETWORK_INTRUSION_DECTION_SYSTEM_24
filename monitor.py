import socket

def send_message(message, destination_ip, destination_port):
    # Create a socket for sending messages
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Send the message to the specified address
        sender_socket.sendto(message.encode("utf-8"), (destination_ip, destination_port))
        print(f"Sent message to {destination_ip}:{destination_port}: {message}")

    except Exception as e:
        print(f"Failed to send message: {e}")

    finally:
        # Close the socket
        sender_socket.close()

if __name__ == "__main__":
    key_manager_ip = "127.0.0.1"  # Replace with the actual IP of your KeyManager node
    key_manager_port = 5555  # Make sure it matches the MANET port of your KeyManager

    message_to_send = "Hello KeyManager! This is a test message from a node."

    send_message(message_to_send, key_manager_ip, key_manager_port)




# import os
# import time
# from threading import Thread
# from queue import Queue

# class FileModificationReport:
#     def __init__(self, timestamp, file_path, node_ip, modification_type):
#         self.timestamp = timestamp
#         self.file_path = file_path
#         self.node_ip = node_ip
#         self.modification_type = modification_type

# class KeyManagerNode:
#     def __init__(self, ip, directory, log_file_path):
#         self.ip = ip
#         self.directory = directory
#         self.reports_queue = Queue()
#         self.log_file_path = log_file_path

#     def receive_report(self, report):
#         # Process the report and acknowledge the modification
#         log_message = (
#             f"Received report at {report.timestamp} from Node {report.node_ip}:\n"
#             f"File Path: {report.file_path}\n"
#             f"Modification Type: {report.modification_type}\n"
#         )
#         print(log_message)
#         self.log_to_file(log_message)

#     def log_to_file(self, log_message):
#         with open(self.log_file_path, "a") as log_file:
#             log_file.write(log_message + "\n" + "-" * 30 + "\n")

#     def listen_for_reports(self):
#         while True:
#             if not self.reports_queue.empty():
#                 report = self.reports_queue.get()
#                 self.receive_report(report)

#     def run(self):
#         # Start listening for reports in a separate thread
#         listener_thread = Thread(target=self.listen_for_reports)
#         listener_thread.start()

#         try:
#             # Continuously check for reports and log them
#             while True:
#                 time.sleep(1)

#         except KeyboardInterrupt:
#             listener_thread.join()

# # Test Case
# if __name__ == "__main__":
#     # Central key manager node
#     key_manager = KeyManagerNode(
#         ip="192.168.0.106",
#         directory="thesis - Copy (6)",
#         log_file_path="key_manager_log.txt",
#     )

#     # Start the key manager node
#     key_manager_thread = Thread(target=key_manager.run)
#     key_manager_thread.start()

#     try:
#         key_manager_thread.join()

#     except KeyboardInterrupt:
#         pass
