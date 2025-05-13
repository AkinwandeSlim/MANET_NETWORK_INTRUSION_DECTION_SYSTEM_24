# key_manager.py
import datetime
import os
import json
import time
import socket
from threading import Thread
from files_monitor import FileMonitor
from colorama import Fore, Style, init
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


# Initialize colorama
init(autoreset=True)

class KeyManager:
    def __init__(self,node_id,ip, directory, manet_ip, manet_port, monitor_files=True):
        self.ip = ip
        self.directory = directory
        self.manet_ip = manet_ip
        self.manet_port = manet_port
        self.monitor_files = monitor_files
        self.key_manager_monitor = FileMonitor(folderPath=self.directory,ip=self.manet_ip , port=self.manet_port) if monitor_files else None
        self.node_id=node_id
        self.connected_nodes = list()
        self.public_key,self.private_key= self.generate_rsa_key_pair()
        # self.connected_nodes = set()
    def start_manet_communication(self):
        # Set up a socket for MANET communication
        manet_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        manet_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        manet_socket.bind(("127.0.0.2", 5600))
        # manet_socket.bind((self.manet_ip, self.manet_port))

        # print(Fore.GREEN + Style.BRIGHT + "Key Manager is waiting for messages from nodes...")

        while True:
            data, address = manet_socket.recvfrom(1024)
            # print(f"Received Message From ......{(address)}")
            message = data.decode("utf-8")
            # self.log_message(f"Received message:{message}")

            # Process the message from nodes
            self.process_node_message(message, address)

    def process_node_message(self, message, address):
 
        json_data = None

        try:
            # Try to parse the message as JSON
            json_data = json.loads(message)
        except json.JSONDecodeError:
            # If it's not valid JSON, treat it as a string
            pass

        if json_data and "content_type" in json_data and json_data["content_type"] == "json":
            # Handle JSON content
            acknowledgment_message=self.handle_json_content(json_data,address)
        else:
            # Treat as a string
            acknowledgment_message=self.handle_string_content(message, address)

        destination_ip, destination_port=address
        self.send_MANET_message(acknowledgment_message, destination_ip, destination_port)

    def handle_string_content(self,message,address):
         # Add logic to process and handle messages from nodes
        # For example, you can print the message or take other actions
        acknowledgment_message=""
        if "deleted" in message:
            print(Fore.RED + Style.BRIGHT + self.log_message(message))
            # Send acknowledgment message to the sender node
            acknowledgment_message = f"Acknowledgment: Admin received  message from this node."

         
        elif "modified" in message:
            print(Fore.YELLOW + Style.BRIGHT + self.log_message(message))
            # Send acknowledgment message to the sender node
            acknowledgment_message = f"Acknowledgment: Admin node received  message from this node."
        elif "connecting" in message:
            print(Fore.CYAN + Style.BRIGHT + f"Node at {address} connected to the MANET network.")
            acknowledgment_message = f"You are now connected to the MANET network."

            # Add the connected node to the set
            self.connected_nodes.add(address)

            # Generate RSA key pair for the connected node
            public_key, private_key = self.generate_rsa_key_pair()
            # Save the keys to a file with the node's address
            self.save_keys_to_file(public_key, private_key, address)
            # Announce the new node to all connected nodes
            self.announce_new_node(address)        
        else:
            print(f"Message from {address}: {message}")
            print(self.log_message(message))


        return acknowledgment_message




    def handle_json_content(self,message,address):
        node_id=message["node_id"]
        address=message["address"]
        pubKey=message["public_key"]

        print(Fore.CYAN + Style.BRIGHT + f"{node_id} at {address} is connected to the MANET network.")
        acknowledgment_message = f"You are now connected to the MANET network."


        nodes_info={
            "node_id":message["node_id"],
            "address":message["address"],
            "public_key":message["public_key"]
        }
        # Add the connected node to the set
        self.connected_nodes.append(nodes_info)
        # self.connected_nodes.add(nodes_info)

        # # Generate RSA key pair for the connected node
        # public_key, private_key = self.generate_rsa_key_pair()
        # Save the keys to a file with the node's address
        # self.save_keys_to_file(public_key, private_key, address)
        # Announce the new node to all connected nodes
        self.announce_new_node(nodes_info)        


        return acknowledgment_message


    def announce_new_node(self, new_nodes_info):
        # print(self.connected_nodes)

        for node_info in self.connected_nodes:

            if node_info['address'] != new_nodes_info['address']:

              
                message={

                "content":f"{new_nodes_info['node_id']} is now  connected to the MANET network",
                "node_id":new_nodes_info['node_id'],
                "address":new_nodes_info['address'],
                "public_key":new_nodes_info["public_key"],
                "message_type":"node_announcement",
                "content_type":"json"
                }
                destination_ip,destination_port=node_info['address'].split(":")
                # print(f"node_info address:{nodes_ad}")
                destination_port=int(destination_port)
                self.send_MANET_message(message,destination_ip,destination_port,"json")

    def generate_rsa_key_pair(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        public_key = private_key.public_key()
        return public_key, private_key


    def save_message_to_file(self, message, address):
            # Create a folder to store messages if it doesn't exist
            folder_path = "received_messages"
            os.makedirs(folder_path, exist_ok=True)

            # Format the file name with timestamp and sender's address
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            sender_ip, sender_port = address
            file_name = f"message_{timestamp}_{sender_ip}_{sender_port}.txt"

            # Construct the full path to save the file
            file_path = os.path.join(folder_path, file_name)

            try:
                # Save the message to the file
                with open(file_path, "w") as file:
                    file.write(message)
                print(Fore.GREEN + Style.BRIGHT + f"Message saved to file: {file_path}")

            except Exception as e:
                print(Fore.RED + Style.BRIGHT + f"Failed to save message to file: {e}")


    def save_keys_to_file(self, public_key, private_key, address):
        folder_path = "node_keys"
        os.makedirs(folder_path, exist_ok=True)
        key_filename = f"keys_{address[0]}_{address[1]}.json"
        key_filepath = os.path.join(folder_path, key_filename)

        with open(key_filepath, "w") as key_file:
            serialized_public_key = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode("utf-8")
            serialized_private_key = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ).decode("utf-8")

            keys_data = {
                "public_key": serialized_public_key,
                "private_key": serialized_private_key
            }

            json.dump(keys_data, key_file)

        print(Fore.GREEN + Style.BRIGHT + f"Keys saved to file: {key_filepath}")

 
    def start_monitoring(self, interval):
        if self.monitor_files and self.key_manager_monitor:
            key_manager_thread = Thread(target=self.key_manager_monitor.run, args=(interval,))
            key_manager_thread.start()
        else:
            print(Fore.YELLOW + Style.BRIGHT + "File monitoring is disabled for the Key Manager.")

    # def log_message(self, message):
    #     current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     print(f"[{current_time}] {message}")

    def log_message(self, message):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return (f"[{current_time}] {message}")


    def connect_to_manet(self,node_id,directory):
        # Message to indicate that the node has connected to the network
        # message = f"{node_id} with address :{self.ip}:{self.port} is  connecting to the MANET Network"
        message=self.share_public_key()
        # Send MANET message to the key manager
        key_manager_address = ("127.0.0.1", 5555)  # Replace with the actual KeyManager address
        self.send_MANET_message(message, key_manager_address[0], key_manager_address[1],"json")

    def share_public_key(self):
        # Share public key with the key manager
        public_key_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        message = json.dumps({
            "node_id":    self.node_id,
            "public_key": public_key_bytes.decode("utf-8"),
            "address":f"{self.manet_ip}:{self.manet_port}",
            "message_type": "public_key_announcement",
            "content_type":"json",
        })

        return message

    def send_MANET_message(self, message, destination_ip, destination_port, content_type="string"):
        # Create a socket for sending messages
        sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sender_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sender_socket.bind((self.manet_ip, self.manet_port))
        message_type=None
        try:
            if content_type == "json":
                # Parse the JSON message to extract information
                json_data = json.loads(message)

                # Extract the message type from the JSON message
                message_type = json_data.get("message_type")



            if message_type == "public_key_announcement":
                # Handle the public key announcement
                # self.handle_public_key_announcement(json_data)
                # print(f"Sent message to {destination_ip}:{destination_port}: {message}")
                print(Fore.CYAN + Style.BRIGHT +f"Connecting to the MANET Network............")
                print(type(message))
                sender_socket.sendto(message.encode("utf-8"), (destination_ip, destination_port))


            elif "File" in message:
                # sender_socket.bind((self.manet_ip, self.manet_port))
                # Send the message to the specified address
                sender_socket.sendto(message.encode("utf-8"), (destination_ip, destination_port))
                # print(Fore.CYAN + Style.BRIGHT +f"Acknowledgment Messages sent to {destination_ip}:{destination_port}")

            else:

                # sender_socket.bind((self.manet_ip, self.manet_port))
                # Send the message to the specified address
                sender_socket.sendto(message.encode("utf-8"), (destination_ip, destination_port))
                print(Fore.CYAN + Style.BRIGHT +f"Acknowledgment Messages sent to {destination_ip}:{destination_port}")


        except Exception as e:
            print(f"Failed to send message: {e}")

        finally:
            # Close the socket
            sender_socket.close()







    def generate_rsa_key_pair(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        public_key = private_key.public_key()
        return public_key, private_key


if __name__ == "__main__":
    key_manager_config = {"ip": "192.168.1.183", "directory": "thesis - Copy (6)"}
    manet_ip = "127.0.0.2"  # Use the loopback address for testing on the same machine
    manet_port = 5600

    # Specify whether to monitor files (True by default)
    key_manager = KeyManager(
        node_id='ADMIN',
        ip=manet_ip,
        directory=key_manager_config["directory"],
        manet_ip=manet_ip,
        manet_port=manet_port,
        monitor_files=False,  # Set to False to disable file monitoring
    )

    # Start MANET communication in a separate thread
    manet_thread = Thread(target=key_manager.start_manet_communication)
    manet_thread.start()


    # key_manager.connect_to_manet("node_id",self.directory)
    # Start monitoring the key manager's directory in the main thread
    key_manager.start_monitoring(interval=5)

    try:
        while True:
            # Send a test message every 20 seconds
            # key_manager.send_MANET_message("Hello from KeyManager!", "127.0.0.1", 5556)
            print(Fore.GREEN + Style.BRIGHT + "Admin is waiting for messages from nodes...")
            time.sleep(20)

    except KeyboardInterrupt:
        # Stop the key manager monitor and MANET communication thread
        if key_manager.key_manager_monitor:
            key_manager.key_manager_monitor.observer.stop()

        # Join the key manager thread
        manet_thread.join()














