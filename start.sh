#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 logfile"
    echo "Need to generate data first: python generator.py"
    exit 
fi

echo "Log file: "$1
echo "" > $1
echo sudo python Test.py 0 fault
sudo python Test.py 0 fault >> $1
echo sudo python Test.py 1 fault
sudo python Test.py 1 fault >> $1
echo sudo python Test.py 2 fault
sudo python Test.py 2 fault >> $1
echo sudo python Test.py 0 none-adapt
#sudo python Test.py 0 none-adapt >> $1
echo sudo python Test.py 1 none-adapt
#sudo python Test.py 1 none-adapt >> $1
echo sudo python Test.py 2 none-adapt
#sudo python Test.py 2 none-adapt >> $1
echo sudo python Test.py 0 full-adapt
sudo python Test.py 0 full-adapt >> $1
echo sudo python Test.py 1 full-adapt
sudo python Test.py 1 full-adapt >> $1
echo sudo python Test.py 2 full-adapt
sudo python Test.py 2 full-adapt >> $1
echo sudo python Test.py 0 semi-adapt
sudo python Test.py 0 semi-adapt >> $1
echo sudo python Test.py 1 semi-adapt
sudo python Test.py 1 semi-adapt >> $1
echo sudo python Test.py 2 semi-adapt
sudo python Test.py 2 semi-adapt >> $1
