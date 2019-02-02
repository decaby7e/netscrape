#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import OVSController
import os


class SingleSwitchTopo(Topo):
    # Single switch connected to n hosts
    def build(self, n=2):
        switch = self.addSwitch('s1')
        # Python's range(N) generates 0..N-1
        for h in range(n):
            host = self.addHost('h%s' % (h + 1))
            self.addLink(host, switch)


def simpleTest():
    # Create network
    topo = SingleSwitchTopo(n=2)
    net = Mininet(topo=topo, controller=OVSController)
    net.start()

    # Define hosts & switch
    h1 = net.get('h1')
    h2 = net.get('h2')
    s1 = net.get('s1')

    # BEGIN COMMANDS

    print ">> Starting frpc on s1... (h2:5161 --> axon:6161)"
    s1.cmd('/home/labuser/Mininet/class-testing/apps/frp/frpc -c /home/labuser/Mininet/class-testing/apps/frp/frpc.ini')

    #print ">> Starting REMOTE_APP on axon.ddns.net:22..."
    #os.system("ssh -t root@axon.ddns.net 'REMOTE_APP'")

    print ">> Starting trafficGenServer on h2... (h2:5161)"
    h2.cmd('python /home/labuser/Mininet/class-testing/scripts/trafficGenServer.py')

    print ">> Beginning pcap capture on s1..."
    s1.cmd('/home/labuser/Mininet/class-testing/scripts/tsharkCaptureMn.sh')

    print ">> Starting trafficGenClient on h1... (h1:5161)"
    h1.cmd('python /home/labuser/Mininet/class-testing/scripts/trafficGenClient.py')

    # END COMMANDS

    net.stop()


if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()
