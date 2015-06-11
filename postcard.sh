/ovs/bin/ovs-ofctl -O OpenFlow13 del-flows br0
/ovs/bin/ovs-ofctl -O OpenFlow13 add-flow br0  dl_type=0x0800,priority=9,nw_src=0.0.0.0/1,nw_dst=220.9.94.188/31,actions=push_mpls:0x8847,set_mpls_label:0,output:4
/ovs/bin/ovs-ofctl -O OpenFlow13 add-flow br0  dl_type=0x0800,priority=8,nw_src=35.15.251.128/25,nw_dst=35.15.240.0/24,actions=push_mpls:0x8847,set_mpls_label:1,output:4
/ovs/bin/ovs-ofctl -O OpenFlow13 add-flow br0  dl_type=0x0800,priority=7,nw_src=42.21.11.3/32,actions=push_mpls:0x8847,set_mpls_label:2,output:4
/ovs/bin/ovs-ofctl -O OpenFlow13 add-flow br0  dl_type=0x0800,priority=6,nw_src=0.0.0.0/1,nw_dst=229.158.109.0/24,actions=push_mpls:0x8847,set_mpls_label:3,output:4
/ovs/bin/ovs-ofctl -O OpenFlow13 add-flow br0  dl_type=0x0800,priority=5,nw_dst=98.30.236.0/23,actions=push_mpls:0x8847,set_mpls_label:4,output:4
/ovs/bin/ovs-ofctl -O OpenFlow13 add-flow br0  dl_type=0x0800,priority=4,nw_src=34.48.229.0/25,nw_dst=34.48.220.0/24,actions=push_mpls:0x8847,set_mpls_label:5,output:4
/ovs/bin/ovs-ofctl -O OpenFlow13 add-flow br0  dl_type=0x0800,priority=3,nw_src=220.9.105.54/32,nw_dst=220.9.109.120/31,actions=push_mpls:0x8847,set_mpls_label:6,output:4
/ovs/bin/ovs-ofctl -O OpenFlow13 add-flow br0  dl_type=0x0800,priority=2,nw_src=0.0.0.0/1,nw_dst=146.243.112.0/23,actions=push_mpls:0x8847,set_mpls_label:7,output:4
/ovs/bin/ovs-ofctl -O OpenFlow13 add-flow br0  dl_type=0x0800,priority=1,nw_src=43.83.187.0/24,nw_dst=0.0.0.0/1,actions=push_mpls:0x8847,set_mpls_label:8,output:4
