# COL334 Assignment 1: Mapping the Machine You Live On
**Team:** Vedant Gupta & Daksh Chauhan

---

## Measurement Context
All measurements for Figure 1A were taken from Zanskar NC-13 using a MacBook connected via Wi-Fi (`en0`) to `IITD_WIFI` on the 5 GHz band (Channel 157) with an RSSI of -63 dBm[cite: 1]. The host was assigned the private IP `10.184.30.65` on a `/19` subnet, with a configured default gateway of `10.184.0.1` and IPv6 DNS resolvers[cite: 1]. 

Measurements for Figure 1B were taken from Room L1 (hostel) using a Linux laptop connected via Wi-Fi (`wlan0`) to `eduroam` (WPA2 802.1X) on the 5 GHz band (Channel 149)[cite: 1]. The host received IP `10.184.30.72` on the same `10.184.0.0/19` subnet with the identical configured gateway of `10.184.0.1`[cite: 1].

## A1: Your Path Out
### Figure 1A: Zanskar Hostel Path (Vedant)
![Zanskar Path Out](figure1a.svg)

**Analysis of Zanskar Path (Vedant):**
*   **The Gateway Discrepancy:** The configured default gateway (`10.184.0.1`) does not match the first visible traceroute hop (`10.184.0.13`)[cite: 2]. This indicates a First Hop Redundancy Protocol (like VRRP/HSRP) utilizing a Virtual IP, or a proxy ARP configuration[cite: 2].
*   **The Campus Boundary & CGNAT:** The network border filters TTL-expired packets, masking intermediate public routers[cite: 2]. Forcing an ICMP trace revealed an intermediate edge router at `100.99.0.210`, placing it within the `100.64.0.0/10` Carrier-Grade NAT (CGNAT) block[cite: 2]. 
*   **Divergent External Routing:** Traffic to Google bypasses the transit ISP, handing off directly to a Google edge router (`72.14.204.62`)[cite: 2]. General transit (to MIT/Akamai) is routed through Reliance Jio (AS55836) infrastructure at `136.232.148.177`[cite: 2].

---

### Figure 1B: Multi-Location Path (Daksh)
![Room L1 Path](figure1b.svg)

**Analysis of Multi-Location Path (Daksh):**
*   **Two-Tier Campus Access:** Surveying multiple locations revealed two distinct access architectures[cite: 1]. The hostel (L1) on `10.184.0.0/19` reaches the core in two hops, while public areas (L2-L4) on `10.152.192.0/18` require a third hop through an intermediate distribution layer (`10.254.151.x`)[cite: 1]. 
*   **Hierarchical Design:** The extra distribution hop for public areas adds ~1–2 ms of latency without causing broader routing divergence, indicating a design where densely populated zones use an additional aggregation layer[cite: 1].

---

### Synthesis: The Unified Campus Architecture
*   **Core Routing Convergence:** Despite utilizing different hardware, connecting from geographically distinct subnets, and operating on different tiers of the access layer, traffic from all five surveyed locations (Zanskar, L1, L2, L3, and L4) seamlessly converges at the identical primary campus core router (`10.255.109.100`). 
*   **Universal Edge Policy:** Every single path mapped by the team experiences the exact same policy-based routing at the campus boundary. Whether originating from the residential subnets (Zanskar and L1) or the public aggregation layer (L2, L3, L4), IIT Delhi's multi-homed external routing policy (Google direct peering vs. Jio transit) is applied universally across the backbone.