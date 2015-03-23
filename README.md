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
|-Makefile


2. miniSAT
Mini sat is a sat solver which is used to solve sat problem. Since it's written by C/C++, a python extention was produced as lib/miniSAT.so. The source code located in minisat/minisat/simp/miniSAT.cc. To use miniSAT.so in python, an example was followed:
    import miniSAT
    miniSAT.solve("p cnf 100 3 1 2 0 -2 3 0 -3 0")
The input is in CNF format, you can see the details in http://www.domagoj-babic.com/uploads/ResearchProjects/Spear/dimacs-cnf.pdf.


