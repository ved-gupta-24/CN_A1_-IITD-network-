# COL334 Assignment 1: Master Submission Checklist

## Phase 1: Setup & Preliminaries
- [ ] **Find Default Gateway (T1):** Run `netstat -nr | grep default` (macOS) to find your gateway IP[cite: 1]. Remember to check this every time you change physical locations[cite: 1].
- [ ] **Verify Capture Tools:** Ensure `dumpcap` or `tshark` (via Wireshark) is installed and working on both teammates' laptops before starting Part B[cite: 1].
- [ ] **Coordinate Capture Times:** Agree with your partner on specific 10-minute windows for the Part B captures (both teammates must capture within 15 minutes of each other)[cite: 1].

## Phase 2: Part A — Cartography (50 Marks)[cite: 1]

### A1: Your Path Out
- [x] **Traceroute Data:** Run traceroutes to the open internet (at least 3 public hops)[cite: 1].
- [x] **Whois Lookups:** Run `whois` on the first three public hops[cite: 1].
- [ ] **Take Photo Evidence:** Photograph the nearest AP or wall port[cite: 1]. **Crucial:** Must include a handwritten placard in the frame with your roll numbers, date, and location (digital overlays score zero)[cite: 1].
- [ ] **Draw the Diagram (Joint):**
    - [ ] Show both teammates' paths side-by-side (merging/diverging where applicable)[cite: 1].
    - [ ] Include device, interface, AP/port, IP, T1 gateway, and DNS resolver[cite: 1].
    - [ ] Identify where the packet crosses the IIT Delhi boundary[cite: 1].
    - [ ] Draw a dashed line labeled "here my evidence stops"[cite: 1].
    - [ ] Mark everything past the dashed line in grey and label it "inferred"[cite: 1].
- [ ] **Tag Evidence:** Add `E-X` tags to every element on the diagram (untagged elements score zero)[cite: 1].

### A2: Campus Topology
- [x] **A2.1 (Router Hunt):** Trace to 10-15 destinations (campus and non-campus)[cite: 1].
    - [x] Create the Hop Table (IP, traces it appears in, position, RTT, best guess at role)[cite: 1].
    - [x] Draw the internal topology graph (routers as nodes, adjacencies as edges)[cite: 1].
- [x] **A2.2 (Wireless Layer):** Run a Wi-Fi survey from 3 different campus locations[cite: 1].
    - [x] Record SSID, BSSID, band, channel, and signal strength[cite: 1].
    - [x] Answer the 3 analysis questions (distinct APs, widespread vs local SSIDs, overlapping channels)[cite: 1].
- [ ] **A2.3 (Class Map):** Add your router hops and AP data to the shared spreadsheet (`COL334_A1_Campus_Map.xlsx`)[cite: 1].
    - [ ] Verify two rows submitted by other teams (Confirm, Contradict, or Couldn't reach) and log the results[cite: 1].

### A3: The Delay Experiment
- [ ] **A3.1 (Where does the time go?):**
    - [x] Table of min/median/max RTT for T1 through T5[cite: 1].
    - [ ] **PLOT:** RTT vs. Approximate Distance[cite: 1].
    - [ ] Answer the 3 analysis questions[cite: 1].
- [ ] **A3.2 (Transmission Delay):**
    - [x] Table of min RTT to T1 and T3 across packet sizes (64, 256, 512, 1024, 1400)[cite: 1].
    - [ ] **PLOT:** Minimum RTT vs. Packet Size (two lines, fitted with a straight line)[cite: 1].
    - [ ] Answer the 3 analysis questions[cite: 1].
- [ ] **A3.3 (Watch a queue fill):**
    - [x] Table of 5-minute continuous ping data for Busy Hour and Quiet Hour[cite: 1].
    - [ ] **PLOT:** RTT vs. Time for both hours on the same graph[cite: 1].
    - [ ] Answer the 2 analysis questions[cite: 1].

### A4 & A5: Evidence and Findings
- [ ] **A4 (Evidence Appendix):** Compile 10 to 15 tagged items (`E-1` onward)[cite: 1].
    - [ ] Format strictly as: Who, When, Where, [the artefact], Supports[cite: 1].
    - [ ] Ensure command outputs are verbatim (not tidied up)[cite: 1].
- [ ] **A5 (Three Findings):** Document exactly 3 things that could be better (at least 1 from delay, 1 from topology)[cite: 1].
    - [ ] Format strictly as: Saw, Evidence, Think (+ 1 other explanation), Fix, Check[cite: 1].

## Phase 3: Part B — The Stakeout (35 Marks)[cite: 1]

### Data Collection (Both Teammates)
- [ ] **Day 1 Captures:**
    - [ ] W1 (08:00 - 11:00): Run 10-min capture + `netlab_gen.py` script[cite: 1].
    - [ ] W2 (13:00 - 16:00): Run 10-min capture + script[cite: 1].
    - [ ] W3 (20:00 - 23:00): Run 10-min capture + script[cite: 1].
- [ ] **Day 2 Captures:** Repeat W1, W2, W3[cite: 1].
- [ ] **Log Appendices:** Fill out both "Capture log" tables from the handout appendix (Where and when, What you were connected to)[cite: 1].

### B1: Two Days, Two Devices
- [ ] **PL-1 (Line Plot):** Plot Window vs. RTT median and p95 to T1, T3 (one line per teammate)[cite: 1].
- [ ] **PL-2 (Bar Chart):** Plot Window band vs. RTT p95 (grouped bars per teammate)[cite: 1].
- [ ] **Analysis:** Answer Q1 (worst window) and Q2 (biggest non-workload consumer)[cite: 1].

### B2: The Hunt
- [ ] **Find Anomalies:** Hunt through pcaps for the 3 to 6 planted anomalies[cite: 1].
- [ ] **Anomaly Table:** For each finding, log: What it is, File, Frame, Value, Display filter, Frames returned[cite: 1].
- [ ] **Script Outputs:** Record `ROLL`, `SEED_TAG`, `TOKEN`, and `INTERVAL` for both teammates[cite: 1].

### B3: Argue Against Yourself
- [ ] **Write Prose (400-600 words):** Answer the 3 specific prompts (hardest anomaly to spot at scale, the innocent case for one anomaly, operator vs. local view)[cite: 1].

## Phase 4: Final Compilation & Submission Checks

### Formatting & Naming
- [ ] **Roll Number Formatting:** Sort roll numbers alphabetically (e.g., `2024CS10057_2024CS10093`)[cite: 1].
- [ ] **Page 1 Requirement:** Ensure both names and roll numbers are on the first page of *both* reports (Part A and Part B)[cite: 1].

### Part A Submission (PDF)
- [ ] Contains all sections (A1 through A5)[cite: 1].
- [ ] Maximum 20 pages[cite: 1].
- [ ] Filename: `A1_<ROLL1>_<ROLL2>_partA.pdf`[cite: 1].

### Part B Submission (ZIP)
- [ ] Zip structure is strictly: `report.pdf`, `captures/` folder, `logs/` folder, `analysis/` folder[cite: 1].
- [ ] `captures/` contains exactly 12 raw `.pcapng` files named `<ROLL>_D<d>_W<w>.pcapng`[cite: 1].
- [ ] `logs/` contains exactly 12 script log files named `netlab_gen_<ROLL>_D<d>_W<w>.log`[cite: 1].
- [ ] No hidden files (`.DS_Store`, `__MACOSX`)[cite: 1].
- [ ] Filename: `A1_<ROLL1>_<ROLL2>_partB.zip`[cite: 1].
