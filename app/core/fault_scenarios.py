from typing import Dict, Any


SCENARIOS = {
    "Normal Connection": {
        "description": "All connectivity measurements succeed.",
        "gateway_reachable": True,
        "dns_success": True,
        "packet_loss": 0,
        "latency": 35,
        "throughput_mbps": 850.0
    },

    "Gateway Unreachable": {
        "description": "The local gateway does not respond.",
        "gateway_reachable": False,
        "dns_success": False,
        "packet_loss": 100,
        "latency": None,
        "throughput_mbps": None
    },

    "DNS Failure": {
        "description": "Gateway works, but DNS resolution fails.",
        "gateway_reachable": True,
        "dns_success": False,
        "packet_loss": 0,
        "latency": 5,
        "throughput_mbps": None
    },

    "Induced Packet Loss": {
        "description": "Gateway works but substantial packet loss is observed.",
        "gateway_reachable": True,
        "dns_success": True,
        "packet_loss": 35,
        "latency": 80,
        "throughput_mbps": 420.0
    },

    "Network Congestion": {
        "description": "Connectivity works but latency increases under a simulated loaded condition.",
        "gateway_reachable": True,
        "dns_success": True,
        "packet_loss": 2,
        "latency": 220,
        "throughput_mbps": 120.0
    },

    "Inconclusive": {
        "description": "Available measurements are insufficient to isolate the cause.",
        "gateway_reachable": True,
        "dns_success": True,
        "packet_loss": None,
        "latency": None,
        "throughput_mbps": None
    }
}


def create_scenario_evidence(name: str) -> Dict[str, Any]:

    scenario = SCENARIOS[name]

    gateway_reachable = scenario["gateway_reachable"]
    dns_success = scenario["dns_success"]

    packet_loss = scenario["packet_loss"]
    latency = scenario["latency"]
    throughput = scenario["throughput_mbps"]

    return {
        "timestamp": "SIMULATED CONTROLLED LAB SCENARIO",

        "gateway": "192.168.1.1",

        "gateway_test": {
            "host": "192.168.1.1",
            "reachable": gateway_reachable,
            "latency_ms": 5 if gateway_reachable else None,
            "packet_loss_percent": 0 if gateway_reachable else 100
        },

        "dns_test": {
            "success": dns_success,
            "hostname": "example.com",
            "resolved_ip": "93.184.216.34" if dns_success else None,
            "resolution_ms": 20 if dns_success else None
        },

        "internet_test": {
            "host": "8.8.8.8",
            "reachable": gateway_reachable,
            "latency_ms": latency,
            "packet_loss_percent": packet_loss
        },

        "throughput_test": {
            "success": throughput is not None,
            "throughput_mbps": throughput,
            "loaded_condition": name == "Network Congestion",
            "source": "Controlled laboratory simulation"
        },

        "scenario": name
    }
