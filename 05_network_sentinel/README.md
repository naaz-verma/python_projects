# Project 5: Network Sentinel

A network security monitoring dashboard that scans your local network, monitors connections, and visualizes network activity in real-time.

## What It Does
- Scans local network to discover connected devices
- Monitors active network connections on your machine
- Performs port scanning on target hosts (educational)
- Visualizes network traffic and connection data
- Logs suspicious activity patterns

## How to Run
```bash
cd 05_network_sentinel
streamlit run app.py
```

## Python Concepts You'll Learn
- Socket programming (TCP connections, port scanning)
- Threading (concurrent operations)
- Networking fundamentals (IP, ports, protocols)
- Data visualization (Plotly charts)
- Real-time dashboards with Streamlit
- Working with system commands (subprocess)
- Data structures for logging and analysis

## Files
| File | What It Does |
|------|-------------|
| `app.py` | Streamlit dashboard with all monitoring views |
| `scanner.py` | Network and port scanning utilities |
| `monitor.py` | Connection monitoring and logging |

## Tech Stack
- Python
- Streamlit (dashboard)
- Plotly (visualizations)
- Socket (networking)
- Threading (concurrency)

## Important Note
This tool is for **educational purposes only**. Only scan networks and devices you own or have explicit permission to test.
