from time import sleep
from mininet.node import Controller
from mininet.net import Containernet
from mininet.cli import CLI
from mininet.log import info, setLogLevel

net = Containernet(controller=Controller)
setLogLevel('info')

net.addController('c0')
s1 = net.addSwitch('s1')
web_server_1 = net.addHost('server1', ip='10.0.0.100')
web_server_2 = net.addHost('server2', ip='10.0.0.101')
client = net.addHost('client', ip='10.0.0.99')

net.addLink(web_server_1, s1)
net.addLink(web_server_2, s1)
net.addLink(client, s1)

net.start()
info(web_server_1.cmd("pipenv run python web_server.py 'Server 1' &"))
info(web_server_2.cmd("pipenv run python web_server.py 'Server 2' &"))
sleep(5)
info(client.cmd("curl 10.0.0.100"))
info(client.cmd("curl 10.0.0.101"))
CLI(net)
net.stop()
