import SocketServer
import socket
import json

class ServiceDiscoveryServer:

    def __init__(self, ip, port, syncServerPort):
        while self.isOpenUdpPort(ip, port):
            port+=1

        self.syncServerPort = syncServerPort
        server = SocketServer.UDPServer((ip, port), self.getHandlerClass(syncServerPort))
        print "sds opened udp {}:{}".format(ip, port)
        server.serve_forever()

    def isOpenUdpPort(self, ip, port):
        s = socket.socket(type=socket.SOCK_DGRAM)
        try:
            s.bind((ip, port))
            s.close()
            return False
        except IOError:
            return True

    def getHandlerClass(self, syncServerPort):
        class Handler(SocketServer.BaseRequestHandler):
            def handle(self):
                try:
                    request = json.loads(self.request[0].strip())
                    if request['command'] == 'hello':
                        ip, port = self.server.server_address
                        answer = json.dumps({'ip': ip, 'port': syncServerPort})
                        socket = self.request[1]
                        socket.sendto(answer, self.client_address)
                except ValueError:
                    pass
        return Handler