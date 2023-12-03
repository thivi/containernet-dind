from time import sleep
from mininet.node import Controller
from mininet.net import Containernet
from mininet.cli import CLI
from mininet.log import info, setLogLevel
import docker

setLogLevel('info')

client = docker.from_env()
client.images.build(path=".", tag="dind",
                    dockerfile="Dockerfile.dind")

net = Containernet(controller=Controller)

net.addController('c0')
s1 = net.addSwitch('s1')
server = net.addDocker('server',
                       ip='10.0.0.100',
                       dimage="dind",
                       dcmd="dockerd-entrypoint.sh",
                       volumes=["/home/thivi/blog:/home"],
                       privileged=True
                    )
client = net.addHost('client', ip='10.0.0.99')

net.addLink(server, s1)
net.addLink(client, s1)

net.start()
sleep(5)
info(server.cmd("docker build -f ./Dockerfile.webserver -t web-server ."))
info(server.cmd("docker run --rm -d -p 80:80 --name server1 web-server 'Server 1'"))
info(server.cmd("docker run --rm -d -p 8080:80 --name server2 web-server 'Server 2'"))
sleep(3)
info(client.cmd("curl 10.0.0.100:80"))
info(client.cmd("curl 10.0.0.100:8080"))
CLI(net)
net.stop()
