
all: header minisat classbench
	cd pdump/pylibpcap-0.6.4;python setup.py build && sudo python setup.py install
	
header: 
	cd header;make
	cp -f header/*.so ./probe/
minisat:
	cd minisat;make
classbench:
	cd classbench;make
