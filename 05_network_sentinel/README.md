# Project 5: Network Sentinel

A network security monitoring dashboard that scans ports, monitors connections, and gives you a real-time view of your computer's network activity -- all from your browser.

---

## Prerequisites

- A laptop/PC with Windows 10 or 11
- Basic Python knowledge (variables, functions, lists, dictionaries, loops, if/else)
- Completed Project 3 (Password Fortress) recommended but not required

---

## What Is This Project About?

Every time you open a website, send a message, or stream a video, your computer is making **network connections**. Each connection uses a **port** (like a door number) and a **protocol** (like a language). This project teaches you how to **see and understand** all that network activity on your own machine.

You'll build a web dashboard with 4 features:
1. **Dashboard** -- see your IP address, hostname, and live connection stats with charts
2. **Port Scanner** -- scan any machine to find which ports (doors) are open
3. **Connection Monitor** -- see every active network connection on your computer right now
4. **Network Tools** -- ping hosts, check services, and do DNS lookups

> **Important:** This is an **educational tool**. Only scan networks and devices you own or have explicit permission to test. Unauthorized scanning is illegal.

---

## Key Networking Concepts (Read This Before the Code)

Before diving into the code, understand these 5 concepts:

### 1. IP Address
Your computer's address on the network -- like a home address for data.
- `192.168.1.5` -- your local/private IP (inside your Wi-Fi network)
- `8.8.8.8` -- Google's public IP (on the internet)
- `127.0.0.1` -- localhost (your own machine, always)

### 2. Port
A number (0-65535) that identifies a specific service on a machine. Think of IP as the building address and port as the apartment number.

| Port | Service | What It Does |
|------|---------|-------------|
| 21 | FTP | File transfers |
| 22 | SSH | Secure remote login |
| 25 | SMTP | Sending emails |
| 53 | DNS | Translating domain names to IPs |
| 80 | HTTP | Websites (unencrypted) |
| 443 | HTTPS | Websites (encrypted) |
| 3306 | MySQL | Database connections |
| 3389 | RDP | Windows remote desktop |

### 3. Protocol
The "language" computers use to talk to each other:
- **TCP** -- reliable, ordered delivery (like a phone call -- you know the other side received it)
- **UDP** -- fast but no guarantee (like shouting across a room -- faster but might get lost)

### 4. Connection States
When your computer connects to another, the connection goes through states:
- **LISTENING** -- your computer is waiting for incoming connections on this port
- **ESTABLISHED** -- active two-way connection (data is flowing)
- **TIME_WAIT** -- connection was closed but system is keeping it briefly
- **CLOSE_WAIT** -- the other side closed the connection, waiting for your side to finish

### 5. DNS (Domain Name System)
Translates human-readable names to IP addresses:
```
google.com  -->  DNS  -->  142.250.80.46
```
Without DNS, you'd have to memorize IP addresses for every website.

---

## Step-by-Step Setup

### Step 0: Check if Python is Installed

Open **Command Prompt** (search "cmd" in Start menu) and type:

```bash
python --version
```

You should see something like `Python 3.12.x`. If you get an error:
1. Download Python from [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. **IMPORTANT: Check the box "Add Python to PATH"** during installation
3. Restart your command prompt after installing

Also verify pip:

```bash
pip --version
```

If `pip` gives an error, try `python -m pip --version` instead.

### Step 1: Install VS Code (if not installed)

1. Download from [https://code.visualstudio.com/](https://code.visualstudio.com/)
2. Install with default settings
3. Open VS Code
4. Install the **Python extension**: click Extensions icon (left sidebar) > search "Python" > install the one by Microsoft

### Step 2: Open the Project Folder

1. In VS Code: **File > Open Folder** > navigate to `05_network_sentinel` folder
2. Open the terminal: **Terminal > New Terminal** (or press `` Ctrl + ` ``)
3. Make sure the terminal shows you're inside the project folder

### Step 3: Install Required Packages

Run these commands **one by one** in the VS Code terminal:

```bash
pip install streamlit
pip install plotly
pip install pandas
```

If `pip` doesn't work, try with `python -m pip` instead:
```bash
python -m pip install streamlit
python -m pip install plotly
python -m pip install pandas
```

**What each package does:**
| Package | Why We Need It |
|---------|---------------|
| `streamlit` | Turns our Python code into a web dashboard (no HTML/CSS needed) |
| `plotly` | Creates interactive charts (pie charts, bar charts for network data) |
| `pandas` | Organizes connection data into tables (DataFrames) |

**Note:** This project also uses `socket`, `threading`, `subprocess`, `platform`, `re`, and `datetime` -- but these all come **built-in with Python**. No installation needed for them.

### Step 4: Run the App

From the terminal, make sure you're inside the `05_network_sentinel` folder, then run:

```bash
streamlit run app.py
```

If that doesn't work, try:
```bash
python -m streamlit run app.py
```

This will automatically open your browser at `http://localhost:8501` with the dashboard running.

To **stop the app**: press `Ctrl+C` in the terminal.

---

## Project Files -- What Each File Does

Read the files in this order when learning:

### File 1: `scanner.py` -- The Port Scanner (Read This First)

**What it does:** Checks which ports are open on a target machine using **socket programming** and **threading**.

**Key concepts for students:**
- `socket.socket(AF_INET, SOCK_STREAM)` -- creates a TCP connection object (like dialing a phone number)
- `sock.connect_ex((host, port))` -- tries to connect to a specific port. Returns `0` if the port is open, non-zero if closed
- `sock.settimeout(1.0)` -- don't wait forever; give up after 1 second
- `threading.Thread()` -- scan multiple ports **at the same time** instead of one by one (way faster)
- `threading.Lock()` -- prevents two threads from writing to the same list at the same time

**Key functions:**
```
scan_port()        --> Check if ONE port is open on a host
scan_ports()       --> Scan common ports (20 well-known ports) using threads
scan_port_range()  --> Scan a custom range (e.g., 1-1024) in batches of 50
resolve_hostname() --> Convert "google.com" to "142.250.80.46"
get_local_ip()     --> Get your own machine's IP address
get_hostname()     --> Get your machine's name
```

**Important Python you'll learn here:**
```python
# Socket programming -- the foundation of all networking
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create TCP socket
sock.settimeout(1.0)                                        # 1 second timeout
result = sock.connect_ex(("192.168.1.1", 80))               # Try port 80
# result == 0 means OPEN, anything else means CLOSED
sock.close()                                                 # Always close!

# Threading -- doing multiple things at once
import threading

def scan_one_port(port):
    # ... scan logic ...

threads = []
for port in [80, 443, 22, 3306]:
    t = threading.Thread(target=scan_one_port, args=(port,))
    threads.append(t)
    t.start()           # Start the thread (runs in background)

for t in threads:
    t.join()             # Wait for all threads to finish

# Thread-safe list with Lock
lock = threading.Lock()
results = []

def safe_append(item):
    with lock:           # Only one thread can enter this block at a time
        results.append(item)
```

### File 2: `monitor.py` -- The Connection Monitor (Read This Second)

**What it does:** Shows all active network connections on your computer and provides network tools (ping, service check).

**Key concepts for students:**
- `subprocess.check_output()` -- runs a system command (like `netstat`) and captures its output as text
- `platform.system()` -- checks if you're on Windows, Linux, or Mac (commands differ per OS)
- Parsing text output -- splitting lines, extracting fields from command output
- `re.search()` -- using regex to find patterns in ping output

**Key functions:**
```
get_active_connections()  --> Runs "netstat -an" and parses the output into a list of dictionaries
get_connection_stats()    --> Counts TCP/UDP, states, top ports, unique IPs from the connections
ping_host()               --> Pings a host and returns if reachable + average latency
check_common_services()   --> Quick-checks 6 common services on a target host
```

**Important Python you'll learn here:**
```python
# Running system commands from Python
import subprocess

output = subprocess.check_output("netstat -an", shell=True, text=True, timeout=10)
# output is a big string with all your connections

# Parsing text line by line
lines = output.strip().split("\n")
for line in lines:
    parts = line.split()            # Split by whitespace
    if parts[0] in ("TCP", "UDP"):  # Only process connection lines
        protocol = parts[0]
        local_addr = parts[1]
        remote_addr = parts[2]
        state = parts[3]

# Platform-aware commands
import platform

if platform.system() == "Windows":
    cmd = f"ping -n 4 google.com"    # Windows uses -n for count
else:
    cmd = f"ping -c 4 google.com"    # Linux/Mac uses -c for count

# Counting with dictionaries
state_counts = {}
for connection in connections:
    state = connection["state"]
    state_counts[state] = state_counts.get(state, 0) + 1
# Result: {"ESTABLISHED": 15, "LISTENING": 8, "TIME_WAIT": 3}

# Extracting data with regex
import re
match = re.search(r"Average\s*=\s*(\d+)ms", ping_output)
if match:
    avg_time = float(match.group(1))    # Extract the number
```

### File 3: `app.py` -- The Dashboard (Read This Last)

**What it does:** The web interface using Streamlit -- creates a professional-looking network monitoring dashboard.

**Key concepts for students:**
- `st.set_page_config(layout="wide")` -- uses the full browser width (dashboard style)
- `st.tabs()` -- creates tab navigation (Dashboard, Port Scanner, Connection Monitor, Tools)
- `st.metric()` -- displays a metric card (Your IP, Hostname, Active Connections)
- `st.columns()` -- splits the page into side-by-side columns
- `st.progress()` -- shows a progress bar during port scanning
- `st.dataframe()` -- displays data as an interactive table
- `st.multiselect()` -- lets users filter by protocol or state
- `go.Pie()` and `go.Bar()` -- Plotly charts for connection states and port distribution
- `pd.DataFrame()` -- converts list of dictionaries into a table

---

## Teaching Flow (Recommended Order)

```
Step 1: Context        --> "What happens when you open google.com? Where does the data go?"
Step 2: Concepts       --> Explain IP, ports, protocols, TCP vs UDP, connection states
Step 3: Setup          --> Install packages, run the app, explore the Dashboard tab
Step 4: scanner.py     --> How sockets work, how port scanning works, why threading matters
Step 5: monitor.py     --> How netstat works, parsing system command output, platform differences
Step 6: app.py         --> How Streamlit creates the dashboard, charts, filters
Step 7: Experiment     --> Scan localhost, check your own connections, ping different hosts
Step 8: Discussion     --> "Why is unauthorized scanning illegal? What's ethical hacking?"
```

---

## How It Works (Simple Explanation)

```
=== DASHBOARD TAB ===

app.py calls scanner.py:
   - get_local_ip()    --> Your machine's IP address
   - get_hostname()    --> Your machine's name

app.py calls monitor.py:
   - get_active_connections()  --> Runs "netstat -an", parses output
   - get_connection_stats()    --> Counts TCP/UDP, states, top ports
        |
app.py displays:
   - Metric cards (IP, hostname, connection count)
   - Pie chart of connection states
   - Bar chart of top 10 local ports
   - Unique remote IP count

=== PORT SCANNER TAB ===

User enters target IP and clicks "Start Scan"
        |
scanner.py:
   - resolve_hostname() converts hostname to IP
   - Creates a thread for each port to scan
   - Each thread: socket.connect_ex() --> returns 0 if port is open
   - Threads run in parallel (50 at a time for range scans)
   - Lock ensures safe access to results list
        |
app.py shows:
   - Progress bar during scanning
   - Table of open ports with service names
   - Bar chart visualization

=== CONNECTION MONITOR TAB ===

app.py calls monitor.py:
   - Runs "netstat -an" command via subprocess
   - Parses each line: protocol, local address, remote address, state
   - Returns list of dictionaries
        |
app.py shows:
   - Filterable table (by protocol, by state)
   - Total connection count

=== TOOLS TAB ===

Ping:           subprocess runs "ping -n 4 google.com" --> parses average time
Service Check:  socket.connect_ex() on 6 common ports --> Open/Closed
DNS Lookup:     socket.gethostbyname("google.com") --> "142.250.80.46"
```

---

## Quick Reference: All Terminal Commands

```bash
# ---- First time setup (run ONCE) ----

# Check Python is installed
python --version

# Check pip is installed
pip --version

# Install required packages
pip install streamlit
pip install plotly
pip install pandas

# ---- Every time you want to run the app ----

# Navigate to project folder (if not already there)
cd 05_network_sentinel

# Start the app
streamlit run app.py

# OR if streamlit command not found:
python -m streamlit run app.py

# Stop the app: press Ctrl+C in terminal

# ---- Useful checks ----

# See all installed packages
pip list

# Check if a specific package is installed
pip show streamlit
pip show plotly
pip show pandas
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'streamlit'` | Run `pip install streamlit` |
| `ModuleNotFoundError: No module named 'plotly'` | Run `pip install plotly` |
| `ModuleNotFoundError: No module named 'pandas'` | Run `pip install pandas` |
| `streamlit: command not found` | Try `python -m streamlit run app.py` |
| `'python' is not recognized` | Python not installed or not in PATH. Reinstall Python and check "Add to PATH" |
| `pip: command not found` | Try `python -m pip install ...` instead of `pip install ...` |
| Port scanner shows no results | This is normal -- most ports are closed by default. Try scanning `127.0.0.1` (localhost) |
| Connection monitor shows empty | You may need admin/elevated privileges. Try running VS Code as Administrator |
| Ping doesn't work | Some networks block ping (ICMP). Try pinging `127.0.0.1` (always works) |
| "Permission denied" errors | Run your terminal as Administrator (right-click > "Run as administrator") |
| Browser doesn't open automatically | Manually go to `http://localhost:8501` in your browser |
| Charts not displaying | Make sure both `plotly` and `pandas` are installed |

---

## Python Concepts Used in This Project

| Concept | Where It's Used |
|---------|----------------|
| Variables & strings | IP addresses, hostnames, command strings |
| Lists | Storing open ports, connections, scan results |
| Dictionaries | Connection info (`{"protocol": "TCP", "state": "ESTABLISHED", ...}`) |
| Functions | `scan_port()`, `get_active_connections()`, `ping_host()`, etc. |
| f-strings | `f"ping -n {count} {host}"` -- building commands dynamically |
| for loops | Iterating through ports, connections, parsing lines |
| if/elif/else | Checking port states, platform detection, filtering |
| `import` | Using `socket`, `threading`, `subprocess`, `platform`, `re`, `datetime` |
| Socket programming | `socket.socket()`, `connect_ex()`, `gethostbyname()` -- the core of networking |
| Threading | `threading.Thread()`, `.start()`, `.join()`, `Lock()` -- parallel execution |
| Subprocess | `subprocess.check_output()` -- running system commands from Python |
| Regular expressions | `re.search()` -- extracting data from ping output |
| Platform detection | `platform.system()` -- Windows vs Linux command differences |
| String parsing | `.split()`, `.strip()`, `.rsplit()` -- breaking command output into fields |
| Dictionary `.get()` | `ports.get(port, 0) + 1` -- counting with default values |

**Concepts NOT needed:** Classes/OOP, APIs, file I/O, AI -- this project is pure networking + system programming.

---

## Ethical Hacking Disclaimer

This tool is built for **learning and education only**.

- **DO** scan your own computer (`127.0.0.1` / `localhost`)
- **DO** scan devices on your own home network (with permission)
- **DO NOT** scan school/college/company networks without written permission
- **DO NOT** scan random IP addresses on the internet
- **DO NOT** use this to find vulnerabilities in systems you don't own

Unauthorized port scanning is **illegal** in most countries. Ethical hackers always get **written permission** before testing any system. This project teaches you the fundamentals so you understand what security professionals do -- responsibly.

---

## What It Does
- See your computer's IP address, hostname, and all active network connections
- Scan any host for open ports (20 common ports or custom range)
- Monitor active TCP/UDP connections with filters and charts
- Ping hosts, check service availability, and perform DNS lookups
- Visualize network data with interactive pie charts and bar charts
