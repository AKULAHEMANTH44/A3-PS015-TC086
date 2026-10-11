import subprocess
import platform
import socket
import time
import re
import psutil


def get_default_gateway():
    """Find the real active IPv4 default gateway on Windows."""
    if platform.system().lower() == "windows":
        try:
            result = subprocess.run(
                ["route", "print", "0.0.0.0"],
                capture_output=True,
                text=True,
                timeout=10
            )

            for line in result.stdout.splitlines():
                parts = line.split()

                if len(parts) >= 5:
                    destination = parts[0]
                    gateway = parts[2]
                    interface = parts[3]

                    if (
                        destination == "0.0.0.0"
                        and gateway != "0.0.0.0"
                        and re.match(r"^\d+\.\d+\.\d+\.\d+$", gateway)
                    ):
                        return gateway

        except Exception:
            pass

    return None


def ping_host(host, count=4):
    """Measure reachability, latency and packet loss."""

    if platform.system().lower() == "windows":
        command = [
            "ping",
            "-n",
            str(count),
            "-w",
            "1000",
            host
        ]
    else:
        command = [
            "ping",
            "-c",
            str(count),
            "-W",
            "1",
            host
        ]

    start = time.perf_counter()

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=15
        )

        elapsed = time.perf_counter() - start
        output = result.stdout

        loss_match = re.search(
            r"Lost = \d+ \((\d+)% loss\)",
            output,
            re.IGNORECASE
        )

        if not loss_match:
            loss_match = re.search(
                r"(\d+)%\s*loss",
                output,
                re.IGNORECASE
            )

        packet_loss = (
            float(loss_match.group(1))
            if loss_match
            else (0.0 if result.returncode == 0 else 100.0)
        )

        latency_match = re.search(
            r"Average =\s*(\d+)\s*ms",
            output,
            re.IGNORECASE
        )

        if not latency_match:
            latency_match = re.search(
                r"(?:avg|average).*?(\d+)\s*ms",
                output,
                re.IGNORECASE
            )

        latency = (
            float(latency_match.group(1))
            if latency_match
            else None
        )

        return {
            "host": host,
            "reachable": result.returncode == 0,
            "latency_ms": latency,
            "packet_loss_percent": packet_loss,
            "duration_seconds": round(elapsed, 3),
            "raw_output": output
        }

    except Exception as e:
        return {
            "host": host,
            "reachable": False,
            "latency_ms": None,
            "packet_loss_percent": 100.0,
            "duration_seconds": None,
            "error": str(e)
        }


def dns_test(hostname="example.com"):
    """Test DNS resolution."""

    start = time.perf_counter()

    try:
        address = socket.gethostbyname(hostname)
        elapsed = (time.perf_counter() - start) * 1000

        return {
            "success": True,
            "hostname": hostname,
            "resolved_ip": address,
            "resolution_ms": round(elapsed, 2)
        }

    except Exception as e:
        elapsed = (time.perf_counter() - start) * 1000

        return {
            "success": False,
            "hostname": hostname,
            "resolved_ip": None,
            "resolution_ms": round(elapsed, 2),
            "error": str(e)
        }


def get_network_interfaces():
    """Collect local IPv4 interface information."""

    interfaces = []

    for name, addresses in psutil.net_if_addrs().items():

        for address in addresses:

            if address.family == socket.AF_INET:

                interfaces.append({
                    "interface": name,
                    "ip": address.address,
                    "netmask": address.netmask
                })

    return interfaces


def run_basic_diagnostics():
    """Run the PS-015 connectivity measurements."""

    gateway = get_default_gateway()

    gateway_result = None

    if gateway:
        gateway_result = ping_host(gateway)

    dns_result = dns_test()

    internet_result = ping_host("8.8.8.8")

    return {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "gateway": gateway,
        "gateway_test": gateway_result,
        "dns_test": dns_result,
        "internet_test": internet_result,
        "interfaces": get_network_interfaces()
    }
