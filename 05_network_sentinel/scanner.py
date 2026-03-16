import socket
import threading
from datetime import datetime

# Common ports and their services
COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    993: "IMAPS",
    995: "POP3S",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    5900: "VNC",
    6379: "Redis",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
    27017: "MongoDB",
}


def scan_port(host, port, timeout=1.0):
    """
    Check if a single port is open on the target host.

    Returns:
        dict with port info if open, None if closed
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()

        if result == 0:
            service = COMMON_PORTS.get(port, "Unknown")
            return {
                "port": port,
                "state": "open",
                "service": service,
            }
    except (socket.error, OSError):
        pass
    return None


def scan_ports(host, ports=None, timeout=1.0, callback=None):
    """
    Scan multiple ports on a target host using threads.

    Args:
        host: Target hostname or IP
        ports: List of ports to scan (defaults to common ports)
        timeout: Connection timeout in seconds
        callback: Function called with (port, result) for progress

    Returns:
        List of dicts for open ports
    """
    if ports is None:
        ports = sorted(COMMON_PORTS.keys())

    open_ports = []
    lock = threading.Lock()

    def _scan_one(port):
        result = scan_port(host, port, timeout)
        if result:
            with lock:
                open_ports.append(result)
        if callback:
            callback(port, result)

    threads = []
    for port in ports:
        t = threading.Thread(target=_scan_one, args=(port,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return sorted(open_ports, key=lambda x: x["port"])


def scan_port_range(host, start_port=1, end_port=1024, timeout=0.5, callback=None):
    """
    Scan a range of ports using threaded batches.

    Args:
        host: Target hostname or IP
        start_port: First port to scan
        end_port: Last port to scan
        timeout: Connection timeout
        callback: Progress callback

    Returns:
        List of open port dicts
    """
    ports = list(range(start_port, end_port + 1))
    open_ports = []
    lock = threading.Lock()
    batch_size = 50  # scan 50 ports at a time

    def _scan_one(port):
        result = scan_port(host, port, timeout)
        if result:
            with lock:
                open_ports.append(result)
        if callback:
            callback(port, result)

    for i in range(0, len(ports), batch_size):
        batch = ports[i:i + batch_size]
        threads = []
        for port in batch:
            t = threading.Thread(target=_scan_one, args=(port,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

    return sorted(open_ports, key=lambda x: x["port"])


def resolve_hostname(host):
    """Resolve a hostname to IP address."""
    try:
        ip = socket.gethostbyname(host)
        return ip
    except socket.gaierror:
        return None


def get_local_ip():
    """Get the local IP address of this machine."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def get_hostname():
    """Get the hostname of this machine."""
    return socket.gethostname()
