# sdn_probe_gen
Sections:

1)File structure
2)miniSAT



Content:
1.File structure
sdn_probe_gen
|-lib           library.
|-minisat       sat solver.
|-probe         packet generation algorithms.
|--FaulDete.py  algorithm 1
|--NonaTrou.py  algorithm 2
|--FullAdap.py  algorithm 3
|--SemiAdap.py  algorithm 4
|-Makefile


2. miniSAT
Mini sat is a sat solver which is used to solve sat problem. Since it's written by C/C++, a python extention was produced as lib/miniSAT.so. The source code located in minisat/minisat/simp/miniSAT.cc. To use miniSAT.so in python, an example was followed:
    import miniSAT
    miniSAT.solve("p cnf 100 3 1 2 0 -2 3 0 -3 0")
The input is in CNF format, you can see the details in http://www.domagoj-babic.com/uploads/ResearchProjects/Spear/dimacs-cnf.pdf.

3. Run the Test
Plz cd in to dictionary probe. Run as "example.py input.json".


4. Post Card Processor
Post Card Processor will write a pair of (packet_id, rule_id) into the shared Queue while an experimental packet was detected.
It should be start running b4 experimental packets were sent. It will automatically quit after its father thread quits.

The experimental packet should attach 4 bytes 0x1f1f1f1f just after the head area to specify itself. After that, 2 bytes should be followed to specify the packet id.

Besides, rule installed on switch should attached with action push_mpls:0x8847,set_mpls_label:rule_id,output:(port to foward packet to post card collector h3). An example rule was followed:

ovs-ofctl  -O OpenFlow13 add-flow s2 in_port=1,actions=output:2,push_mpls:0x8847,set_mpls_label:8,output:3


