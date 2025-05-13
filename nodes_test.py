

# key_manager.py
import datetime
import sys
import os
import json
import time
import socket
from threading import Thread
from files_monitor import FileMonitor
from colorama import Fore, Style, init                                  

from key_manager2 import KeyManager

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.hashes import SHA256
# Initialize colorama
init(autoreset=True)

class NodeManager:
    def __init__(self, ip, port, node_id,  directory, manet_ip, manet_port, monitor_files=True):
        self.ip = ip
        self.port = port
        self.directory = directory
        self.manet_ip = manet_ip
        self.manet_port = manet_port
        self.monitor_files = monitor_files
        self.node_manager_monitor = None
        self.connected_nodes = set()
        self.node_id=node_id

        # self.name = name
        self.rsa_private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.rsa_public_key = self.rsa_private_key.public_key()
        self.des_key = self.generate_3des_key()
        self.next_node = None
        self.target_node = None  # Added target_node attribute
   
    def start_monitoring(self, interval):
        if self.monitor_files:
            # Create the FileMonitor instance without starting MANET communication
            self.node_manager_monitor = FileMonitor(
                folderPath=self.directory,
                ip=self.ip,
                port=self.port,
                node_id=self.node_id,
                monitor_own_directory=True  
            )

            # # Start MANET communication in a separate thread
            # manet_thread = Thread(target=self.start_manet_communication)
            # manet_thread.start()

            # Start monitoring the key manager's directory
            node_manager_thread = Thread(target=self.node_manager_monitor.run, args=(interval,))
            node_manager_thread.start()
        else:
            print(Fore.YELLOW + Style.BRIGHT + "File monitoring is disabled for the node manager.")



    def generate_3des_key(self):
        return os.urandom(24)  # 24 bytes for a 192-bit key

    def rsa_encrypt(self, message, public_key):
        ciphertext = public_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=SHA256()),
                algorithm=SHA256(),
                label=None
            )
        )
        return ciphertext

    def rsa_decrypt(self, ciphertext):
        plaintext = self.rsa_private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=SHA256()),
                algorithm=SHA256(),
                label=None
            )
        )
        return plaintext

    def des_encrypt(self, message, key):
        padder = sym_padding.PKCS7(algorithms.TripleDES.block_size).padder()
        padded_message = padder.update(message) + padder.finalize()

        cipher = Cipher(algorithms.TripleDES(key), modes.ECB())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_message) + encryptor.finalize()
        return ciphertext

    def des_decrypt(self, ciphertext, key):
        cipher = Cipher(algorithms.TripleDES(key), modes.ECB())
        decryptor = cipher.decryptor()
        decrypted_padded_message = decryptor.update(ciphertext) + decryptor.finalize()

        unpadder = sym_padding.PKCS7(algorithms.TripleDES.block_size).unpadder()
        plaintext = unpadder.update(decrypted_padded_message) + unpadder.finalize()
        return plaintext

    def forward_message(self, encrypted_message,target_node=None):
        if self.next_node is not None and target_node is not None:
            print(f"{self.name} sending Encrypted  message: {encrypted_message}")
            # Forward the encrypted message to the next node
            self.next_node.receive_and_forward(encrypted_message)
        elif self.next_node is not None  :
            self.receive_and_forward(encrypted_message)
        else:
            # Decrypt the message and forward it to the target node
            decrypted_message = self.des_decrypt(encrypted_message, self.des_key)
            print(f"{self.name} received message: {decrypted_message}")
            # self.target_node.receive_and_forward(encrypted_message)

    def receive_and_forward(self, encrypted_message):
        # Forward the encrypted message to the next node
        print(f"{self.name} receive and forward message: {encrypted_message}")
        self.next_node.forward_message(encrypted_message)














if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python key_manager.py <ip> <port> <directory> <manet_ip> <manet_port>")
        sys.exit(1)

    node_id, ip, port, directory,  = sys.argv[1:5]


    manet_ip = "127.0.0.1"  # Use the loopback address for testing on the same machine
    manet_port = 5555  # Use a different port for the key manager's MANET communication




    node_manager = NodeManager(
    ip=ip,
    port=int(port),
    directory=directory,
    node_id=node_id,
    manet_ip=manet_ip,
    manet_port=int(manet_port),
    monitor_files=True,  # Set to False to disable file monitoring

)



    # Start monitoring and MANET communication
    node_manager.start_monitoring(interval=5)

    try:
        while True:
            # Send a test message every 20 seconds
            # key_manager.send_message("Hello from NodeManager!", ("127.0.0.1", 5556))
            if node_id =="ADMIN":
                print(Fore.GREEN + Style.BRIGHT + "ADMIN is waiting for messages from nodes...")
            else:
                print(Fore.GREEN + Style.BRIGHT + "Node Manager is waiting for messages from nodes...")

            time.sleep(20)

    except KeyboardInterrupt:
        # Stop the key manager monitor and MANET communication thread
        if node_manager.node_manager_monitor:
            node_manager.node_manager_monitor.observer.stop()
