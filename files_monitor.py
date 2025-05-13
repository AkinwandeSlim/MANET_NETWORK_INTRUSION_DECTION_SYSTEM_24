import datetime
import os
import json
import base64
import time
import socket
import threading
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from colorama import Fore, Style, init
import monitor_mail
import utilities
from Crypto.Cipher import DES3
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
from Crypto.Cipher import DES3
import base64
import os





class FileMonitor:

    def __init__(self, folderPath: str,ip: str, port:str, node_id:str, filePaths: list = os.listdir(os.getcwd()), configFile: str = "config.json",
                 keyManagerAddress: tuple = ("127.0.0.1", 5555), monitor_own_directory: bool = True):


        # Configuring Path and Credentials
        self.folderPath = folderPath
        self.filePaths = filePaths
        self.emailID, self.password = monitor_mail.getCred()

        with open("config.json", "r") as f:
            self.configData = json.load(f)
            f.close()

        # MANET Configuration
        self.manet_port = 5555
        self.keyManagerAddress = keyManagerAddress

        self.ip=ip
        self.port=port
        self.acknowledgment_received = False

        # Initializing a Detector and Observer
        self.detector = FileSystemEventHandler()
        self.observer = Observer()

        # Configuring the Detector
        self.detector.on_created = self.on_created
        self.detector.on_modified = self.on_modified
        self.detector.on_deleted = self.on_deleted

        # Flag and variable to track file modification
        self.is_file_modified = False
        self.modified_file = None
        self.next_node_address=None
        self.next_node_pubKey=None

        self.node_id=node_id
        self.next_node = None 
        self.target_node=None
        self.target_pubkey=None
        self.public_key,self.private_key= self.generate_rsa_key_pair()
        self.des_key=self.generate_3des_key()
        # Scheduling the process
        self.observer.schedule(self.detector, self.folderPath, recursive=True)
        # self.connected_nodes = list()
        self.connected_nodes = set()
        self.routing_table = {}

        # Start MANET communication thread
        manet_thread = threading.Thread(target=self.start_manet_communication)
        manet_thread.start()
        self.connect_to_manet()


    def run(self, interval: int):
        utilities.displayMessage("Monitoring Started")
        self.observer.start()
        programStopped = False

        while programStopped == False:
            try:
                # Running an infinite loop to track changes every 5 seconds
                while True:
                    time.sleep(interval)
                    utilities.displayMessage("No Change Detected", style=2)

            except KeyboardInterrupt:
                # If the user presses (Ctrl + C), Monitoring is Terminated
                utilities.displayMessage("Monitoring Terminated")
                programStopped = True
                self.observer.stop()

            self.observer.join()

    def log_message(self, message):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return (f"[{current_time}] "+ Fore.CYAN + Style.BRIGHT+ f"{message}")


    def log_received_message(self, message):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return (f"[{current_time}] "+ Fore.CYAN + Style.BRIGHT+ f"{message}")


    def set_next_node(self, next_node):
        self.next_node = next_node

    def log_send_message(self, message):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}] "+ Fore.CYAN + Style.BRIGHT+ f"{message}")


    def print_routing_table(self):
        # Print the routing table for debugging or monitoring
        print("Routing Table:")
        for node_id, node_info in self.routing_table.items():
            print(f"Node {node_id} -> Next Node: {node_info['next_node_id']}")


        for nodes_key, node_value in self.routing_table.items():
            # Check if the current node is the one you are looking for
            if self.target_node is None and self.target_pubkey is None:
                # Check if "ADMIN" is in the next_node_id
                if "ADMIN" in node_value['next_node_id']:
                    # Get the admin public key
                    admin_public_key = node_value['next_node_pubKey']
                    # Now you can use admin_public_key as needed
                    
                    self.target_node="ADMIN"
                    self.target_pubkey=admin_public_key
                    print("Target Node:", self.target_node)
                    print("Admin Public Key:", self.target_pubkey)
                else:
                    print("ADMIN not found in next_node_id")

    def start_manet_communication(self):
        # Set up a socket for MANET communication
        manet_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        manet_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        manet_socket.bind((self.ip, self.port))
        # manet_socket.bind((self.manet_ip, self.manet_port))

        # print(Fore.GREEN + Style.BRIGHT + "Key Manager is waiting for messa`ges from nodes...")

        while True:
            data, address = manet_socket.recvfrom(5120)
            # print(f"Message Received From [{(address)}]")
           
            message = data.decode("utf-8")
            # self.log_message(f"Received message:{message}")

            # Process the message from nodes
            self.process_node_message(message,address)




    def process_node_message(self, message, address):

        json_data = None

        try:
            # Try to parse the message as JSON
            json_data = json.loads(message)
        except json.JSONDecodeError:
            # If it's not valid JSON, treat it as a string
            pass



        if json_data and "content_type" in json_data and json_data["content_type"] == "json":
            if "routing_table" in json_data and "message_type" in json_data and json_data["message_type"] == "routing_table_update":
                # Update the routing table and inform nodes
                self.routing_table = json_data["routing_table"]
                for nodes_key,node_value in self.routing_table.items():
                    if nodes_key==self.node_id:
                        self.next_node=node_value['next_node_id']
                        self.next_node_address=node_value['next_node_address']
                        self.next_node_pubKey=node_value['next_node_pubKey']
                        break
                print(f"Next Node ID: {self.next_node}")
                print(f"Next Node ADDRESS: {self.next_node_address}")   
                print(f"Next Node PUBLIC-KEY: {self.next_node_pubKey}")
                self.print_routing_table()

            elif "encrypted_message" in json_data and "message_type" in json_data and json_data["message_type"] == "hybrid_message":
                # Update the routing table and inform nodes
                target_node = json_data["destination_node"]
               
                if self.node_id != target_node:
                    print(Fore.CYAN + Style.BRIGHT + f"forwarding alert message to next node ......")
                    self.notify_next_node(message)
                else:   
                    # print("Adminnnn!!!!!")
                    # print({"encrypted_message":json_data['encrypted_message'],"encrypted_key":json_data['encrypted_key']})
                    self.handle_encrypted_message_content(json_data, address)

        else:
            self.handle_string_content(message, address)




    # def handle_string_content(self,message,address):
    #     # Add logic to process and handle messages from nodes
    #     # For example, you can print the message or take other actions
    #     if "File" in message and self.node_id != "ADMIN":
    #         print(Fore.CYAN + Style.BRIGHT + "Forwarding alert message to next node .....")
    #         self.notify_next_node(message)
    #         return


    #     if "deleted" in message:
    #         print(f"Message  From:{(address)}")
    #         current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #         print (f"[{current_time}] "+ Fore.RED + Style.BRIGHT+ f"{message}")
    #         # print(Fore.RED + Style.BRIGHT + self.log_message(message))

    #     elif "modified" in message:
    #         print(f"Message  From:{(address)}")
    #         # print(Fore.YELLOW + Style.BRIGHT + self.log_message(message))
    #         current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #         print (f"[{current_time}] "+ Fore.YELLOW + Style.BRIGHT+ f"{message}")

    #     # Check if the acknowledgment flag is present in the message
    #     elif "Acknowledgment" in message:
    #         # Set the acknowledgment received flag to True
    #         self.acknowledgment_received = True
    #         print(Fore.GREEN + Style.BRIGHT+"Message Delivered √√")
    #     elif "connected" in message:      
    #         print(Fore.GREEN + Style.BRIGHT+ self.log_received_message(message))
    #     else:
    #         print("  "+ self.log_message(message))



    def handle_string_content(self, message, address):
        if "File" in message and self.node_id != "ADMIN":
            print(Fore.CYAN + Style.BRIGHT + "Forwarding alert message to next node .....")
            self.notify_next_node(message)
            return

        if "deleted" in message:
            print(f"Message From: {address}")
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{current_time}] " + Fore.RED + Style.BRIGHT + f"{message}")

        elif "modified" in message:
            print(f"Message From: {address}")
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{current_time}] " + Fore.YELLOW + Style.BRIGHT + f"{message}")

        elif "created" in message:
            print(f"Message From: {address}")
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{current_time}] " + Fore.GREEN + Style.BRIGHT + f"{message}")

        elif "Acknowledgment" in message:
            self.acknowledgment_received = True
            print(Fore.GREEN + Style.BRIGHT + "Message Delivered √√")
        elif "connected" in message:
            print(Fore.GREEN + Style.BRIGHT + self.log_received_message(message))
        else:
            print("  " + self.log_message(message))









    def handle_json_content(self, message, address):

        # Extract node information from the message
        node_id = message["node_id"]
        address = message["address"]
        # pub_key = message["public_key"]
        info= message["content"]

        # Print the connection information
        print(Fore.CYAN + Style.BRIGHT + info)



    def handle_encrypted_message_content(self, message, address):
        # Extract node information from the message
        encrypted_key = message["encrypted_key"]
        encrypted_message = message["encrypted_message"]
        verify_tag=message['verify_tag']
        nonce=message["nonce"]
        private_key=self.private_key
  
        decrypted_message = self.hybrid_decryption(encrypted_key,encrypted_message,verify_tag,private_key,nonce)


        self.handle_string_content(decrypted_message,address)
        # Now you have the decrypted message and key, you can handle it as needed
        # print(f"Decrypted Message: {decrypted_message}")




    # def notify_key_manager(self, file_event,file_path,):
    #     timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    #     # print(f"{timestamp} - File Modified: {file_path}") 
    #     # Send MANET message to the key manager
    #     dest_ip,dest_port=self.next_node_address.split(":")
    #     target_node=self.target_node
    #     target_pub_key=self.target_pubkey.encode('utf-8')

    #     message=f"File {file_path} is {file_event}."
    #     encrypted_message,encrypted_key,verify_tag,nonce= self.hybrid_encryption(message, target_pub_key)
    #             # Convert bytes to string using 'utf-8' encoding


    #     hybrid_message=json.dumps({
    #                       "encrypted_message":encrypted_message,
    #                       "encrypted_key":encrypted_key,
    #                       "destination_node":target_node,
    #                       "verify_tag":verify_tag,
    #                       "nonce":nonce,
    #                       "message_type":"hybrid_message",
    #                       "content_type":"json"
    #                     })
       
    #     self.send_MANET_message(hybrid_message, dest_ip, int(dest_port), content_type="json")






    def notify_key_manager(self, file_event, file_path):
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        if self.target_pubkey is None:
            print(f"{timestamp} - Error: Target public key is not set. Cannot send {file_event} notification for {file_path}")
            return

        dest_ip, dest_port = self.next_node_address.split(":")
        target_node = self.target_node
        target_pub_key = self.target_pubkey.encode('utf-8')

        message = f"File {file_path} is {file_event}."
        encrypted_message, encrypted_key, verify_tag, nonce = self.hybrid_encryption(message, target_pub_key)

        hybrid_message = json.dumps({
            "encrypted_message": encrypted_message,
            "encrypted_key": encrypted_key,
            "destination_node": target_node,
            "verify_tag": verify_tag,
            "nonce": nonce,
            "message_type": "hybrid_message",
            "content_type": "json"
        })

        self.send_MANET_message(hybrid_message, dest_ip, int(dest_port), content_type="json")






    def notify_next_node(self,message):
        dest_ip,dest_port=self.next_node_address.split(":")
        # print(dest_ip,dest_port)
        self.send_MANET_message(message, dest_ip, int(dest_port))
 
    def handle_routing_table_update(self, routing_table):
        # Update your node's local routing table
        self.routing_table = routing_table


    def send_manet_message(self, destination_ip, message):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.sendto(json.dumps(message).encode('utf-8'), (destination_ip, self.manet_port))
        client_socket.close()


    def send_MANET_message(self, message, destination_ip, destination_port, content_type="string"):
        # Create a socket for sending messages
        sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sender_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sender_socket.bind((self.ip, self.port))
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
                sender_socket.sendto(message.encode("utf-8"), (destination_ip, destination_port))
            elif message_type == "hybrid_message":
                # Handle the public key announcement
                # self.handle_public_key_announcement(json_data)
                # print(f"Sent message to {destination_ip}:{destination_port}: {message}")
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






    def handle_manet_file_notification(self, file_path):
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        print(f"{timestamp} - MANET File Modified: {file_path}")
        # Set flags and variables to indicate file modification
        self.is_file_modified = True
        self.modified_file = file_path


    # def on_created(self, event):
    #     timestamp = datetime.datetime.now().strftime("%d-%m-%Y  %H:%M:%S")
    #     print(f"{timestamp} - File {event.event_type.title()} : {event.src_path}")



    def on_created(self, event):
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y  %H:%M:%S")
        print(f"{timestamp} - File {event.event_type.title()} : {event.src_path}")

        # Check if the event is for a file (not a directory) and if it's relevant
        if not event.is_directory and (event.event_type == "created" or event.src_path in self.filePaths or event.src_path.split(os.sep)[-1] in self.filePaths):
            # Notify key manager when a file is created
            self.notify_key_manager("created", event.src_path)













    def on_modified(self, event):
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y  %H:%M:%S")
        print(f"{timestamp} - File {event.event_type.title()}: {event.src_path}")

        if event.event_type == "modified" or (event.src_path in self.filePaths or event.src_path.split(os.sep)[-1] in self.filePaths):
            # Notify key manager when a file is modified
            self.notify_key_manager("modified",event.src_path)


    # def notify_nodes_manager(self, file_event,file_path,destination_node):
    #     timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    #     # print(f"{timestamp} - File Modified: {file_path}")
    #     Message=f"File {file_path} is {file_event}."
    #     self.des_key = self.generate_3des_key()
    #     self.target_node = "ADMIN"
    #     encrypt_message=self.des_encrypt(Message,self.des_key)
        
    #     # Send MANET message to the key manager
    #     dest_ip,dest_port=self.next_node_address.split(":")
    #     print(dest_ip,dest_port)
    #     self.send_MANET_message(f"File {file_path} is {file_event}.", dest_ip, int(dest_port))


    def on_deleted(self, event):
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y  %H:%M:%S")
        print(f"{timestamp} - File {event.event_type.title()} : {event.src_path}")
        print(event.event_type)

        if event.event_type == "deleted" or (event.src_path in self.filePaths or event.src_path.split(os.sep)[-1] in self.filePaths):
            # Notify key manager when a file is modified
            self.notify_key_manager("deleted",event.src_path)   


    def connect_to_manet(self):
        # Message to indicate that the node has connected to the network
        # message = f"{node_id} with address :{self.ip}:{self.port} is  connecting to the MANET Network"
        message=self.share_public_key()
        # Send MANET message to the key manager
        # key_manager_address = ("127.0.0.1", 5555)  # Replace with the actual KeyManager address
        self.send_MANET_message(message, self.keyManagerAddress[0], self.keyManagerAddress[1],"json")



    def share_public_key(self):


        message = json.dumps({
            "node_id":    self.node_id,
            "public_key": self.public_key.decode('utf-8'),
            "address":    f"{self.ip}:{self.port}",
            "message_type": "public_key_announcement",
            "content_type":"json",
        })

        return message




    def generate_rsa_key_pair(self):
        # Generate an RSA key pair
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        
        return public_key, private_key



    def generate_3des_key(self):
        return os.urandom(24)


    def encrypt_rsa_message(self,message, public_key):
        # message=base64.b64decode(message)
        message = base64.b64encode(message).decode('utf-8')
        # Import the recipient's public key
        recipient_key = RSA.import_key(public_key)

        # Create a cipher object using the recipient's public key
        cipher = PKCS1_OAEP.new(recipient_key)

        # Encrypt the message
        ciphertext = cipher.encrypt(message.encode('utf-8'))

        # Return the base64-encoded ciphertext
        return base64.b64encode(ciphertext).decode('utf-8')

    def decrypt_rsa_message(self,ciphertext, private_key):
        # Import the recipient's private key
        private_key = RSA.import_key(private_key)

        # Create a cipher object using the recipient's private key
        cipher = PKCS1_OAEP.new(private_key)

        # Decode the base64-encoded ciphertext and decrypt the message
        decrypted_message = cipher.decrypt(base64.b64decode(ciphertext))

        # Return the decrypted message
        return decrypted_message.decode('utf-8')



    def encrypt_3des(self,plaintext):
        # Generate a random 3DES encryption key
        key = self.des_key

        nonce = os.urandom(16)

        # Create a 3DES cipher object using the key and nonce
        cipher = DES3.new(key, DES3.MODE_EAX, nonce=nonce)

        # Convert the plaintext message to bytes
        bytes_data = bytes(plaintext, 'utf-8')

        # Encrypt the plaintext message
        ciphertext, tag = cipher.encrypt_and_digest(bytes_data)
        # Convert the ciphertext and tag to base64 for easy storage
        ciphertext_base64 = base64.b64encode(ciphertext).decode('utf-8')
        tag_base64 = base64.b64encode(tag).decode('utf-8')
        nonce=base64.b64encode(nonce).decode('utf-8')
        # print(f"cipher_nonce: {nonce}")
        return key,ciphertext_base64, tag_base64, nonce

    def decrypt_3des(self,key,ciphertext_base64,tag_base64,nonce):
        nonce=base64.b64decode(nonce)
        # Decode base64-encoded ciphertext and tag
        ciphertext = base64.b64decode(ciphertext_base64)
        tag = base64.b64decode(tag_base64)

        # Create a 3DES cipher object using the key and nonce
        cipher = DES3.new(key, DES3.MODE_EAX, nonce=nonce)

        # Decrypt the ciphertext message
        decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)

        # Convert decrypted bytes to string
        plaintext = decrypted_data.decode('utf-8')

        return plaintext



    def hybrid_encryption(self,message, public_key):
        key_4_3des,encrypted_message, tag_3des, nonce = self.encrypt_3des(message)
        encrypted_key = self.encrypt_rsa_message(key_4_3des, public_key)

        return encrypted_message,encrypted_key,tag_3des,nonce

    def hybrid_decryption(self,cipher_key,ciphertext_base64,tag_base64,private_key,nonce):

        decrypted_key = self.decrypt_rsa_message(cipher_key,private_key)

        decrypted_key=base64.b64decode(decrypted_key)

        
        decrypted_message = self.decrypt_3des(decrypted_key,ciphertext_base64,tag_base64,nonce)


        return decrypted_message




 


  