import subprocess
import platform
import re
from datetime import datetime


def get_active_connections():
    """
    Get active network connections using netstat.

    Returns:
        List of dicts with connection info
    """
    connections = []

    try:
        if platform.system() == "Windows":
            output = subprocess.check_output("netstat -an", shell=True, text=True, timeout=10)
        else:
            output = subprocess.check_output("netstat -an", shell=True, text=True, timeout=10)

        lines = output.strip().split("\n")

        for line in lines:
            parts = line.split()
            if len(parts) >= 4 and parts[0] in ("TCP", "UDP", "tcp", "udp", "tcp4", "tcp6", "udp4", "udp6"):
                proto = parts[0].upper()
                local = parts[1] if len(parts) > 1 else ""
                remote = parts[2] if len(parts) > 2 else ""
                state = parts[3] if len(parts) > 3 else "N/A"

                # Normalize protocol
                if "TCP" in proto:
                    proto = "TCP"
                elif "UDP" in proto:
                    proto = "UDP"

                connections.append({
                    "protocol": proto,
                    "local_address": local,
                    "remote_address": remote,
                    "state": state,
                    "timestamp": datetime.now().isoformat(),
                })
    except (subprocess.SubprocessError, FileNotFoundError):
        pass

    return connections


def get_connection_stats(connections):
    """Analyze connections and return statistics."""
    stats = {
        "total": len(connections),
        "tcp": sum(1 for c in connections if c["protocol"] == "TCP"),
        "udp": sum(1 for c in connections if c["protocol"] == "UDP"),
        "established": sum(1 for c in connections if c["state"] == "ESTABLISHED"),
        "listening": sum(1 for c in connections if c["state"] in ("LISTENING", "LISTEN")),
        "time_wait": sum(1 for c in connections if c["state"] == "TIME_WAIT"),
        "close_wait": sum(1 for c in connections if c["state"] == "CLOSE_WAIT"),
    }

    # Unique remote IPs
    remote_ips = set()
    for c in connections:
        addr = c["remote_address"]
        if addr and addr not in ("*:*", "0.0.0.0:*", "[::]:*"):
            ip = addr.rsplit(":", 1)[0]
            remote_ips.add(ip)
    stats["unique_remote_ips"] = len(remote_ips)

    # Port frequency
    local_ports = {}
    for c in connections:
        addr = c["local_address"]
        if ":" in addr:
            port = addr.rsplit(":", 1)[-1]
            if port != "*":
                local_ports[port] = local_ports.get(port, 0) + 1
    stats["top_local_ports"] = sorted(local_ports.items(), key=lambda x: x[1], reverse=True)[:10]

    # State distribution
    state_dist = {}
    for c in connections:
        state = c["state"]
        state_dist[state] = state_dist.get(state, 0) + 1
    stats["state_distribution"] = state_dist

    return stats


def ping_host(host, count=4):
    """
    Ping a host and return results.

    Returns:
        dict with ping statistics
    """
    try:
        if platform.system() == "Windows":
            cmd = f"ping -n {count} {host}"
        else:
            cmd = f"ping -c {count} {host}"

        output = subprocess.check_output(cmd, shell=True, text=True, timeout=30)

        # Extract average time
        avg_time = None
        if platform.system() == "Windows":
            match = re.search(r"Average\s*=\s*(\d+)ms", output)
            if match:
                avg_time = float(match.group(1))
        else:
            match = re.search(r"avg.*?=\s*[\d.]+/([\d.]+)/", output)
            if match:
                avg_time = float(match.group(1))

        return {
            "host": host,
            "reachable": True,
            "avg_time_ms": avg_time,
            "output": output,
        }
    except subprocess.SubprocessError:
        return {
            "host": host,
            "reachable": False,
            "avg_time_ms": None,
            "output": "Host unreachable or timed out",
        }


def check_common_services(host):
    """Quick check of common services on a host."""
    import socket

    services = [
        (80, "HTTP"),
        (443, "HTTPS"),
        (22, "SSH"),
        (21, "FTP"),
        (3389, "RDP"),
        (3306, "MySQL"),
    ]

    results = []
    for port, name in services:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            sock.close()
            results.append({
                "port": port,
                "service": name,
                "status": "Open" if result == 0 else "Closed",
            })
        except (socket.error, OSError):
            results.append({
                "port": port,
                "service": name,
                "status": "Error",
            })

    return results
