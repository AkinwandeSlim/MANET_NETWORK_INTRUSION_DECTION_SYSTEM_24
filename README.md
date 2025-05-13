Absolutely! Here's the improved `README.md` in plain text format for you to **copy and paste** directly into your GitHub README editor:

---

````markdown
```ascii
███╗░░░███╗░█████╗░███╗░░██╗██╗████████╗░█████╗░██████╗░
████╗░████║██╔══██╗████╗░██║██║╚══██╔══╝██╔══██╗██╔══██╗
██╔████╔██║██║░░██║██╔██╗██║██║░░░██║░░░██║░░██║██████╔╝
██║╚██╔╝██║██║░░██║██║╚████║██║░░░██║░░░██║░░██║██╔══██╗
██║░╚═╝░██║╚█████╔╝██║░╚███║██║░░░██║░░░╚█████╔╝██║░░██║
╚═╝░░░░░╚═╝░╚════╝░╚═╝░░╚══╝╚═╝░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝
````

# MANET Network Intrusion Detection System

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)

> ⚠️ A Python-based simulated security system that monitors file activities across MANET nodes using hybrid encryption and dynamic routing.

---

## 📌 Overview

This **Network Intrusion Detection System** (NIDS) for **Mobile Ad-Hoc Networks (MANET)** simulates real-time file event monitoring across multiple nodes and routes encrypted alerts securely to an admin node. It is tailored for volatile environments such as **military ops**, **disaster zones**, and **IoT systems**.

🎓 Developed as part of a Master's Thesis using **Python 3.11.5**.

📽️ [🎬 Watch Demo Video](https://drive.google.com/file/d/1R7bFUaqWfdxPiKw1he6C9VygCgyk9S2A/view?usp=drive_link)

---

## ✨ Features

* 📂 Real-Time File Monitoring (`watchdog`)
* 🔐 Hybrid Encryption: 3DES + RSA
* 📡 Secure Alert Routing via UDP
* 🖥️ CLI + Textual Dashboard (`real_dashboard.py`)
* 📬 Email Notifications (`monitor_mail.py`)
* 🎨 Color-coded terminal logs (create/modify/delete)
* 🔑 RSA Key Manager for key distribution
* 🧭 Routing simulation (`AdHocSim.py`)
* 🧱 UML Diagrams: Class, Sequence, Activity

---

## 📁 Project Structure

```text
manet-network-intrusion-detection-system-24/
├── improved_code/
│   └── files_monitor.py
├── NODE1/ NODE2/ NODE3/ NODE4/
├── ADMIN/
├── screenshot/
├── Manet-master/
│   └── AdHocSim.py
├── config.json
├── cred.txt
├── key_manager2.py
├── nodes_test.py
├── real_dashboard.py
├── requirements.txt
└── *.docx
```

---

## ⚙️ Prerequisites

* Python ≥ 3.8
* Git
* OS: Windows / Linux / macOS
* UDP Ports: `5555–5599` open

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🚀 Installation

1. **Clone repository**

```bash
git clone https://github.com/AkinwandeSlim/manet-network-intrusion-detection-system-24.git
cd manet-network-intrusion-detection-system-24
```

2. **Create node folders**

```bash
mkdir NODE1 NODE2 NODE3 NODE4 ADMIN
```

---

## 🛠️ Usage

1. **Start Key Manager**

```bash
python key_manager2.py
```

2. **Run Monitoring Nodes**

```bash
python nodes_test.py Node_X1 127.0.0.2 5559 NODE1
python nodes_test.py Node_X2 127.0.0.2 5560 NODE2
python nodes_test.py Node_X3 127.0.0.2 5561 NODE3
python nodes_test.py ADD_NODE 127.0.0.2 5562 NODE4
```

3. **Run Admin Node**

```bash
python nodes_test.py ADMIN 127.0.0.2 5599 ADMIN
```

4. **Simulate File Events**

```bash
echo. > NODE1/test.txt       # Create
echo Test >> NODE1/test.txt  # Modify
rm NODE1/test.txt            # Delete
```

5. **Launch Dashboard (Optional)**

```bash
python real_dashboard.py
```

---

## 🖼️ Demo & Screenshots

* 🎥 [Demo Video](https://drive.google.com/file/d/1R7bFUaqWfdxPiKw1he6C9VygCgyk9S2A/view?usp=drive_link)
* 📸 Add your screenshots under `/screenshot` folder


## 📸 Screenshots

### 1. Initial Setup
![Initial Setup](Screenshot%202025-05-12%20115229.jpg)

### 2. Dashboard View
![Dashboard](Screenshot%202025-05-12%20120008.jpg)

### 3. Node Configuration
![Node Config](Screenshot%202025-05-12%20120241.jpg)

### 4. Alert Example
![Alert Example](Screenshot%202025-05-12%20120411.jpg)

---

## ⚙️ How It Works

1. 🔑 RSA keys generated and distributed by Key Manager
2. 🖥️ Nodes monitor folders with `watchdog`
3. 🔒 Alerts encrypted (3DES + RSA)
4. 📡 Alerts routed via UDP hops
5. 📨 Admin receives, decrypts & logs alert
6. 🖥️ Visuals and emails triggered

---

## 📚 Research Methodology

* UML diagrams (Use-case, Class, Sequence, Activity)
* Object-Oriented Design Principles
* Evaluation metrics in thesis `.docx` files

---

## ✅ Testing

* Unit tests for encryption & logging
* Integration: Node routing & alerts
* Scenario-based: `file_intrude.py` file events

---

## 🧩 Challenges Addressed

* 🛰️ Dynamic topologies (routing)
* 🔐 Lightweight security (3DES+RSA)
* 📊 Real-time response with dashboard
* 💡 Usability in CLI & Textual UI

---

## 🔮 Future Enhancements

* Dynamic node join/leave
* ML-based anomaly detection
* Advanced protocols (e.g., AODV)
* Remote/cloud alert sync
* Web-based GUI

---

## 🤝 Contributing

```bash
git checkout -b feature/your-feature
git commit -m "Add <feature>"
git push origin feature/your-feature
```

Then open a Pull Request.

---

## 📄 License

This project is under the [MIT License](LICENSE).

---

## 📞 Contact

**Author:** Akinwande Slim
📧 [akinwandealex95@gmail.com](mailto:akinwandealex95@gmail.com)
🌐 [GitHub](https://github.com/AkinwandeSlim)

---

## 🙏 Acknowledgments

* Inspired by Sankarayanan et al. (2017)
* Built with: Python, watchdog, pycryptodome, textual
* UMLs via diagrams.net
* Thanks to open-source community ❤️

```

---

Let me know if you want it exported as a `.md` file or pushed to a repo for you.
```
