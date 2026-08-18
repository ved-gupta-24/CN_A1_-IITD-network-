<!-- # Assignment 1 — A1: Your Path Out

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
- DNS resolver: [PENDING] -->

# Assignment 1 — A1: Your Path Out

## Step 1 — Identify Network Interface, Local IP, MAC Address, and Gateway

### Goal
Determine the active network interface, private IP address, subnet mask, device MAC address, default gateway, DNS resolvers, and AP details to establish the local endpoint of the connection.

### Command / Action
1. `ifconfig en0 | grep -E "inet |ether"`
2. `netstat -nr -f inet | grep default`
3. `scutil --dns | grep 'nameserver\[[0-9]*\]' | head -n 2`
4. macOS Option (⌥) + Click on Wi-Fi icon in menu bar.

### Observation
Terminal Outputs:
    ether 14:7f:ce:a0:03:dc
    inet 10.184.30.65 netmask 0xffffe000 broadcast 10.184.31.255

    default            10.184.0.1         UGScg                 en0

    nameserver[0] : 2001:df4:e000:26::202
    nameserver[1] : 2001:df4:e000:29::104

Wi-Fi Menu UI Outputs:
    SSID: IITD_WIFI
    BSSID: a4:b4:39:40:dd:4f
    Channel: 157 (5 GHz, 80 MHz)
    RSSI: -63 dBm
    Security: WPA2 Enterprise

### Result
- **Interface:** en0
- **Device MAC Address:** 14:7f:ce:a0:03:dc
- **Local IP Address:** 10.184.30.65
- **Subnet Mask:** 255.255.224.0 (0xffffe000)
- **Default Gateway (T1):** 10.184.0.1
- **DNS Resolver:** 2001:df4:e000:26::202, 2001:df4:e000:29::104
- **SSID:** IITD_WIFI
- **BSSID (AP MAC):** a4:b4:39:40:dd:4f

### Record / To Fill
- **Location where measurement was taken:** Zanskar Hostel NC-13 room 
- **SSID:** IITD_WIFI
- **Interface:** en0
- **IP:** 10.184.30.65
- **Subnet mask:** 255.255.224.0
- **Gateway / T1:** 10.184.0.1
- **Wi-Fi interface MAC:** 14:7f:ce:a0:03:dc
- **BSSID / actual AP:** a4:b4:39:40:dd:4f
- **DNS resolver:** 2001:df4:e000:26::202, 2001:df4:e000:29::104
- **AP photograph:** [PENDING - Take photo of AP with placard]

### Inference
The laptop is connected to IITD_WIFI via interface en0 on a 5 GHz band (Channel 157) with an assigned private IP of 10.184.30.65. The default gateway (T1) is 10.184.0.1. The specific Access Point handling this connection has the BSSID a4:b4:39:40:dd:4f.



# Assignment 1 — A1: Your Path Out

## Step 2 — Verify T1 with Traceroute and Find Public Hops

### Goal
Check whether the default gateway appears as the first visible router (hop 1) in traceroute, find the last internal campus router, and identify the first 3 public routers outside the campus network.

### Commands Used
1. `traceroute -n 8.8.8.8` (Default UDP trace)
2. `sudo traceroute -I -m 20 -n 1.1.1.1` (ICMP trace to bypass firewall)

### Observation (UDP Trace to 8.8.8.8)
 1  10.184.0.13  4.133 ms
 2  10.255.109.100  4.271 ms
 ...
 7  10.255.237.94  60.504 ms
 8  10.152.7.214  60.640 ms
 9  * * *
10  * * *
11  8.8.8.8  60.614 ms

### Observation (ICMP Trace to 1.1.1.1)
 1  10.184.0.13  6.504 ms
 ...
 4  10.119.233.65  3.446 ms
 5  * * *
 6  * * *
 7  * * *
 8  * * *
 9  100.99.0.210  82.028 ms
10  1.1.1.1  6.214 ms

### Result
- **Our default gateway (T1):** 10.184.0.1
- **Traceroute Hop 1:** 10.184.0.13
- **T1 != traceroute hop 1**
- **Last internal campus router:** 10.152.7.214 (from the UDP trace)
- **Public Hops Found:** Intermediate public transit routers are masked.

### Inference
1. **The Gateway Discrepancy:** The configured default gateway (10.184.0.1) does not match the first visible traceroute hop (10.184.0.13). This usually occurs due to a First Hop Redundancy Protocol (like VRRP/HSRP) where the gateway is a virtual IP, or due to a local wireless controller/proxy ARP setup routing the traffic.
2. **Campus Boundary & Private IP Space:** The packets traverse deep into the campus infrastructure, utilizing private RFC 1918 addresses (`10.x.x.x`) up to hop 8.
3. **ISP Masking & CGNAT:** The network border aggressively drops traceroute packets. When forced to use ICMP, hop 9 resolves to `100.99.0.210`. This falls within the `100.64.0.0/10` block, which is designated for Carrier-Grade NAT (CGNAT). This proves the campus ISP uses CGNAT before passing traffic to the global public internet. Because the intermediate public routers are dropping TTL-expired packets for security, we are unable to extract 3 distinct intermediate public IPs.



## Step 3 — WHOIS Lookups for Public Destinations

### Goal
Identify the organization and regional registry responsible for the public IP addresses successfully reached in the traceroute.

### Commands Used
1. `whois 8.8.8.8 | head -n 20`
2. `whois 1.1.1.1 | head -n 20`

### Observation (8.8.8.8)
refer:        whois.arin.net
inetnum:      8.0.0.0 - 8.255.255.255
organisation: Administered by ARIN
NetRange:     8.8.8.0 - 8.8.8.255
CIDR:         8.8.8.0/24
NetName:      GOGL

### Observation (1.1.1.1)
refer:        whois.apnic.net
inetnum:      1.0.0.0 - 1.255.255.255
organisation: APNIC
status:       ALLOCATED
whois:        whois.apnic.net

### Result
- **IP Address 1:** 8.8.8.8
  - **Organization / NetName:** GOGL (Google LLC)
  - **Registry:** ARIN (American Registry for Internet Numbers)

- **IP Address 2:** 1.1.1.1
  - **Organization:** APNIC (Asia-Pacific Network Information Centre)
  - **Registry:** APNIC
  - *(Note: While the IP block is administered by APNIC, 1.1.1.1 is widely known as the public DNS resolver operated by Cloudflare in partnership with APNIC).*


# Assignment 1 — A3: The Delay Experiment

## A3.1 — Where does the time go?

### Goal
Record and analyze the Round-Trip Time (RTT) to five specific targets (T1-T5) to understand how distance and network conditions affect delay, and plot the relationship between RTT and approximate distance[cite: 1].

### Commands Used
- `ping -c 50 10.184.0.1` (T1: Default Gateway)[cite: 1]
- `ping -c 50 www.iitd.ac.in` (T2: IITD Website)[cite: 1]
- `ping -c 50 8.8.8.8` (T3: Google DNS)[cite: 1]
- `ping -c 50 www.iitb.ac.in` (T4: IIT Bombay)[cite: 1]
- `ping -c 50 www.mit.edu` (T5: MIT Website)[cite: 1]

### Measured RTT Data
| Target | Destination IP | Distance (Approx) | Min RTT (ms) | Median RTT (ms) | Max RTT (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T1** | 10.184.0.1 | 0 km (Local) | 2.801 | 4.600 | 60.799 |
| **T2** | 10.10.211.212 | 0 km (Campus) | 3.024 | 4.949 | 56.129 |
| **T3** | 8.8.8.8 | Varies (Anycast) | 57.737 | 58.924 | 300.344 |
| **T4** | 103.21.124.133 | ~1100 km | N/A | N/A | N/A |
| **T5** | 23.47.244.83 | ~12,000 km | 54.653 | 56.499 | 143.778 |

*(Note: T4 resulted in 100% packet loss, likely due to a firewall configured to drop ICMP Echo Requests).*

### Plot: RTT vs. Distance
*[Insert A3.1 Plot Here: X-axis = Distance (km), Y-axis = RTT (ms). Plot Min, Median, and Max for T1, T2, T3, and T5]*

### Analysis & Inferences

**1. Estimated Propagation Delay vs. Measured Minimum:**
Using the formula $d / (2 \times 10^8 \text{ m/s})$, the estimated one-way propagation delay to MIT (T5) at 12,000 km is approximately $60 \text{ ms}$, meaning the RTT should have a hard floor of at least $120 \text{ ms}$[cite: 1]. However, our measured minimum was $54.653 \text{ ms}$. This discrepancy exists because `www.mit.edu` resolves to an Akamai CDN edge server (`e9566.dscb.akamaiedge.net`), meaning the ICMP packets never actually travelled to Massachusetts; they were intercepted and answered by a geographically closer cache server.

**2. Gap Between Minimum and Median:**
The gap between the minimum RTT and the median RTT is primarily caused by **queuing delay**[cite: 1]. This delay component shows up as variation rather than a fixed amount because it depends on the instantaneous traffic load at every router along the path. When a router's buffer is empty, a packet passes through immediately (minimum RTT). When the buffer is full of other traffic, the packet must wait, increasing the total time.

**3. RTT to T1 is Not Zero:**
Even though T1 (the default gateway) is only one hop away, the RTT is not zero[cite: 1]. The observed minimum RTT of $2.801 \text{ ms}$ consists of local network overhead:
*   **Transmission Delay:** Time required to push the packet onto the wireless medium.
*   **Propagation Delay:** The physical time for the signal to reach the Access Point.
*   **Processing Delay:** The time the AP takes to process the frame and generate the reply.
*   **Medium Access (MAC) Delay:** On Wi-Fi (CSMA/CA), the device must wait for a clear channel before transmitting, adding variable delay.

**4. Missing Data for T4 (IIT Bombay):**
The RTT for T4 could not be plotted because the ping resulted in 100% packet loss. This indicates that the target network (`103.21.124.133`) or its perimeter firewall is explicitly configured to drop ICMP Echo Request packets for security and anti-reconnaissance reasons, preventing standard latency measurements.

# Assignment 1 — A3: The Delay Experiment

## A3.2 — Make transmission delay visible

### Goal
Observe how packet size affects round-trip time (RTT) by pinging the default gateway (T1) and a public destination (T3) with varying payload sizes, and analyze the resulting transmission delay.

### Commands Used
- `ping -c 30 -s [size] 10.184.0.1` (Sizes: 64, 256, 512, 1024, 1400 bytes)[cite: 1]
- `ping -c 30 -s [size] 8.8.8.8` (Sizes: 64, 256, 512, 1024, 1400 bytes)[cite: 1]

### Measured Minimum RTT Data
| Packet Size | T1 Min RTT (10.184.0.1) | T3 Min RTT (8.8.8.8) |
| :--- | :--- | :--- |
| **64 Bytes** | 2.842 ms | 59.761 ms |
| **256 Bytes** | 2.800 ms | 59.865 ms |
| **512 Bytes** | 3.476 ms | 59.431 ms |
| **1024 Bytes** | 3.093 ms | 59.925 ms |
| **1400 Bytes** | 3.364 ms | 59.522 ms |

### Plot: Minimum RTT vs. Packet Size
*[Insert A3.2 Plot Here: X-axis = Packet Size (Bytes), Y-axis = Min RTT (ms). Plot two lines (T1 and T3) and fit a straight line through each]*

### Analysis & Inferences

**1. What is the slope made of?**
The slope of the line represents the **transmission delay** ($L/R$), which is the time required to push the physical bits of the packet onto the link[cite: 1]. As the packet size ($L$) increases, it takes more time to transmit, causing the slope to rise[cite: 1]. Because a packet to T3 crosses multiple router links (unlike T1, which is only one hop), the transmission delay is incurred repeatedly at each intermediate hop, which should theoretically make the slope for T3 steeper than T1.

**2. What is the intercept made of?**
The y-intercept represents the baseline latency independent of packet size. This consists primarily of the **propagation delay** (the time for the signal to physically travel over the medium) and the baseline **processing/MAC delays** at the routers[cite: 1]. The intercept for T3 is much higher (~60 ms) than T1 (~3 ms) because T3 involves traversing the campus infrastructure, the ISP, and reaching a public Google Anycast server, vastly increasing the physical distance and number of processing nodes.

**3. Slope Comparison & Real-World Observations:**
In our measured data, the RTT remained relatively flat across all sizes for both T1 (hovering between 2.8-3.4 ms) and T3 (hovering between 59.4-59.9 ms). The expected linear slope (Transmission Delay) is nearly invisible. 
This "messy real result"[cite: 1] occurs because modern campus networks and ISP backbone links have incredibly high bandwidth ($R$ in the $L/R$ equation). A 1400-byte packet is so small relative to gigabit or multi-gigabit link speeds that the increase in transmission time is only a fraction of a millisecond. This tiny increase is completely swallowed by the natural jitter and variable MAC delays inherent to a shared Wi-Fi connection, resulting in a flat or even slightly fluctuating plot rather than a clean, upward-sloping line.


# Assignment 1 — A3: The Delay Experiment

## A3.3 — Watch a queue fill

### Goal
Continuously ping a public destination (T3: Google DNS, `8.8.8.8`) across a 5-minute window during both a busy hour and a quiet hour to observe buffer dynamics and time-dependent queuing delay.

### Experimental Setup & Timestamps
*   **Target:** `8.8.8.8` (Google Public DNS)
*   **Packet Count:** 300 packets (1 packet/sec $\approx$ 5 minutes)
*   **Capture 1 (Busy Hour):** ~5:10 PM – 5:15 PM IST
*   **Capture 2 (Quiet Hour):** ~2:35 AM – 2:40 AM IST

---

### Measured RTT Summary
| Metric | Busy Hour (~5:10 PM) | Quiet Hour (~2:35 AM) |
| :--- | :--- | :--- |
| **Packets Transmitted / Received** | 300 / 300 (0.0% loss) | 300 / 300 (0.0% loss) |
| **Minimum RTT** | 58.766 ms | 58.676 ms |
| **Average RTT** | 64.657 ms | 97.183 ms |
| **Maximum RTT** | 211.649 ms | 460.370 ms |
| **Standard Deviation ($\sigma$)** | 14.201 ms | 84.150 ms |

---

### Plot: RTT Over Time (5-Minute Time Series)
*[Insert A3.3 Plot Here: X-axis = Time / Sequence (1 to 300 seconds), Y-axis = RTT (ms). Overlay two distinct lines: "Busy Hour (5:10 PM)" and "Quiet Hour (2:35 AM)"]*

---

### Analysis & Inferences

**1. Which delay component moved, and which didn't?**
*   **Did NOT move — Propagation and Transmission Delay:** The minimum RTT floor remained virtually identical across both runs ($58.766\text{ ms}$ at 5:10 PM vs. $58.676\text{ ms}$ at 2:35 AM). Because the physical distance to the Google Anycast point-of-presence and the physical link capacities remained constant, the baseline propagation and transmission delays did not shift.
*   **Moved — Queuing Delay:** All observed variation, elevated averages, and extreme spikes were driven entirely by variable queuing delay. When intermediate router or access point buffers filled with transient burst traffic, packets spent significantly longer waiting in queue before transmission.

**2. What does the shape of the graph tell you? (Queue Dynamics)**
*   The queue is **not steadily full; it is bursty and follows a cyclic "sawtooth" pattern.**
*   Rather than maintaining a consistently high delay, the RTT hovers at its $\approx 60\text{ ms}$ baseline for long stretches and periodically undergoes rapid escalation events.
*   A clear queue-filling pattern is visible in the quiet hour capture (e.g., sequences 161 through 170), where the delay steps up incrementally each second:
    $$90.7\text{ ms} \rightarrow 135.8\text{ ms} \rightarrow 181.9\text{ ms} \rightarrow 223.8\text{ ms} \rightarrow 272.1\text{ ms} \rightarrow 311.2\text{ ms} \rightarrow 352.2\text{ ms} \rightarrow 399.0\text{ ms} \rightarrow 446.5\text{ ms}$$
    Once the buffer drains or the burst completes (sequence 171), the latency immediately drops back to the $60.3\text{ ms}$ floor.
*   This behavior illustrates classic bufferbloat and transient traffic bursts rather than permanent link saturation.