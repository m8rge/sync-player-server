import SocketServer
import socket
import json
import threading
import staticPlugin

#todo: more type checking

class SyncPlayerServer:

    protocolVersion = '1.0'
    pluginInterface = None

    def __init__(self, ip, port):
        self.pluginInterface = staticPlugin.staticPlugin

        while self.isOpenTcpPort(ip, port):
            port+=1

        server = self.ThreadedTCPServer((ip, port), self.getHandlerClass(self.pluginInterface))
        server_thread = threading.Thread(server.serve_forever)
        server_thread.start()
        print "opened {}:{}".format(ip, port)

    def isOpenTcpPort(self, ip, port):
        s = socket.socket()
        #noinspection PyBroadException
        try:
            s.bind((ip, port))
            s.close()
            return False
        except:
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

                    #noinspection PyBroadException
                    try:
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
                    except:
                        processClientData = False
        return Handler

if __name__ == "__main__":
    syncPlayerServer = SyncPlayerServer('127.0.0.1', 45444)

#    class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
#        def handle(self):
#            data = self.request.recv(1024)
#            cur_thread = threading.current_thread()
#            response = "{}: {}".format(cur_thread.name, data)
#            self.request.send(response)
#
#class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
#    pass
#
#if __name__ == "__main__":
#    HOST, PORT = "127.0.0.1", 0
#
#    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
#    ip, port = server.server_address
#    server_thread = threading.Thread(target=server.serve_forever)
#    server_thread = threading.Thread(server.serve_forever)
#    server_thread.daemon = True
#    server_thread.start()
#    print "opened {}:{}, thread:{}".format(HOST, PORT, server_thread.name)
