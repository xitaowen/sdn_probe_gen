
all:
	cd minisat;make
	cd pdump/pylibpcap-0.6.4;python setup.py build && python setup.py install
	cd classbench;make
	
	cd header;make
	cp -f header/*.so ./probe/
