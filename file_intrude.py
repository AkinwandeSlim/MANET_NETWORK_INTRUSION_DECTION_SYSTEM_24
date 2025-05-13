import time
import os
from threading import Thread
from files_monitor import FileMonitor

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
    key_manager = {"ip": "192.168.0.106", "directory": "thesis - Copy (6)"}

    # Start FileMonitors for each node
    monitors = []
    for node in nodes:
        monitor = FileMonitor(folderPath=node["directory"], keyManagerAddress=(key_manager["ip"], 5555))
        monitors.append(monitor)

    # Start FileMonitor for the key manager
    key_manager_monitor = FileMonitor(folderPath=key_manager["directory"])

    # Start the monitors in separate threads
    monitor_threads = [Thread(target=monitor.run, args=(5,)) for monitor in monitors]
    for thread in monitor_threads:
        thread.start()

    # Start the key manager monitor in a separate thread
    key_manager_thread = Thread(target=key_manager_monitor.run, args=(5,))
    key_manager_thread.start()

    try:
        # Simulate changes in the nodes' directories for 60 seconds
        simulation_duration = 60  # seconds
        start_time = time.time()

        while time.time() - start_time < simulation_duration:
            time.sleep(10)
            for node in nodes:
                # Simulate a file modification in each node's directory
                with open(os.path.join(node["directory"], "test_file.txt"), "a") as file:
                    file.write("Simulated change")

    except KeyboardInterrupt:
        # Stop the monitors
        for monitor in monitors:
            monitor.observer.stop()
        key_manager_monitor.observer.stop()

        # Join the threads
        for thread in monitor_threads:
            thread.join()
        key_manager_thread.join()











