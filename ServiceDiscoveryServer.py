import SocketServer
import socket
import json

class ServiceDiscoveryServer:

    protocolVersion = '1.0'
    syncServerPort = 0

    def __init__(self, ip, port, syncServerPort):
        while self.isOpenUdpPort(ip, port):
            port+=1

        self.syncServerPort = syncServerPort
        server = SocketServer.TCPServer((ip, port), self.handler)
#        server = SocketServer.UDPServer((ip, port), self.handler)
        server.serve_forever()

    def isOpenUdpPort(self, ip, port):
        s = socket.socket()
#        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect((ip, int(port)))
            s.shutdown(socket.SHUT_RDWR)
            return True
        except:
            return False

    class handler(SocketServer.BaseRequestHandler):
        def handle(self):
            data = self.request.recv(1024)
            try:
                request = json.loads(data)
                if request['command'] == 'hello':
                    ip, port = self.server.server_address
                    answer = dict({'ip': ip, 'port': syncServerPort, 'protocol': protocolVersion})
                    self.request.send(json.dumps(answer))
            except:
                pass

if __name__ == "__main__":
    sdServer = ServiceDiscoveryServer('127.0.0.1', 45444, 80)