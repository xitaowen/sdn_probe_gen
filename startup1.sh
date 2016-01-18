#!/bin/bash
qemu-kvm -enable-kvm -m 2048 -drive file=/home/byang/vm/openflow/mininet-vm-h1.qcow2,if=virtio -net nic,model=virtio,vlan=2 -net user,vlan=2,hostfwd=tcp::2201-:22 -net nic,model=virtio,macaddr=52:54:00:12:23:10 -net tap,ifname=tap1 -net nic,model=virtio,vlan=1,macaddr=66:54:00:12:33:10 -net tap,vlan=1,ifname=tap11 -nographic

