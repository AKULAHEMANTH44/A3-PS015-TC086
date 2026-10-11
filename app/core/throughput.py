import socket
import threading
import time


HOST = "127.0.0.1"
PORT = 8765
TEST_SIZE = 10 * 1024 * 1024


def _server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(1)

    conn, _ = server.accept()

    remaining = TEST_SIZE

    while remaining > 0:
        chunk = b"x" * min(64 * 1024, remaining)
        conn.sendall(chunk)
        remaining -= len(chunk)

    conn.close()
    server.close()


def measure_local_throughput():
    thread = threading.Thread(target=_server, daemon=True)
    thread.start()

    time.sleep(0.1)

    client = socket.create_connection((HOST, PORT), timeout=10)

    received = 0
    start = time.perf_counter()

    while received < TEST_SIZE:
        data = client.recv(64 * 1024)

        if not data:
            break

        received += len(data)

    elapsed = time.perf_counter() - start

    client.close()
    thread.join(timeout=2)

    if elapsed <= 0 or received == 0:
        return {
            "success": False,
            "throughput_mbps": None,
            "bytes_downloaded": received,
            "duration_seconds": None,
            "error": "No usable throughput data received",
        }

    throughput = (received * 8) / elapsed / 1_000_000

    return {
        "success": True,
        "throughput_mbps": round(throughput, 2),
        "bytes_downloaded": received,
        "duration_seconds": round(elapsed, 2),
        "error": None,
    }


if __name__ == "__main__":
    print(measure_local_throughput())
