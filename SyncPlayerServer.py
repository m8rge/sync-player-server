import SocketServer
import socket
import json
import threading

import staticPlugin #todo: import plugin from config
import ServiceDiscoveryServer

class SyncPlayerServer:

    protocolVersion = '1.0'
    pluginInterface = None

    def __init__(self, ip, port):
        self.pluginInterface = staticPlugin.staticPlugin()

        udpPort = port
        while self.isOpenTcpPort(ip, port):
            port+=1

        server = self.ThreadedTCPServer((ip, port), self.getHandlerClass(self.pluginInterface))
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.start()
        print "sps started at {}:{}".format(ip, port)
        threading.Thread(ServiceDiscoveryServer.ServiceDiscoveryServer(ip, udpPort, port))

    def isOpenTcpPort(self, ip, port):
        s = socket.socket()
        try:
            s.bind((ip, port))
            s.close()
            return False
        except IOError:
            return True

    class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
        pass

    def getHandlerClass(self, pluginInterface):
        class Handler(SocketServer.BaseRequestHandler):
            def handle(self):
                processClientData = True
                while processClientData:
                    buffer = ''
                    while buffer == '' or (buffer.startswith('{') and '}' not in buffer) or len(buffer)>1024:
                        buffer+= self.request[0].strip()

                    try:
                        #todo: more type checking
                        request = json.loads(buffer)
                        if request['command'] == 'hello':
                            answer = {'answer': 'hello', 'protocol': protocolVersion}
                            self.request.sendall(json.dumps(answer))
                            if request['protocol'] != protocolVersion:
                                processClientData = False

                        if request['command'] == 'getAlbums':
                            answer = pluginInterface.getAlbums()
                            self.request.sendall(json.dumps(answer))

                        if request['command'] == 'getSongsInfo':
                            answer = pluginInterface.getSongsInfo(request['albumId'])
                            self.request.sendall(json.dumps(answer))

                        if request['command'] == 'getSongs':
                            for audioId in request['audioIds']:
                                song = pluginInterface.getSong(audioId)
                                answer = {'id': song.id, 'length': song.length}
                                self.request.sendall(json.dumps(answer))
                                self.request.send(song.data)
                            self.request.sendall(json.dumps({'action':'stop'}))
                    except ValueError:
                        processClientData = False
        return Handler

if __name__ == "__main__":
    hostname = socket.gethostbyname(socket.gethostname())
    syncPlayerServer = SyncPlayerServer(hostname, 45444) #todo: define port