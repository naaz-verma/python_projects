import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from scanner import scan_ports, scan_port_range, resolve_hostname, get_local_ip, get_hostname, COMMON_PORTS
from monitor import get_active_connections, get_connection_stats, ping_host, check_common_services

# --- Page Config ---
st.set_page_config(page_title="Network Sentinel", page_icon="🛡️", layout="wide")

st.title("Network Sentinel")
st.markdown("*Built with WorldWithWeb* | **Educational tool -- only scan networks you own or have permission to test**")

# --- Tabs ---
tab1, tab2, tab3, tab4 = st.tabs([
    "Dashboard",
    "Port Scanner",
    "Connection Monitor",
    "Tools"
])

# ==================== TAB 1: DASHBOARD ====================
with tab1:
    st.header("Network Overview")

    # System info
    col1, col2, col3 = st.columns(3)
    local_ip = get_local_ip()
    hostname = get_hostname()
    col1.metric("Your IP", local_ip)
    col2.metric("Hostname", hostname)

    # Active connections summary
    if st.button("Refresh Dashboard", key="refresh_dash"):
        st.rerun()

    connections = get_active_connections()
    stats = get_connection_stats(connections)

    col3.metric("Active Connections", stats["total"])

    # Metrics row
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("TCP", stats["tcp"])
    c2.metric("UDP", stats["udp"])
    c3.metric("Established", stats["established"])
    c4.metric("Listening", stats["listening"])

    # Connection state chart
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Connection States")
        if stats["state_distribution"]:
            fig = go.Figure(data=[go.Pie(
                labels=list(stats["state_distribution"].keys()),
                values=list(stats["state_distribution"].values()),
                hole=0.4,
            )])
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("Top Local Ports")
        if stats["top_local_ports"]:
            ports = [p[0] for p in stats["top_local_ports"]]
            counts = [p[1] for p in stats["top_local_ports"]]
            fig = go.Figure(data=[go.Bar(x=ports, y=counts, marker_color="steelblue")])
            fig.update_layout(height=350, xaxis_title="Port", yaxis_title="Connections")
            st.plotly_chart(fig, use_container_width=True)

    st.metric("Unique Remote IPs", stats["unique_remote_ips"])

# ==================== TAB 2: PORT SCANNER ====================
with tab2:
    st.header("Port Scanner")
    st.warning("Only scan hosts you own or have explicit permission to test.")

    target = st.text_input("Target host (IP or hostname):", value="127.0.0.1", key="scan_target")
    scan_type = st.radio("Scan type:", ["Common Ports (fast)", "Port Range (slower)"], horizontal=True)

    if scan_type == "Port Range (slower)":
        col1, col2 = st.columns(2)
        start_port = col1.number_input("Start port:", 1, 65535, 1)
        end_port = col2.number_input("End port:", 1, 65535, 1024)

    if st.button("Start Scan", key="scan_btn"):
        # Resolve hostname
        ip = resolve_hostname(target)
        if not ip:
            st.error(f"Could not resolve hostname: {target}")
        else:
            st.info(f"Scanning {target} ({ip})...")
            progress = st.progress(0)
            scanned = [0]

            if scan_type == "Common Ports (fast)":
                total = len(COMMON_PORTS)

                def update_progress(port, result):
                    scanned[0] += 1
                    progress.progress(scanned[0] / total)

                results = scan_ports(ip, callback=update_progress)
            else:
                total = end_port - start_port + 1

                def update_progress(port, result):
                    scanned[0] += 1
                    if scanned[0] % 50 == 0:
                        progress.progress(min(scanned[0] / total, 1.0))

                results = scan_port_range(ip, start_port, end_port, timeout=0.5, callback=update_progress)

            progress.progress(1.0)

            if results:
                st.success(f"Found {len(results)} open port(s)")
                df = pd.DataFrame(results)
                st.dataframe(df, use_container_width=True)

                # Visual
                fig = go.Figure(data=[go.Bar(
                    x=[str(r["port"]) for r in results],
                    y=[1] * len(results),
                    text=[r["service"] for r in results],
                    marker_color="limegreen",
                )])
                fig.update_layout(
                    title="Open Ports",
                    xaxis_title="Port",
                    yaxis_visible=False,
                    height=300,
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No open ports found in the scanned range.")

# ==================== TAB 3: CONNECTION MONITOR ====================
with tab3:
    st.header("Active Connections")

    if st.button("Refresh", key="refresh_conn"):
        st.rerun()

    connections = get_active_connections()

    if connections:
        # Filters
        col1, col2 = st.columns(2)
        proto_filter = col1.multiselect("Protocol:", ["TCP", "UDP"], default=["TCP", "UDP"])
        state_options = list(set(c["state"] for c in connections))
        state_filter = col2.multiselect("State:", state_options, default=state_options)

        filtered = [c for c in connections
                     if c["protocol"] in proto_filter and c["state"] in state_filter]

        st.markdown(f"Showing **{len(filtered)}** of {len(connections)} connections")

        df = pd.DataFrame(filtered)
        if not df.empty:
            st.dataframe(df.drop(columns=["timestamp"], errors="ignore"), use_container_width=True)
    else:
        st.info("No active connections found (or insufficient permissions).")

# ==================== TAB 4: TOOLS ====================
with tab4:
    st.header("Network Tools")

    tool_choice = st.selectbox("Select tool:", ["Ping", "Service Check", "DNS Lookup"])

    if tool_choice == "Ping":
        ping_target = st.text_input("Host to ping:", value="google.com", key="ping_target")
        ping_count = st.slider("Ping count:", 1, 10, 4)

        if st.button("Ping", key="ping_btn"):
            with st.spinner(f"Pinging {ping_target}..."):
                result = ping_host(ping_target, ping_count)
            if result["reachable"]:
                st.success(f"{ping_target} is reachable!")
                if result["avg_time_ms"]:
                    st.metric("Average Latency", f"{result['avg_time_ms']} ms")
                with st.expander("Raw output"):
                    st.code(result["output"])
            else:
                st.error(f"{ping_target} is unreachable.")
                st.code(result["output"])

    elif tool_choice == "Service Check":
        service_target = st.text_input("Host to check:", value="127.0.0.1", key="svc_target")
        if st.button("Check Services", key="svc_btn"):
            with st.spinner("Checking common services..."):
                results = check_common_services(service_target)
            df = pd.DataFrame(results)
            st.dataframe(df, use_container_width=True)

    elif tool_choice == "DNS Lookup":
        dns_target = st.text_input("Hostname to resolve:", value="google.com", key="dns_target")
        if st.button("Lookup", key="dns_btn"):
            ip = resolve_hostname(dns_target)
            if ip:
                st.success(f"{dns_target} resolves to **{ip}**")
            else:
                st.error(f"Could not resolve {dns_target}")
