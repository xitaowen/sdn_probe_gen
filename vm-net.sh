#!/bin/bash
# create and configure the bridges
brctl addbr br1
brctl addbr br2
brctl addbr br3
brctl addif br1 eth1
brctl addif br2 eth2
brctl addif br3 eth3
# create the TAPs device for the virtual machines
tunctl -u root -t tap1
tunctl -u root -t tap2
tunctl -u root -t tap3
ip link set tap1 up
ip link set br1 up
ip link set eth1 up
brctl addif br1 tap1
ip link set tap2 up
ip link set br2 up
ip link set eth2 up
brctl addif br2 tap2
ip link set tap3 up
ip link set br3 up
ip link set eth3 up
brctl addif br3 tap3
# create and configure the control bridge
brctl addbr br-ctl
ip link set br-ctl up
tunctl -u root -t tap11
tunctl -u root -t tap22
tunctl -u root -t tap33
ip link set tap11 up
ip link set tap22 up
ip link set tap33 up
brctl addif br-ctl tap11
brctl addif br-ctl tap22
brctl addif br-ctl tap33
ifconfig br-ctl 10.0.66.1/24
# PYTHONPATH=. ./bin/ryu-manager --ofp-tcp-listen-port 6634 --verbose ryu/app/simple_switch.py
