import SocketServer
import socket
import threading
import json

class ServiceDiscoveryServer:

    protocolVersion = '1.0'
    syncServerPort = 0

    def __init__(self, ip, port, syncServerPort):
        while self.isOpenUdpPort(ip, port):
            port+=1

        self.syncServerPort = syncServerPort
        ServiceDiscoveryServer = SocketServer.UDPServer((ip, port), self.handler)
        ServiceDiscoveryServerThread = threading.Thread(ServiceDiscoveryServer.serve_forever)
        ServiceDiscoveryServerThread.start()

    def isOpenUdpPort(self, ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect((ip, int(port)))
            s.shutdown(socket.SHUT_RDWR)
            return True
        except:
            return False

    class handler(SocketServer.BaseRequestHandler):
        def handle(self):
            data = self.request[0].strip()
            try:
                request = json.loads(data)
                if request['command'] == 'hello':
                    ip, port = self.server.server_address
                    answer = dict({'ip': ip, 'port': syncServerPort, 'protocol': protocolVersion})
                    socket = self.request[1]
                    socket.sendto(json.dumps(answer), self.client_address)
            except:
                pass
