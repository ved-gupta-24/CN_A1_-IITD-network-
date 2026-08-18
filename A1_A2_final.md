# COL334 Assignment 1 — Part A: Network Cartography

**Student:** Daksh
**Device:** Linux laptop, wlan0, eduroam (WPA2 802.1X)
**Dates:** 2026-08-17 to 2026-08-19

---

## A1: Network Map

### Locations Surveyed

| # | Location | Date/Time | IP Address | Subnet | Default Gateway | Traceroute Hop 1 | Wi-Fi Band/CH | Connected AP BSSID |
|---|---|---|---|---|---|---|---|---|
| L1 | Room (hostel) | Aug 19, 01:05 | 10.184.30.72 | 10.184.0.0/19 | 10.184.0.1 | 10.184.0.13 | 5 GHz / CH 149 | 48:8B:0A:DA:E9 |
| L2 | MusicRoom | Aug 17, 21:24 | 10.152.251.125 | 10.152.192.0/18 | 10.152.224.1 | 10.152.224.3 | 5 GHz / CH 36 | 88:9C:AD:5B:3A |
| L3 | BSWRoom | Aug 17, 22:04 | 10.152.251.125 | 10.152.192.0/18 | 10.152.224.1 | 10.152.224.3 | 5 GHz / CH 36 | 88:9C:AD:5A:98 |
| L4 | LH510 (lecture hall) | Aug 17, 11:57 | 10.152.255.148 | 10.152.192.0/18 | 10.152.224.1 | 10.152.224.3 | 5 GHz / CH 36 | 70:BD:96:6E:8E |

**Key observation:** The campus has (at least) two access subnets. L1 is on `10.184.0.0/19` and reaches the backbone in 2 hops. L2–L4 are on `10.152.192.0/18` and require 3 hops (an extra distribution layer at `10.254.151.x`). Despite this, all paths converge at the same core routers — the extra hop adds ~1–2 ms but no routing divergence.

### Topology Diagram

```
                           LAPTOP
                             |
               +-------------+---------------+
               |                             |
        [10.184.0.0/19]              [10.152.192.0/18]
          L1 (Room)                L2, L3, L4
               |                             |
          10.184.0.13                   10.152.224.3
          (access gateway)              (access gateway)
               |                             |
               |                     10.254.151.9 / .13
               |                     (distribution, load-balanced)
               |                             |
               +-------------+---------------+
                             |
               +-------+-----+------+--------+
               |       |            |         |
          10.254.236  10.254.208  SILENT   10.255.109.100
         .2/.6/.22/.26   .6      (HPC)    (external uplink)
          (4-member    (CSE)       |           |
           ECMP LB)               |       10.255.107.3
               |       |         |           |
          CAMPUS    10.208.20.2  10.113    10.119.233.65
          SERVICES  (CSE server) .30.x      (NKN entry)
               |                              |
      +--------+--------+          +---------+---------+
      |    |    |   |    |          |         |         |
  10.10  10.10 10.7  10.17  10.10  GOOGLE    IITB      MIT
 .211.x  .7.6 .172.2 .8.92 .20.2  8.8.8.8   path      path
 (vhost) (own  (ERP) (lib)  (adm)  via       via NKN   via Jio
         cloud)                   Google     backbone  → Akamai
                                  peering
```

### Three External Paths — Side-by-Side (from Room / L1)

| Hop | Google (8.8.8.8) | IITB (103.21.124.133) | MIT (118.215.155.66) |
|---|---|---|---|
| 1 | 10.184.0.13 | 10.184.0.13 | 10.184.0.13 |
| 2 | 10.255.109.100 | 10.255.109.100 | 10.255.109.100 |
| 3 | 10.255.107.3 | 10.255.107.3 | 10.255.107.3 |
| 4 | 10.119.233.65 | 10.119.233.65 | 10.119.233.65 |
| 5 | 10.1.207.69 | 10.1.207.69 | `* * *` |
| 6 | 10.1.200.137 | **10.1.207.122** ← diverges | **10.119.234.162** ← diverges |
| 7 | 10.255.237.94 (LB) | 10.120.123.118 | **136.232.148.177** (Jio) |
| 8 | 10.152.7.214 | 10.1.207.121 (~97ms) | `* * *` |
| 9 | **72.14.204.62** (Google) | 10.1.200.137 | `* * *` |
| 10 | `* * *` | 10.255.238.122 (LB) | **49.44.117.1** (Akamai) |
| 11 | **8.8.8.8** (~101ms) | 10.119.249.49 | `* * *` ... unreachable |
| 12 | — | 10.119.249.50 | — |
| 13 | — | **10.10.10.1** (IITB gw) | — |
| 14+ | — | `* * *` ... unreachable | — |

**Exit strategies:**
1. **Google** — NKN peers directly with Google at hop 9 (`72.14.204.62`)
2. **IITB** — stays entirely on NKN private backbone (all `10.x.x.x`), 13 visible hops
3. **MIT** — NKN → Reliance Jio (`136.232.148.177`) → Akamai CDN (`49.44.117.1`); content served from India

### Campus Internal Routing

| Destination | DNS Resolves To | Distribution Router | Hops (Room) | Hops (L2/L3) | Status |
|---|---|---|---|---|---|
| ee.iitd.ac.in | 10.10.211.211 | 236.x cluster | 3 | 4 | Reachable |
| physics.iitd.ac.in | 10.10.211.211 | 236.x cluster | 8* | 9* | Reachable (rate-limited) |
| chemistry.iitd.ac.in | 10.10.211.211 | 236.x cluster | 8* | 9* | Reachable (rate-limited) |
| mech.iitd.ac.in | 10.10.211.211 | 236.x cluster | 8* | 9* | Reachable (rate-limited) |
| textile.iitd.ac.in | 10.10.211.211 | 236.x cluster | 8* | 9* | Reachable (rate-limited) |
| maths.iitd.ac.in | 10.10.211.216 | 236.x cluster | 3 | 4 | Reachable |
| cse.iitd.ac.in | 10.208.20.2 | 208.6 (CSE own) | 3 | 4 | Reachable |
| erp.iitd.ac.in | 10.7.172.2 | 236.x cluster | 3 | 4 | Reachable (!X) |
| owncloud.iitd.ac.in | 10.10.7.6 | 236.x cluster | 3 | 4 | Reachable |
| hpc.iitd.ac.in | 10.113.30.12/14 | SILENT | 3 | 4 | Reachable |
| www.iitd.ac.in | 10.10.211.212 | 236.x cluster | — | — | Blocks ICMP |
| webmail.iitd.ac.in | 10.10.125.176 | 236.x cluster | — | — | Blocks ICMP |
| admissions.iitd.ac.in | 10.10.20.2 | 236.x cluster | — | — | Blocks ICMP |
| library.iitd.ac.in | 10.17.8.92 | 236.x cluster | — | — | Blocks ICMP |

*Hop counts marked with `*` are inflated by ICMP rate-limiting on the shared server `10.10.211.211`, not additional network hops. The server hosts 5 departments via virtual hosting and throttles ICMP responses.

---

## A2.1: Hop Table

See companion file: **`a1_hop_data_final.csv`** (48 entries)

### Summary Statistics

| Category | Count |
|---|---|
| Unique router/destination IPs | 44 |
| Access gateways | 3 (10.184.0.13, 10.152.224.3, 10.184.0.1 VIP) |
| Distribution routers | 8 (236.x×4, 208.6, 151.x×2, 109.100) |
| NKN backbone routers | 14 |
| Public/ISP routers | 3 (Google, Jio, Akamai) |
| Campus destinations | 14 |
| External destinations | 3 |
| DNS servers | 4 |

### Distribution Router Analysis

| Router(s) | Serves | Load Balancing | Evidence Count |
|---|---|---|---|
| 10.254.236.{2,6,22,26} | All `10.10.x`, `10.17.x`, `10.7.x` services | 4-way ECMP (per-packet) | 40+ traces across 4 locations |
| 10.254.208.6 | CSE dept (`10.208.x`) | None (single) | 4 traces (1 per location) |
| 10.254.151.{9,13} | 10.152.x subnet access | 2-way load-balanced | All L2/L3/L4 traces |
| 10.255.109.100 | External/internet traffic | None (single) | 12 traces (3 external × 4 locations) |
| SILENT | HPC (`10.113.x`) | Unknown | Inferred from gap in 4 traces |

### NKN Backbone Load Balancing

Three routers at the NKN edge serve as a load-balanced group:
- `10.255.237.94`
- `10.255.238.122`
- `10.255.238.254`

These appear at different hop positions across traces (hop 7–11), confirming **mesh topology** within the NKN backbone. The same router `10.1.200.137` appears at hop 6 in the Google path and hop 9 in the IITB path, proving the NKN is not a simple chain but a **mesh with multiple paths**.

---

## A2.2: Wireless Survey Analysis

### Physical APs per Location

| Location | Campus APs | Non-Campus Devices | Total SSIDs Visible |
|---|---|---|---|
| L1 — Room | 8 | 1 (CPPLUS CCTV) | 37 |
| L2 — MusicRoom | 2 | 0 | 14 |
| L3 — BSWRoom | 5 | 1 (personal hotspot) | 32 |
| L4 — LH510 | 2 | 2 (personal hotspots) | 14 |

### SSIDs per AP

Each campus AP broadcasts **5 SSIDs per band** (2.4 GHz + 5 GHz):

| SSID | Security | Purpose |
|---|---|---|
| `eduroam` | WPA2 802.1X | Primary academic network |
| `IITD_WIFI` | WPA2 802.1X | Campus Wi-Fi |
| `IITD_Secure_GUEST` | WPA2 802.1X | Guest access |
| `IITD_IOT` | Open | IoT devices |
| `--` (hidden) | Open | Unknown purpose |

### AP Vendors by Location

| Location | Primary Vendor (MAC OUI) | Model Indicators |
|---|---|---|
| Room | Alcatel-Lucent/Nokia (48:8B:0A, CC:DB:93, 7C:0E:CE, A4:9B:CD, 84:F1:47, A0:E0:AF) | 130–195 Mbit/s (2.4G), 1170 Mbit/s (5G) |
| MusicRoom | 88:9C:AD, E4:A4:1C | 195–260 Mbit/s (2.4G), 1170 Mbit/s (5G) |
| BSWRoom | 88:9C:AD, E4:A4:1C | Same as MusicRoom |
| LH510 | 70:BD:96 | 260 Mbit/s (2.4G), 1170 Mbit/s (5G), supports Wi-Fi 6 (HE) |

### Channel Usage — 2.4 GHz

| Channel | L1 Room | L2 MusicRoom | L3 BSWRoom | L4 LH510 | Assessment |
|---|---|---|---|---|---|
| 1 | 1 AP | 1 AP | 1 AP | 1 AP | Clean |
| **5** | **1 CCTV** | — | — | — | **Interference** (overlaps CH1+CH6) |
| 6 | 1 AP | 1 AP | 2 APs | — | Moderate |
| 11 | **5 APs** | — | 2 APs | 1 AP | **Congested at Room** |

### Channel Usage — 5 GHz

| Channel | L1 Room | L2 MusicRoom | L3 BSWRoom | L4 LH510 |
|---|---|---|---|---|
| 36 | — | 1 AP | 1 AP | 1 AP |
| 44 | 1 AP | — | — | — |
| 48 | — | 1 AP | — | — |
| 64 | 1 AP | — | — | — |
| 100 | — | — | 1 AP | — |
| 132 | — | — | 1 AP | — |
| 149 | 2 APs | — | — | — |

5 GHz is well-planned — no co-channel interference at any location.

### Cross-Location AP Overlap

| Shared AP (MAC prefix) | Locations | Signal |
|---|---|---|
| E4:A4:1C:2E:7A | MusicRoom (32%) + BSWRoom (37%) | Confirms physical proximity |

No other APs are visible from multiple survey locations. Room shares zero APs with any other location (consistent with being on a different subnet and different part of campus).

### Non-Campus Devices

| BSSID | SSID | Location | Band/CH | Security | Concern |
|---|---|---|---|---|---|
| 28:18:FD:22:A2:55 | CPPLUS-A255 | Room | 2.4 GHz CH 5 | WPA2 | Overlaps CH 1 and CH 6 |
| AA:7C:C9:97:85:BD | realme x2 | BSWRoom | 5 GHz CH 149 | WPA2 | Personal hotspot, minimal impact |
| 16:9E:DA:94:09:70 | OnePlus Nord CE 3 Lite 5G | LH510 | 5 GHz CH 48 | WPA2/WPA3 | Personal hotspot |
| 46:C2:EC:A0:8B:8A | Redmi Note 13 5G | LH510 | 5 GHz CH 36 | WPA2 | Co-channel with main campus AP |

---

## A5: Three Findings

### Finding 1: Two-Tier Campus Access Architecture

The IITD campus network uses at least two distinct access subnets with different hop depths to the core. Devices on `10.184.0.0/19` (Room/hostel) reach the core distribution in **2 hops**, while devices on `10.152.192.0/18` (MusicRoom, BSWRoom, LH510) require **3 hops** through an extra distribution layer at `10.254.151.{9,13}`. Despite this asymmetry, all paths converge at the same backbone routers — the extra hop adds only ~1–2 ms latency and no routing divergence. This indicates a hierarchical design where larger or more populated areas get an additional aggregation layer.

**Evidence:**
- Room → ee.iitd.ac.in = 3 hops: `10.184.0.13` → `10.254.236.26` → `10.10.211.211`
- MusicRoom → ee.iitd.ac.in = 4 hops: `10.152.224.3` → `10.254.151.9` → `10.254.236.6` → `10.10.211.211`
- Consistent +1 hop offset verified across all 19 traceroute targets

### Finding 2: Four-Member ECMP Load-Balanced Core

The campus core distribution uses a **4-member Equal-Cost Multi-Path (ECMP)** load-balanced cluster at `10.254.236.{2, 6, 22, 26}`. Traceroute's 3-probe-per-hop design reveals per-packet load balancing: all four IPs appear interleaved across probes within a single traceroute run. Importantly, this full cluster was only visible by tracing from multiple locations — Room traces only revealed `.6` and `.26`, while MusicRoom/BSWRoom traces additionally exposed `.2` and `.22`.

**Evidence:**
- `traceroute -4 -n ee.iitd.ac.in` from BSWRoom, hop 3: `10.254.236.22  10.254.236.2  10.254.236.6` — three different routers in one hop line
- `traceroute -4 -n erp.iitd.ac.in` from MusicRoom, hop 3: `10.254.236.26  10.254.236.22  10.254.236.26`
- Room traces only show `.6` and `.26` (never `.2` or `.22`)

### Finding 3: 2.4 GHz Channel Congestion with CCTV Interference at Room Location

At the Room location, **five campus APs** share 2.4 GHz channel 11, creating severe co-channel interference potential. Compounding this, a non-campus CPPLUS CCTV camera (`28:18:FD:22:A2:55`, SSID `CPPLUS-A255`) operates on the non-standard channel 5. In 802.11, channels 1, 6, and 11 are the only non-overlapping options in 2.4 GHz; channel 5 overlaps with both channels 1 and 6, effectively degrading **all three** usable channels at this location. By contrast, MusicRoom and LH510 show clean spectrum with only 1–2 APs per channel and zero non-campus interference sources. The 5 GHz band is well-managed across all locations with no co-channel conflicts.

**Evidence:**
- Room 2.4 GHz CH 11: CC:DB:93, 7C:0E:CE, A4:9B:CD (×2 SSIDs visible), A0:E0:AF — all at 29–47% signal
- Room 2.4 GHz CH 5: 28:18:FD:22:A2:55 "CPPLUS-A255" at 42% signal
- MusicRoom 2.4 GHz: 1 AP on CH 1, 1 AP on CH 6, zero non-campus devices
- LH510 2.4 GHz: 1 AP on CH 1, 1 AP on CH 11, zero non-campus devices (2 personal hotspots on 5 GHz only)

---

## Appendix: Data Collection Methodology

| Tool | Command | Purpose |
|---|---|---|
| traceroute | `traceroute -4 -n <target>` | IPv4-only, skip DNS, 19 targets per location |
| Wi-Fi survey | `nmcli dev wifi list --rescan yes` | AP discovery with fresh scan |
| System info | `ip addr show wlan0`, `ip route`, `resolvectl status`, `iw dev wlan0 link` | Network config at each location |
| All commands | Automated via `collect.sh <location> <name>` | Timestamped output in `data/<name>_<location>_<timestamp>/` |

### Targets Traced (19 total)

**Campus (16):** 10.184.0.1, 10.184.0.13, www.iitd.ac.in, webmail.iitd.ac.in, ee.iitd.ac.in, cse.iitd.ac.in, physics.iitd.ac.in, chemistry.iitd.ac.in, mech.iitd.ac.in, textile.iitd.ac.in, maths.iitd.ac.in, hpc.iitd.ac.in, library.iitd.ac.in, admissions.iitd.ac.in, owncloud.iitd.ac.in, erp.iitd.ac.in

**External (3):** 8.8.8.8, www.iitb.ac.in, www.mit.edu
