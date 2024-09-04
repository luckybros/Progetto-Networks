#!/usr/bin/python
import threading
import random
import time
from mininet.log import setLogLevel, info
from mininet.topo import Topo
from mininet.net import Mininet, CLI
from mininet.node import OVSKernelSwitch, Host
from mininet.link import TCLink, Link
from mininet.node import RemoteController #Controller

class Environment(object):
    def __init__(self):
        "Create a network."
        self.net = Mininet(controller=RemoteController, link=TCLink)
        info("*** Starting controller\n")
        c1 = self.net.addController( 'c1', controller=RemoteController) #Controller
        c1.start()
        info("*** Adding hosts and switches\n")
        self.h1 = self.net.addHost('h1', mac ='00:00:00:00:00:01', ip= '10.0.0.1')
        self.h2 = self.net.addHost('h2', mac ='00:00:00:00:00:02', ip= '10.0.0.2')
        self.cpe1 = self.net.addSwitch('s1', cls=OVSKernelSwitch)
        self.cpe2 = self.net.addSwitch('s2', cls=OVSKernelSwitch)
        self.core1 = self.net.addSwitch('s3', cls=OVSKernelSwitch)
        info("*** Adding links\n")  
        self.net.addLink(self.h1, self.cpe1, bw=6, delay='0.0025ms')
        self.path1 = self.net.addLink(self.cpe1, self.core1, bw=3, delay='25ms')
        self.net.addLink(self.core1, self.cpe2, bw=3, delay='25ms')
        self.net.addLink(self.cpe2, self.h2, bw=6, delay='0.0025ms')       
        info("*** Starting network\n")
        self.net.build()
        self.net.start()

...
if __name__ == '__main__':

    setLogLevel('info')
    info('starting the environment\n')
    env = Environment()

    info("*** Running CLI\n")
    CLI(env.net)