# COL334 Assignment 1 — Part A

**Student:** Daksh
**Device:** Linux laptop, wlan0, eduroam (WPA2 802.1X)
**Dates:** 2026-08-17 to 2026-08-19

---

## A1: Your Path Out

### Locations Surveyed

| # | Location | Date/Time | IP Address | Subnet | Default Gateway | Hop 1 | Wi-Fi Band/CH | Connected AP BSSID |
|---|---|---|---|---|---|---|---|---|
| L1 | Room (hostel) | Aug 19 01:05 | 10.184.30.72 | 10.184.0.0/19 | 10.184.0.1 | 10.184.0.13 | 5 GHz CH 149 | 48:8B:0A:DA:E9 |
| L2 | MusicRoom | Aug 17 21:24 | 10.152.251.125 | 10.152.192.0/18 | 10.152.224.1 | 10.152.224.3 | 5 GHz CH 36 | 88:9C:AD:5B:3A |
| L3 | BSWRoom | Aug 17 22:04 | 10.152.251.125 | 10.152.192.0/18 | 10.152.224.1 | 10.152.224.3 | 5 GHz CH 36 | 88:9C:AD:5A:98 |

Two distinct access subnets observed. L1 on `10.184.0.0/19` reaches backbone in 2 hops. L2/L3 on `10.152.192.0/18` require 3 hops via extra distribution layer `10.254.151.x`. All paths converge at same core routers.

### Topology Diagram

```
                           LAPTOP
                             |
               +-------------+---------------+
               |                             |
        [10.184.0.0/19]              [10.152.192.0/18]
          L1 (Room)                  L2 (MusicRoom)
               |                     L3 (BSWRoom)
          10.184.0.13                     |
          (access gw)              10.152.224.3
               |                   (access gw)
               |                         |
               |                  10.254.151.9/.13
               |                  (distribution LB)
               |                         |
               +-------------+-----------+
                             |
               +-------+-----+------+---------+
               |       |            |          |
          10.254.236  10.254.208  SILENT    10.255.109.100
         .2/.6/.22/.26   .6      (HPC)     (external uplink)
          (4-member    (CSE)       |            |
           ECMP LB)               |        10.255.107.3
               |       |          |            |
          CAMPUS    10.208.20.2  10.113     10.119.233.65
          SERVICES  (CSE server) .30.x       (NKN entry)
               |                               |
      +--------+--------+           +---------+---------+
      |    |    |   |    |           |         |         |
  10.10  10.10 10.7  10.17  10.10  GOOGLE    IITB      MIT
 .211.x  .7.6 .172.2 .8.92 .20.2  8.8.8.8   path      path
 (vhost) (own  (ERP) (lib)  (adm)  via       via NKN   via Jio
         cloud)                   Google     backbone  → Akamai
                                  peering
- - - - - - - - - - - here my evidence stops - - - - - - - - - -
  (grey/inferred beyond last visible traceroute hop)
```

### Three External Paths — Side-by-Side (from Room)

| Hop | Google (8.8.8.8) | IITB (103.21.124.133) | MIT (118.215.155.66) |
|---|---|---|---|
| 1 | 10.184.0.13 (E-1) | 10.184.0.13 (E-1) | 10.184.0.13 (E-1) |
| 2 | 10.255.109.100 (E-2) | 10.255.109.100 (E-2) | 10.255.109.100 (E-2) |
| 3 | 10.255.107.3 (E-3) | 10.255.107.3 (E-3) | 10.255.107.3 (E-3) |
| 4 | 10.119.233.65 (E-3) | 10.119.233.65 (E-3) | 10.119.233.65 (E-3) |
| 5 | 10.1.207.69 | 10.1.207.69 | * * * |
| 6 | 10.1.200.137 | **10.1.207.122** ← diverges | **10.119.234.162** ← diverges |
| 7 | 10.255.237.94 (LB) | 10.120.123.118 | **136.232.148.177** (Jio) (E-4) |
| 8 | 10.152.7.214 | 10.1.207.121 (~97 ms) | * * * |
| 9 | **72.14.204.62** (Google) (E-4) | 10.1.200.137 | * * * |
| 10 | * * * | 10.255.238.122 (LB) | **49.44.117.1** (Akamai) (E-4) |
| 11 | **8.8.8.8** ~101 ms | 10.119.249.49 | * * * unreachable |
| 12 | — | 10.119.249.50 | — |
| 13 | — | **10.10.10.1** (IITB gw) | — |
| 14+ | — | * * * unreachable | — |

**Three exit strategies:**
1. **Google** — NKN peers directly with Google at hop 9 (`72.14.204.62`, whois: Google LLC) (E-4)
2. **IITB** — stays entirely on NKN private backbone (all `10.x.x.x`), 13 visible hops
3. **MIT** — NKN → Reliance Jio (`136.232.148.177`) → Akamai CDN (`49.44.117.1`); content served from India (E-4)

### Campus Internal Routing

| Destination | Resolves To | Dist Router | Hops (Room) | Hops (L2/L3) | Status |
|---|---|---|---|---|---|
| ee.iitd.ac.in | 10.10.211.211 | 236.x | 3 | 4 | Reachable |
| physics.iitd.ac.in | 10.10.211.211 | 236.x | 8* | 9* | Reachable (rate-limited) |
| chemistry.iitd.ac.in | 10.10.211.211 | 236.x | 8* | 9* | Reachable (rate-limited) |
| mech.iitd.ac.in | 10.10.211.211 | 236.x | 8* | 9* | Reachable (rate-limited) |
| textile.iitd.ac.in | 10.10.211.211 | 236.x | 8* | 9* | Reachable (rate-limited) |
| maths.iitd.ac.in | 10.10.211.216 | 236.x | 3 | 4 | Reachable |
| cse.iitd.ac.in | 10.208.20.2 | 208.6 | 3 | 4 | Reachable |
| erp.iitd.ac.in | 10.7.172.2 | 236.x | 3 | 4 | Reachable (!X) |
| owncloud.iitd.ac.in | 10.10.7.6 | 236.x | 3 | 4 | Reachable |
| hpc.iitd.ac.in | 10.113.30.12/14 | SILENT | 3 | 4 | Reachable |
| www.iitd.ac.in | 10.10.211.212 | 236.x | — | — | Blocks ICMP |
| webmail.iitd.ac.in | 10.10.125.176 | 236.x | — | — | Blocks ICMP |
| admissions.iitd.ac.in | 10.10.20.2 | 236.x | — | — | Blocks ICMP |
| library.iitd.ac.in | 10.17.8.92 | 236.x | — | — | Blocks ICMP |

*Hop counts with * are inflated by ICMP rate-limiting on `10.10.211.211` (shared virtual-hosting server), not additional network hops.

---

## A2: Campus Topology

### A2.1 — The Router Hunt

**Full hop table: see `a1_hop_data_notion_v2.csv` (49 rows)**

#### Summary

| Category | Count |
|---|---|
| Unique router/destination IPs | 42 |
| Access gateways | 3 |
| Distribution routers | 8 |
| NKN backbone routers | 14 |
| Public/ISP routers | 3 |
| Campus destinations | 14 |
| External destinations | 3 |
| DNS servers | 4 |

#### Distribution Router Analysis

| Router(s) | Serves | Load Balancing | Evidence |
|---|---|---|---|
| 10.254.236.{2,6,22,26} | All 10.10.x / 10.17.x / 10.7.x | 4-way ECMP per-packet | 40+ traces across 3 locations (E-5) |
| 10.254.208.6 | CSE dept (10.208.x) | None (single) | 3 traces (E-6) |
| 10.254.151.{9,13} | 10.152.x subnet access | 2-way LB | All L2/L3 traces (E-7) |
| 10.255.109.100 | External/internet | None (single) | 6 traces (E-2) |
| SILENT | HPC (10.113.x) | Unknown | Inferred from gap (E-8) |

#### NKN Backbone Mesh Evidence

The same router `10.1.200.137` appears at hop 6 in the Google path and hop 9 in the IITB path. Three routers (`10.255.237.94`, `.238.122`, `.238.254`) form a load-balanced group at the NKN edge, appearing at different hop positions across traces. This proves the NKN is a mesh, not a chain. (E-3)

### A2.2 — The Wireless Layer

#### Physical APs per Location

| Location | Campus APs | Non-Campus | Total SSIDs |
|---|---|---|---|
| L1 — Room | 8 | 1 (CPPLUS CCTV) | 37 |
| L2 — MusicRoom | 2 | 0 | 14 |
| L3 — BSWRoom | 5 | 1 (personal hotspot) | 32 |

#### SSIDs per AP (5 per band)

| SSID | Security | Purpose |
|---|---|---|
| eduroam | WPA2 802.1X | Primary academic |
| IITD_WIFI | WPA2 802.1X | Campus |
| IITD_Secure_GUEST | WPA2 802.1X | Guest |
| IITD_IOT | Open | IoT |
| -- (hidden) | Open | Unknown |

#### AP Vendors

| Location | Primary Vendor (OUI) |
|---|---|
| Room | Alcatel-Lucent/Nokia (48:8B:0A, CC:DB:93, 7C:0E:CE, A4:9B:CD, 84:F1:47, A0:E0:AF) |
| MusicRoom | 88:9C:AD, E4:A4:1C |
| BSWRoom | 88:9C:AD, E4:A4:1C |

#### 2.4 GHz Channel Usage (E-9)

| Channel | L1 Room | L2 MusicRoom | L3 BSWRoom | Assessment |
|---|---|---|---|---|
| 1 | 1 AP | 1 AP | 1 AP | Clean |
| **5** | **1 CCTV** | — | — | Interference (overlaps CH 1 + CH 6) |
| 6 | 1 AP | 1 AP | 2 APs | Moderate |
| 11 | **5 APs** | — | 2 APs | **Congested at Room** |

#### 5 GHz Channel Usage (E-9)

| Channel | L1 Room | L2 MusicRoom | L3 BSWRoom |
|---|---|---|---|
| 36 | — | 1 AP | 1 AP |
| 44 | 1 AP | — | — |
| 48 | — | 1 AP | — |
| 64 | 1 AP | — | — |
| 100 | — | — | 1 AP |
| 132 | — | — | 1 AP |
| 149 | 2 APs | — | — |

No 5 GHz co-channel interference at any location.

#### Cross-Location AP Overlap

Only 1 AP visible from 2 locations: `E4:A4:1C:2E:7A` seen from MusicRoom (32%) and BSWRoom (37%), confirming physical proximity. Zero APs shared between Room and any other location.

#### Non-Campus Devices (E-10)

| BSSID | SSID | Location | Band/CH | Concern |
|---|---|---|---|---|
| 28:18:FD:22:A2:55 | CPPLUS-A255 | Room | 2.4 GHz CH 5 | Overlaps CH 1 and CH 6 |
| AA:7C:C9:97:85:BD | realme x2 | BSWRoom | 5 GHz CH 149 | Minimal impact |

---

## A4: Evidence

### E-1 — Gateway identification

**Who:** Daksh
**When:** 19-08-2026 01:05 (Room), 17-08-2026 21:24 (MusicRoom), 17-08-2026 22:04 (BSWRoom)
**Where:** L1 Room, L2 MusicRoom, L3 BSWRoom
**Artefact:** `ip route | grep default` and `traceroute -4 -n 8.8.8.8` hop 1

Room: `default via 10.184.0.1`, hop 1 = `10.184.0.13`
MusicRoom/BSWRoom: `default via 10.152.224.1`, hop 1 = `10.152.224.3`

**Supports:** A1 topology diagram — access gateways, two-subnet architecture

### E-2 — External uplink router 10.255.109.100

**Who:** Daksh
**When:** 19-08-2026 01:05 (Room), 17-08-2026 22:04 (BSWRoom)
**Where:** L1, L3
**Artefact:** `traceroute -4 -n 8.8.8.8`, `traceroute -4 -n www.iitb.ac.in`, `traceroute -4 -n www.mit.edu` — hop 2 (Room) / hop 3 (BSW)

All three external traces converge at `10.255.109.100` — single external uplink.

**Supports:** A1 external paths, A2.1 distribution router table

### E-3 — NKN backbone mesh topology

**Who:** Daksh
**When:** 19-08-2026 01:05 (Room), 17-08-2026 22:04 (BSWRoom)
**Where:** L1, L3
**Artefact:** `traceroute -4 -n 8.8.8.8` and `traceroute -4 -n www.iitb.ac.in`

`10.1.200.137` at hop 6 (Google path) and hop 9 (IITB path). `10.255.237.94` / `.238.122` / `.238.254` load-balanced group at NKN edge.

**Supports:** A2.1 NKN mesh evidence, A1 external paths

### E-4 — First public hops (whois)

**Who:** Daksh
**When:** 19-08-2026 01:10
**Where:** L1 Room
**Artefact:** `whois 72.14.204.62` → Google LLC. `whois 136.232.148.177` → Reliance Jio. `whois 49.44.117.1` → Reliance Jio / Akamai.

**Supports:** A1 three exit strategies, A1 dashed evidence line

### E-5 — 4-member ECMP core distribution

**Who:** Daksh
**When:** 17-08-2026 22:04 (BSWRoom)
**Where:** L3 BSWRoom
**Artefact:** `traceroute -4 -n ee.iitd.ac.in` hop 3: `10.254.236.22  10.254.236.2  10.254.236.6`

Three different IPs in one hop line. Combined with Room traces showing `.6` and `.26`, proves 4-member cluster.

**Supports:** A2.1 distribution router table, Finding F-2

### E-6 — CSE dedicated distribution router

**Who:** Daksh
**When:** 19-08-2026 01:05 (Room), 17-08-2026 21:24 (MusicRoom), 17-08-2026 22:04 (BSWRoom)
**Where:** L1, L2, L3
**Artefact:** `traceroute -4 -n cse.iitd.ac.in` — hop 2 (Room) / hop 3 (others) = `10.254.208.6`. Never appears in any other trace.

**Supports:** A2.1 distribution router table

### E-7 — 10.152.x distribution layer

**Who:** Daksh
**When:** 17-08-2026 21:24 (MusicRoom), 17-08-2026 22:04 (BSWRoom)
**Where:** L2, L3
**Artefact:** All traceroutes from L2/L3 show hop 2 = `10.254.151.9` or `.13`. Never seen from L1 (Room).

**Supports:** A1 two-tier architecture, Finding F-1

### E-8 — HPC silent distribution router

**Who:** Daksh
**When:** 19-08-2026 01:05 (Room), 17-08-2026 22:04 (BSWRoom)
**Where:** L1, L3
**Artefact:** `traceroute -4 -n hpc.iitd.ac.in` — hop 1 visible, hop 2 = `* * *`, hop 3 = `10.113.30.14` (Room) / `10.113.30.12` (BSW)

Inferred: silent router at hop 2 serves 10.113.x subnet.

**Supports:** A2.1 distribution router table

### E-9 — Wi-Fi survey (3 locations)

**Who:** Daksh
**When:** 19-08-2026 01:05 (Room), 17-08-2026 21:24 (MusicRoom), 17-08-2026 22:04 (BSWRoom)
**Where:** L1, L2, L3
**Artefact:** `nmcli dev wifi list --rescan yes` output. Room: 37 SSIDs, 8 campus APs. MusicRoom: 14 SSIDs, 2 APs. BSWRoom: 32 SSIDs, 5 APs.

**Supports:** A2.2 wireless analysis, Finding F-3

### E-10 — Non-campus CCTV device

**Who:** Daksh
**When:** 19-08-2026 01:05
**Where:** L1 Room
**Artefact:** `nmcli dev wifi list` shows `28:18:FD:22:A2:55 CPPLUS-A255` on 2.4 GHz CH 5 at 42% signal.

**Supports:** A2.2 non-campus devices, Finding F-3

### E-11 — System info snapshots

**Who:** Daksh
**When:** At each location
**Where:** L1, L2, L3
**Artefact:** `ip addr show wlan0`, `ip route`, `resolvectl status`, `iw dev wlan0 link`

Room: 10.184.30.72/19, DNS 10.7.172.202, signal -57 dBm
MusicRoom: 10.152.251.125/18, DNS 10.7.172.202, signal -41 dBm
BSWRoom: 10.152.251.125/18, DNS 10.7.172.202, signal -46 dBm

**Supports:** A1 location table

---

## A5: Three Findings

### F-1 — Two-Tier Campus Access Architecture

**Saw:** Room (10.184.0.0/19) reaches core distribution at hop 2. MusicRoom and BSWRoom (10.152.192.0/18) reach the same core distribution at hop 3, with an extra distribution layer at `10.254.151.{9,13}`. The +1 hop offset is consistent across all 19 traceroute targets. (E-1, E-7)

**Think:** The campus uses a hierarchical access design where larger or more populated areas get an additional aggregation layer. This is standard for large campus networks where a single gateway cannot handle the density. One other explanation I cannot rule out: the 10.254.151.x routers may be doing VLAN trunking or NAC enforcement rather than pure aggregation — the traceroute evidence cannot distinguish these functions.

**Fix:** If the extra hop adds unacceptable latency (it adds ~1–2 ms), the 10.152.x subnet could be re-homed directly under the core 236.x cluster, eliminating one forwarding hop. However, this may break whatever aggregation or policy function the 151.x layer provides.

**Check:** After re-homing, traceroute from a 10.152.x device to any campus service should show the same hop count as from a 10.184.x device (currently differs by exactly 1).

### F-2 — Four-Member ECMP Load-Balanced Core

**Saw:** The core campus distribution uses 4 routers at `10.254.236.{2, 6, 22, 26}`. Traceroute from BSWRoom shows 3 different IPs in a single hop line (per-packet load balancing). Room traces only revealed `.6` and `.26` — the full set was only visible by tracing from multiple subnets. (E-5)

**Think:** Per-packet ECMP means individual TCP flows may traverse different routers, which is fine for stateless forwarding but can cause out-of-order delivery for protocols sensitive to path changes. One other explanation: these could be 4 interfaces on the same physical chassis (a stacked switch or virtual chassis), in which case the "load balancing" is internal to one device and has no reordering risk.

**Fix:** If reordering is observed (check with `ping -c 1000` and counting sequence gaps), switch to per-flow ECMP (hash on 5-tuple) rather than per-packet. This keeps each TCP connection on one path.

**Check:** After switching to per-flow ECMP, repeated traceroutes to the same destination from the same source should show the same 236.x IP for all 3 probes within a single hop, rather than 2–3 different IPs.

### F-3 — 2.4 GHz Channel Congestion with CCTV Interference

**Saw:** At Room, 5 campus APs share 2.4 GHz channel 11 (CC:DB:93, 7C:0E:CE, A4:9B:CD, 7C:0E:CE:15:78, A0:E0:AF). A non-campus CPPLUS CCTV camera (28:18:FD:22:A2:55) operates on channel 5, overlapping both channel 1 and channel 6. At MusicRoom, only 1 AP per channel with zero interference. (E-9, E-10)

**Think:** Five APs on the same channel creates co-channel interference, reducing effective throughput for all clients. The CCTV on CH 5 degrades the remaining two non-overlapping channels (1 and 6), leaving no clean 2.4 GHz option at Room. One other explanation: the APs may implement RRM (Radio Resource Management) and coordinate their transmissions to avoid collisions — the survey only shows channel assignment, not whether the APs are actually interfering at the MAC layer. A packet-level measurement of retransmission rates would be needed to confirm actual performance impact.

**Fix:** Reassign 3 of the 5 APs on CH 11 to channels 1 and 6 (2 on CH 1, 1 on CH 6, 2 on CH 11). Relocate or disable the CCTV camera's Wi-Fi, or move it to a channel that does not overlap campus infrastructure (e.g., CH 11 if APs are rebalanced off it).

**Check:** After rebalancing, a fresh `nmcli dev wifi list` at Room should show no more than 2 campus APs per non-overlapping 2.4 GHz channel, and no non-campus devices on channels 2–5 or 7–10.

---

## Appendix: Methodology

| Tool | Command | Purpose |
|---|---|---|
| traceroute | `traceroute -4 -n <target>` | IPv4 only, skip DNS |
| Wi-Fi survey | `nmcli dev wifi list --rescan yes` | AP discovery |
| System info | `ip addr`, `ip route`, `resolvectl status`, `iw dev wlan0 link` | Config snapshot |
| Automation | `collect.sh <name> <location>` | Timestamped run |

### Targets Traced (19 per location)

**Campus (16):** 10.184.0.1, 10.184.0.13, www.iitd.ac.in, webmail.iitd.ac.in, ee.iitd.ac.in, cse.iitd.ac.in, physics.iitd.ac.in, chemistry.iitd.ac.in, mech.iitd.ac.in, textile.iitd.ac.in, maths.iitd.ac.in, hpc.iitd.ac.in, library.iitd.ac.in, admissions.iitd.ac.in, owncloud.iitd.ac.in, erp.iitd.ac.in

**External (3):** 8.8.8.8, www.iitb.ac.in, www.mit.edu
