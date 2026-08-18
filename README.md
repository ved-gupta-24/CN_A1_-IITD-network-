# Assignment 1 — A1: Your Path Out

## Step 1 — Find the Default Gateway

### Goal
Identify the current default gateway (T1) used by the laptop and record the
context of the measurement.

### Command
netstat -nr | grep default

### Observation
IPv4 default route:
    default    10.152.224.1    ...    en0

### Result
T1 / Default Gateway = 10.152.224.1
Interface = en0

### Record
- Location where measurement was taken - LH 114 (LHC)
- wifi connected to is IITD_WIFI
- Interface: en0
- Default Gateway / T1: 10.152.224.1

### Inference
10.152.224.1 is the laptop's current default gateway and therefore our
candidate first router on the path out of the local network.

The location must be recorded because the gateway can change when moving
between different campus networks.

## Step 2 — Verify T1 with Traceroute

### Goal
Check whether the default gateway appears as the first visible router
(hop 1) in traceroute.

### Command
traceroute -n www.iitd.ac.in

### Observation
Hop 1:
    10.152.224.3

Our default gateway:
    10.152.224.1

Therefore:
    T1 != traceroute hop 1

Also observed:
    Hop 2 → 10.254.151.13 / 10.254.151.9
    Hop 3 → 10.254.236.6 / 10.254.236.26 / 10.254.236.2
    Hop 4 onward → no response (*)

### Inference
The default gateway does not appear as the first visible traceroute hop.

We do NOT yet know why. This discrepancy needs to be investigated rather
than assuming that 10.152.224.3 is necessarily the first router.


## Step 3 — Verify the Routing Decision for T2

### Goal
Check which gateway macOS actually uses when sending traffic to the IITD
destination seen in the traceroute.

### Command
route -n get 10.10.211.212

### Observation
gateway:
    10.152.224.1

interface:
    en0

### Result
For destination 10.10.211.212:
    next-hop gateway = 10.152.224.1
    outgoing interface = en0

### Inference
The routing table independently confirms that 10.152.224.1 is the
actual gateway selected by macOS for this destination.

However, traceroute's first visible response was 10.152.224.3.
The discrepancy remains unresolved and should be investigated rather
than silently "corrected."


## Step 4 — Identify Wi-Fi Interface & Local IP

### Goal
Identify how the laptop is connected to the network and record its local
network configuration.

### Command
networksetup -getinfo Wi-Fi

### Observation
Connection:
    Wi-Fi

SSID:
    IITD_WIFI

Interface:
    en0

IP:
    10.152.230.124

Subnet mask:
    255.255.192.0

Router:
    10.152.224.1

Wi-Fi interface MAC:
    14:7f:ce:a0:03:dc

### Inference
The laptop is connected to IITD_WIFI through Wi-Fi on en0, with local IP
10.152.230.124 and gateway 10.152.224.1.

### Record / To Fill
- Physical location: LH 114 (LHC)
- SSID: IITD_WIFI
- Interface: en0
- IP: 10.152.230.124
- Subnet mask: 255.255.192.0
- Gateway / T1: 10.152.224.1
- Wi-Fi interface MAC: 14:7f:ce:a0:03:dc
- BSSID / actual AP: [PENDING]
- AP photograph: [PENDING]
- DNS resolver: [PENDING]