from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.static import File
from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS
from say import speak
from config import ports


class BroadcastServerProtocol(WebSocketServerProtocol):

    def onOpen(self):
        self.factory.register(self)
        speak( "Welcome, Enter message to share." )

    def onMessage(self, payload, isBinary):
        message = payload.decode('utf8')
        speak( message )

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)


class BroadcastServerFactory(WebSocketServerFactory):

    def __init__(self, url, debug=False, debugCodePaths=False):
        WebSocketServerFactory.__init__(self, url)
        self.clients = []

    def register(self, client):
        if client not in self.clients:
            self.clients.append(client)

    def unregister(self, client):
        if client in self.clients:
            self.clients.remove(client)

    def broadcast(self, msg):
        for client in self.clients:
            client.sendMessage(msg.encode('utf8'))


ServerFactory = BroadcastServerFactory
factory = ServerFactory("ws://localhost:%s" % ports["ws_server"])

factory.protocol = BroadcastServerProtocol
listenWS(factory)

web_root = File("web")
web = Site(web_root)
reactor.listenTCP(ports["static_server"], web)
reactor.run()
