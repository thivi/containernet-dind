from mininet.node import Controller
from mininet.net import Containernet
from mininet.cli import CLI
from mininet.log import info, setLogLevel
import docker

setLogLevel('info')

client = docker.from_env()
client.images.build(path=".", tag="web-server",
                    dockerfile="Dockerfile.webserver")

net = Containernet(controller=Controller)

net.addController('c0')
s1 = net.addSwitch('s1')
web_server_1 = net.addDocker('server1', ip='10.0.0.100', dimage="web-server", dcmd="python web_server.py 'Server 1'")
web_server_2 = net.addDocker('server2', ip='10.0.0.101', dimage="web-server", dcmd="python web_server.py 'Server 2'")
client = net.addHost('client', ip='10.0.0.99')

net.addLink(web_server_1, s1)
net.addLink(web_server_2, s1)
net.addLink(client, s1)

net.start()
info(client.cmd("curl 10.0.0.100"))
info(client.cmd("curl 10.0.0.101"))
CLI(net)
net.stop()
