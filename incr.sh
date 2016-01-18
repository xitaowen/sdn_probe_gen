#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 logfile"
    echo "Need to generate data first: python generator.py"
    exit 
fi

echo "Log file: "$1
echo "" > $1
echo sudo python Incr.py 0 fault
sudo python Incr.py 0 fault >> $1
#echo sudo python Incr.py 0 full-adapt
#sudo python Incr.py 0 full-adapt >> $1
echo sudo python Incr.py 0 semi-adapt
sudo python Incr.py 0 semi-adapt >> $1
echo sudo python IncrPre.py 0 fault
sudo python IncrPre.py 0 fault >> $1
#echo sudo python IncrPre.py 0 full-adapt
#sudo python IncrPre.py 0 full-adapt >> $1
echo sudo python IncrPre.py 0 semi-adapt
sudo python IncrPre.py 0 semi-adapt >> $1
