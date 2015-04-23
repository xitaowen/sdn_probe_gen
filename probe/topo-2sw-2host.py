"""Custom topology example

Two directly connected switches plus a host for each switch:

   3 switches, 4 hosts

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        leftHost = self.addHost( 'h0' )
        rightHost = self.addHost( 'h2' )
        middleHost = self.addHost( 'h1' )
        postcardHost = self.addHost( 'h3')
        leftSwitch = self.addSwitch( 's0' )
        rightSwitch = self.addSwitch( 's2' )
        middleSwitch = self.addSwitch( 's1' )


        # Add links
        self.addLink( leftHost, leftSwitch )
        self.addLink( leftSwitch, middleSwitch )
        self.addLink( middleHost, middleSwitch )
        self.addLink( middleSwitch, rightSwitch )
        self.addLink( rightSwitch, rightHost )
        self.addLink( leftSwitch, postcardHost )
        self.addLink( middleSwitch, postcardHost )
        self.addLink( rightSwitch, postcardHost )


topos = { 'mytopo': ( lambda: MyTopo() ) }
