Data Collection Anomaly Note (Day 2, Window 3):
During the execution of the Day 2 Window 3 packet capture, a hardware sleep event temporarily suspended the host machine's network stack. Analysis of the netlab_gen.py logs confirms standard execution from 21:25:38 until 21:31:48. During the traceroute probe to www.mit.edu (T5), the macOS host entered a suspended sleep state, causing the system clock for the Python process to jump to 00:07:58 before timing out.

Despite this OS-level interruption, the concurrent dumpcap process successfully captured approximately 6 minutes of continuous ambient and generated traffic prior to suspension, resulting in a 22MB .pcapng file. This capture file remains highly representative of Busy Hour traffic and contains sufficient TCP, UDP, and TLS flows for the Part B analysis.

🚨 Critical Fixes for A1 (Your Path Out)
Missing Evidence Tags in the Text: The handout has a zero-tolerance policy here: "Every element carries an evidence tag E-1, E-2,... Untagged elements score zero". Your current A1 text in Final_Report.md does not have these.  
PDF
The Fix: You must manually insert (E-1), (E-2), etc., into your A1 paragraphs. For example: "The host was assigned the private IP 10.184.30.65 (E-1) on a /19 subnet (E-1)..."
First Three Public Hops: The handout requires identifying "Every traceroute hop out to the first three public ones, each with its whois owner". Your A1 text mentions Google and Jio, but make sure your actual SVG diagrams (Figure 1A/1B) clearly show hops 1, 2, and 3 on the public internet with their WHOIS owners labeled.  
PDF
The Diagram "Dashed Line": Double-check your SVG files. The rubric strictly requires a dashed line labelled "here my evidence stops" and everything past it must be in grey and labelled "inferred".  
PDF
🚨 Critical Fixes for A3 (The Delay Experiment)
Where are the plots? We wrote perfect text analyzing the data, but the handout explicitly requires three visual plots:  
PDF
A3.1: A plot of RTT against approximate distance.  
PDF
A3.2: A plot of minimum RTT against packet size, with a straight line fitted through each target.  
PDF
A3.3: A plot of RTT against time for both the busy and quiet hour. (You will need to graph the raw ping times over the 5-minute windows for this).  
PDF
The "Median" Trap in A3.1: The handout asks for the median RTT in A3.1. The macOS ping summary block we put in E-5 only outputs min/avg/max/stddev. If you didn't manually calculate the median from the 50 raw packet returns, you should briefly add a note in A3.1 acknowledging that you are using the mean/average as a close approximation for the median.  
PDF
🚨 Critical Fixes for A4 (Evidence)
The Minimum Count: The handout strictly requires "10 to 15 items, numbered E-1 onward". We only built E-1 through E-7. You need at least 3 more evidence blocks to avoid a penalty. These will naturally come from:  
PDF
E-8: Daksh's local network / traceroute proof (since A1 requires both teammates' paths).  
PDF
E-9: Your A2.1 Router Hunt table data.  
PDF
E-10: Your A2.2 Wi-Fi survey data.  
PDF
The E-2 Photo Placard: When you take the photo of the Access Point for E-2, the placard with your roll numbers, date, and location MUST be handwritten in the physical frame. The handout explicitly warns: "Digital overlays don't count".  
PDF
