#!/usr/bin/env python3
"""
netlab_gen.py — COL334 Assignment 1

Run this while your capture is running:

    python netlab_gen.py --roll 2024CS10057 --day 1 --window 2

It performs your fixed measurements and generates traffic toward the lab
server. It takes about four minutes.

It prints a SEED_TAG. Write that down — you need it in your report.

Start your capture first, then run this, then let the capture run out its
full ten minutes.
"""

import argparse
import base64
import hashlib
import platform
import random
import socket
import subprocess
import sys
import time

COURSE_SALT = "col334-2026-a1-7f3d9b2e4c81a065"
DEFAULT_SERVER = "168.144.154.92"
DNS_BASE = "probe.col334.lab"

TARGETS = [
    ("T2", "www.iitd.ac.in"),
    ("T3", "8.8.8.8"),
    ("T4", "www.iitb.ac.in"),
    ("T5", "www.mit.edu"),
]

CLASS_PROB = {
    "beacon": 0.85,
    "dns_token": 0.80,
    "cleartext_cred": 0.65,
    "port_sweep": 0.70,
    "ttl_anomaly": 0.70,
    "wrong_port": 0.60,
}

USERNAMES = ["mfarooq", "rsharma", "avinash", "kpillai", "dchatterjee",
             "snaidu", "tbhatia", "jvarghese", "nsingh", "pmehra"]


def make_plan(roll, salt):
    roll = roll.strip().upper()
    digest = hashlib.sha256((roll + salt).encode()).hexdigest()
    rng = random.Random(int(digest[:16], 16))

    present = [c for c, p in CLASS_PROB.items() if rng.random() < p]
    ordered = sorted(CLASS_PROB, key=lambda c: -CLASS_PROB[c])
    while len(present) < 3:
        for c in ordered:
            if c not in present:
                present.append(c)
                break
    while len(present) > 6:
        present.remove(rng.choice(present))
    present = [c for c in ordered if c in present]

    plan = {
        "roll": roll,
        "seed_tag": digest[:8].upper(),
        "digest": digest,
        "classes": present,
        "params": {},
    }
    p = plan["params"]

    if "beacon" in present:
        p["beacon"] = {
            "interval_s": rng.randint(5, 19),
            "dst_port": rng.randint(20001, 20040),
            "payload_len": rng.choice([37, 53, 71, 89, 101]),
            "count": rng.choice([8, 10, 12]),
        }

    if "dns_token" in present:
        alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
        token = "".join(rng.choice(alphabet) for _ in range(8))
        label = base64.b32encode(token.encode()).decode().rstrip("=").lower()
        p["dns_token"] = {
            "token": token,
            "label": label,
            "queries": rng.choice([4, 6, 8]),
        }

    if "cleartext_cred" in present:
        p["cleartext_cred"] = {
            "username": rng.choice(USERNAMES) + str(rng.randint(10, 99)),
            "password": "".join(rng.choice("abcdefghjkmnpqrstuvwxyz23456789")
                                for _ in range(10)),
            "port": 8080,
            "path": "/portal/login",
        }

    if "port_sweep" in present:
        start = rng.randint(3000, 9000)
        count = rng.choice([24, 32, 48])
        p["port_sweep"] = {
            "start_port": start,
            "end_port": start + count - 1,
            "count": count,
        }

    if "ttl_anomaly" in present:
        p["ttl_anomaly"] = {
            "ttl": rng.choice([3, 5, 7, 11, 13, 17, 19, 23]),
            "dst_port": rng.randint(30001, 30040),
            "count": rng.choice([5, 7, 9]),
        }

    if "wrong_port" in present:
        p["wrong_port"] = {
            "port": rng.choice([8443, 9443, 10443]),
            "requests": rng.choice([3, 5]),
        }

    return plan


class Log:
    def __init__(self, path):
        self.path = path
        self.fh = open(path, "w", encoding="utf-8")

    def write(self, line=""):
        stamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.fh.write(f"[{stamp}] {line}\n")
        self.fh.flush()

    def raw(self, text):
        self.fh.write(text.rstrip() + "\n")
        self.fh.flush()

    def close(self):
        self.fh.close()


def run_cmd(cmd, log, timeout=120):
    log.write(f"$ {' '.join(cmd)}")
    try:
        out = subprocess.run(cmd, capture_output=True, text=True,
                             timeout=timeout)
        log.raw(out.stdout)
        if out.stderr.strip():
            log.raw("--- stderr ---")
            log.raw(out.stderr)
    except FileNotFoundError:
        log.write(f"!! command not found: {cmd[0]}")
    except subprocess.TimeoutExpired:
        log.write(f"!! timed out after {timeout}s")
    except Exception as exc:
        log.write(f"!! failed: {exc}")
    log.raw("")


def measurements(log):
    system = platform.system().lower()
    win = system.startswith("win")
    mac = system == "darwin"
    log.write("=== fixed measurements ===")

    log.write("-- interface configuration --")
    if win:
        run_cmd(["ipconfig", "/all"], log)
    elif mac:
        run_cmd(["ifconfig"], log)
    else:
        run_cmd(["ip", "addr"], log)

    log.write("-- routing table --")
    if win:
        run_cmd(["route", "print"], log)
    elif mac:
        # IPv4 table only — same job as Linux `ip route` (not `ip -6 route`).
        run_cmd(["netstat", "-nr", "-f", "inet"], log)
    else:
        run_cmd(["ip", "route"], log)

    for tag, host in TARGETS:
        log.write(f"-- ping {tag} {host} --")
        run_cmd(["ping", "-n", "20", host] if win
                else ["ping", "-c", "20", host], log, timeout=90)

    for tag, host in TARGETS:
        log.write(f"-- traceroute {tag} {host} --")
        run_cmd(["tracert", "-d", "-h", "20", host] if win
                else ["traceroute", "-n", "-m", "20", host], log, timeout=150)


def emit_beacon(cfg, server_ip, log):
    payload = bytes([0xAB]) * cfg["payload_len"]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        for i in range(cfg["count"]):
            s.sendto(payload, (server_ip, cfg["dst_port"]))
            if i < cfg["count"] - 1:
                time.sleep(cfg["interval_s"])
    finally:
        s.close()


def emit_dns_token(cfg, _server_ip, log):
    for i in range(cfg["queries"]):
        name = f"{cfg['label']}-{i:02d}.{DNS_BASE}"
        try:
            socket.getaddrinfo(name, None)
        except socket.gaierror:
            pass
        time.sleep(1.5)


def emit_cleartext_cred(cfg, server_ip, log):
    body = f"username={cfg['username']}&password={cfg['password']}&remember=1"
    req = (
        f"POST {cfg['path']} HTTP/1.1\r\n"
        f"Host: {server_ip}\r\n"
        f"User-Agent: netlab-gen/1.0\r\n"
        f"Content-Type: application/x-www-form-urlencoded\r\n"
        f"Content-Length: {len(body)}\r\n"
        f"Connection: close\r\n\r\n{body}"
    )
    try:
        s = socket.create_connection((server_ip, cfg["port"]), timeout=5)
        s.sendall(req.encode())
        s.recv(4096)
        s.close()
    except OSError as exc:
        log.write(f"   (no response: {exc})")


def emit_port_sweep(cfg, server_ip, log):
    for port in range(cfg["start_port"], cfg["end_port"] + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.25)
        try:
            s.connect((server_ip, port))
        except OSError:
            pass
        finally:
            s.close()
        time.sleep(0.05)


def emit_ttl_anomaly(cfg, server_ip, log):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, cfg["ttl"])
    try:
        for _ in range(cfg["count"]):
            s.sendto(b"ttl-probe", (server_ip, cfg["dst_port"]))
            time.sleep(0.8)
    finally:
        s.close()


def emit_wrong_port(cfg, server_ip, log):
    req = (f"GET /status HTTP/1.1\r\nHost: {server_ip}\r\n"
           f"User-Agent: netlab-gen/1.0\r\nConnection: close\r\n\r\n")
    for _ in range(cfg["requests"]):
        try:
            s = socket.create_connection((server_ip, cfg["port"]), timeout=5)
            s.sendall(req.encode())
            s.recv(4096)
            s.close()
        except OSError as exc:
            log.write(f"   (no response: {exc})")
        time.sleep(2)


EMITTERS = {
    "beacon": emit_beacon,
    "dns_token": emit_dns_token,
    "cleartext_cred": emit_cleartext_cred,
    "port_sweep": emit_port_sweep,
    "ttl_anomaly": emit_ttl_anomaly,
    "wrong_port": emit_wrong_port,
}


def main():
    ap = argparse.ArgumentParser(
        description="COL334 Assignment 1 traffic generator")
    ap.add_argument("--roll", required=True, help="your roll number")
    ap.add_argument("--day", type=int, choices=[1, 2], required=True,
                    help="capture day, 1 or 2")
    ap.add_argument("--window", type=int, choices=[1, 2, 3], required=True,
                    help="capture window, 1 2 or 3")
    ap.add_argument("--server", default=DEFAULT_SERVER,
                    help=argparse.SUPPRESS)
    args = ap.parse_args()

    plan = make_plan(args.roll, COURSE_SALT)
    roll = plan["roll"]

    logname = f"netlab_gen_{roll}_D{args.day}_W{args.window}.log"
    log = Log(logname)

    print("=" * 62)
    print(f"  netlab_gen — {roll}   day {args.day}, window {args.window}")
    print(f"  SEED_TAG: {plan['seed_tag']}      <-- copy this into your report")
    print("=" * 62)
    print("  Your capture should already be running. This takes ~4 minutes.")
    print()

    log.write(f"netlab_gen roll={roll} day={args.day} window={args.window}")
    log.write(f"SEED_TAG={plan['seed_tag']}")
    log.write(f"platform={platform.platform()}")
    log.write(f"server={args.server}")
    log.raw("")

    try:
        server_ip = socket.gethostbyname(args.server)
    except socket.gaierror:
        print(f"  !! cannot reach {args.server}")
        print("     Check you are on the campus network, then post on the forum.")
        log.write(f"!! cannot reach {args.server} — aborting")
        log.close()
        return 1

    log.write(f"server = {server_ip}")
    print(f"  [1/2] measurements against {len(TARGETS)} targets ...")
    measurements(log)

    print("  [2/2] generating traffic ...")
    log.write("=== generated traffic ===")

    for cls in plan["classes"]:
        try:
            EMITTERS[cls](plan["params"][cls], server_ip, log)
        except Exception:
            pass

    log.write("=== done ===")
    log.close()

    print()
    print(f"  Done. Log written to {logname}")
    print(f"  SEED_TAG: {plan['seed_tag']}")
    print("  Let your capture run out its full 10 minutes, then keep the")
    print("  .pcapng and this .log safe until you submit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
