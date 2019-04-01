#!/usr/bin/python

## Example topology for containernet
## Created by Jorge Lopez 

"""
This is a simple example of a Containernet custom topology.
"""
from mininet.net import Containernet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
import sys
setLogLevel('info')

net = Containernet()
info('*** Adding controller\n')
c0 = RemoteController( 'c0' )
net.addController(c0)
info('*** Adding docker containers\n')
h1 = net.addDocker('h1', ip='10.0.0.251', mac='9a:d8:73:d8:90:6a', dimage="mysql:5.7", environment={"MYSQL_DATABASE": "exampledb", "MYSQL_USER": "exampleuser", "MYSQL_PASSWORD": "examplepass", "MYSQL_RANDOM_ROOT_PASSWORD": "1" })
h2 = net.addDocker('h2', ip='10.0.0.252', mac='9a:d8:73:d8:90:6b', dimage="wordpress:latest", port_bindings={8080:80}, publish_all_ports=True)
h3 = net.addDocker('h3', ip='10.0.0.253', mac='9a:d8:73:d8:90:6c', dimage="lab-api", port_bindings={8888:5000}, publish_all_ports=True)
h4 = net.addDocker('h4', ip='10.0.0.254', mac='9a:d8:73:d8:90:6d', dimage="lab-web", port_bindings={8081:80}, publish_all_ports=True)
info('*** Adding switches\n')
s1 = net.addSwitch('s1')
s2 = net.addSwitch('s2')
s3 = net.addSwitch('s3')
s4 = net.addSwitch('s4')
info('*** Creating links\n')
net.addLink( h1, s1, 1, 1 )
net.addLink( h2, s2, 1, 1 )
net.addLink( h3, s3, 1, 1 )
net.addLink( h4, s4, 1, 1 )
net.addLink( s1, s2, 2, 2 )
net.addLink( s1, s3, 3, 2 )
net.addLink( s2, s3, 3, 3 )
net.addLink( s2, s4, 4, 2 )
net.addLink( s3, s4, 4, 3 )
info('*** Starting network\n')
net.start()
info('*** Running CLI\n')
CLI(net)
net.stop()
